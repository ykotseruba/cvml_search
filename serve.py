"""
Flask server backend

ideas:
- allow delete of tags
- unify all different pages into single search filter sort interface
- special single-image search just for paper similarity
"""

import os
import re
import time
import datetime
import xapian
import json
from random import shuffle

import numpy as np
from sklearn import svm

from flask import Flask, request, redirect, url_for
from flask import render_template
from flask import g # global session-level object
from flask import session

#from aslite.db import get_papers_db, get_metas_db, get_tags_db, get_last_active_db, get_email_db
#from aslite.db import load_features

# -----------------------------------------------------------------------------
# inits and globals

RET_NUM = 100 # number of papers to return per page

app = Flask(__name__)

# set the secret key so we can cryptographically sign cookies and maintain sessions
if os.path.isfile('secret_key.txt'):
    # example of generating a good key on your system is:
    # import secrets; secrets.token_urlsafe(16)
    sk = open('secret_key.txt').read().strip()
else:
    print("WARNING: no secret key found, using default devkey")
    sk = 'devkey'
app.secret_key = sk

# -----------------------------------------------------------------------------
# globals that manage the (lazy) loading of various state for a request

def get_tags():
    if g.user is None:
        return {}
    if not hasattr(g, '_tags'):
        with get_tags_db() as tags_db:
            tags_dict = tags_db[g.user] if g.user in tags_db else {}
        g._tags = tags_dict
    return g._tags

def get_papers():
    if not hasattr(g, '_pdb'):
        g._pdb = get_papers_db()
    return g._pdb

def get_metas():
    if not hasattr(g, '_mdb'):
        g._mdb = get_metas_db()
    return g._mdb

def get_enquire():
    if not hasattr(g, '_enquire'):
        database = xapian.WritableDatabase('xapiandb')
        g._enquire = xapian.Enquire(database)
    return g._enquire

def get_parser():
    if not hasattr(g, '_qp'):
        queryparser = xapian.QueryParser()
        queryparser.set_stemmer(xapian.Stem("en"))
        queryparser.set_stemming_strategy(queryparser.STEM_SOME)
        queryparser.add_prefix("title", "XTITLE")
        queryparser.add_prefix("summary", "XSUMMARY")
        g._qp = queryparser
    return g._qp

@app.before_request
def before_request():
    g.user = session.get('user', None)

    # record activity on this user so we can reserve periodic
    # recommendations heavy compute only for active users
    if g.user:
        with get_last_active_db(flag='c') as last_active_db:
            last_active_db[g.user] = int(time.time())

@app.teardown_request
def close_connection(error=None):
    # close any opened database connections
    if hasattr(g, '_pdb'):
        g._pdb.close()
    if hasattr(g, '_mdb'):
        g._mdb.close()

# -----------------------------------------------------------------------------
# ranking utilities for completing the search/rank/filter requests

def render_paper(paper):
    # render a single paper with just the information we need for the UI
    #pdb = get_papers()
    #tags = get_tags()
    #thumb_path = 'static/thumb/' + pid + '.jpg'
    #thumb_url = thumb_path if os.path.isfile(thumb_path) else ''
    #d = pdb[pid]
    return dict(
        weight = 0.0,
        id = d['_id'],
        link = d['link'],
        title = d['title'],
        code = d.get('code'),
        time = d['_time_str'],
        authors = ', '.join(a['name'] for a in d['authors']),
        tags = ', '.join(t['term'] for t in d['tags']),
        utags = [t for t, pids in tags.items() if pid in pids],
        summary = d['summary'],
        thumb_url = thumb_url,
    )


def search_rank(q: str = ''):
    if not q:
        return [], [] # no query? no results
    
    parser = get_parser()
    enquire = get_enquire()

    enquire.set_query(parser.parse_query(q))

    offset = 0
    pagesize = 1000

    # And print out something about each match
    matches = []
    for match in enquire.get_mset(offset, pagesize):
        fields = json.loads(match.document.get_data().decode('utf8'))
        fields.pop('txt', None) # remove full text
        fields['weight'] = match.weight
        matches.append(fields)

    return matches

# -----------------------------------------------------------------------------
# primary application endpoints

def default_context():
    # any global context across all pages, e.g. related to the current user
    context = {}
    context['user'] = g.user if g.user is not None else ''
    return context

@app.route('/', methods=['GET'])
def main():

    # default settings
    default_rank = 'search'
    default_tags = ''
    default_q = 'visual attention'
    default_from_year = '2010'
    default_to_year = f'{datetime.date.today().strftime("%Y")}'
    default_skip_have = 'no'

    # override variables with any provided options via the interface
    opt_rank = request.args.get('rank', default_rank) # rank type. search|tags|pid|time|random
    opt_q = request.args.get('q', default_q) # search request in the text box
    opt_tags = request.args.get('tags', default_tags)  # tags to rank by if opt_rank == 'tag'
    opt_pid = request.args.get('pid', '')  # pid to find nearest neighbors to
    opt_from_year = request.args.get('from_year', default_from_year) # start year
    opt_to_year = request.args.get('to_year', default_to_year) # end year
    opt_skip_have = request.args.get('skip_have', default_skip_have) # hide papers we already have?
    opt_svm_c = request.args.get('svm_c', '') # svm C parameter
    opt_page_number = request.args.get('page_number', '1') # page number for pagination

    # if a query is given, override rank to be of type "search"
    # this allows the user to simply hit ENTER in the search field and have the correct thing happen
    matches = search_rank(q=opt_q)

    num_papers_found = len(matches)

    # if  opt_from_year != default_from_year or opt_to_year != default_to_year or opt_tags != default_tags:
    #     mdb = get_metas()
    #     kv = {k:v for k,v in mdb.items()} # read all of metas to memory at once, for efficiency

    # filter by time
    if opt_from_year != default_from_year or opt_to_year != default_to_year:
        end = int(opt_to_year)
        start = int(opt_from_year)
        #print(time, end, start)
        #keep = [i for i,pid in enumerate(pids) if (kv[pid]['year'] >= start and kv[pid]['year'] <= end)]
        matches = [m for m in matches if (m['year'] >= start and m['year'] <= end)]
        #pids, scores = [pids[i] for i in keep], [scores[i] for i in keep]
        num_papers_found = len(matches)

    # filter by venue
    if opt_tags != default_tags:
        venues = [x.lower().strip() for x in opt_tags.split(',')]
        #keep = [i for i,pid in enumerate(pids) if kv[pid]['venue'] in venues]
        matches = [m for m in matches if m['venue'].lower() in venues]
        #pids, scores = [pids[i] for i in keep], [scores[i] for i in keep]
        num_papers_found = len(matches)

    # crop the number of results to RET_NUM, and paginate
    try:
        page_number = max(1, int(opt_page_number))
    except ValueError:
        page_number = 1
    start_index = (page_number - 1) * RET_NUM # desired starting index
    end_index = min(start_index + RET_NUM, len(matches)) # desired ending index
    papers = matches[start_index:end_index]

    # render all papers to just the information we need for the UI
    #papers = [render_pid(pid) for pid in pids]
    #for i, p in enumerate(papers):
    #    p['weight'] = float(i)

    # build the current tags for the user, and append the special 'all' tag
    tags = get_tags()
    #rtags = [{'name':t, 'n':len(pids)} for t, pids in tags.items()]
    #if rtags:
    #    rtags.append({'name': 'all'})

    # build the page context information and render
    context = default_context()
    context['papers'] = papers
    context['tags'] = ''
    context['words'] = []
    context['num_found'] = num_papers_found
    context['words_desc'] = "Here are the top 40 most positive and bottom 20 most negative weights of the SVM. If they don't look great then try tuning the regularization strength hyperparameter of the SVM, svm_c, above. Lower C is higher regularization."
    context['gvars'] = {}
    context['gvars']['rank'] = opt_rank
    context['gvars']['tags'] = opt_tags
    context['gvars']['pid'] = opt_pid
    context['gvars']['to_year'] = opt_to_year
    context['gvars']['from_year'] = opt_from_year
    context['gvars']['skip_have'] = opt_skip_have
    context['gvars']['search_query'] = opt_q
    #context['gvars']['svm_c'] = str(C)
    context['gvars']['page_number'] = str(page_number)
    return render_template('index.html', **context)

# @app.route('/inspect', methods=['GET'])
# def inspect():

#     # fetch the paper of interest based on the pid
#     pid = request.args.get('pid', '')
#     pdb = get_papers()
#     if pid not in pdb:
#         return "error, malformed pid" # todo: better error handling

#     # load the tfidf vectors, the vocab, and the idf table
#     features = load_features()
#     x = features['x']
#     idf = features['idf']
#     ivocab = {v:k for k,v in features['vocab'].items()}
#     pix = features['pids'].index(pid)
#     wixs = np.flatnonzero(np.asarray(x[pix].todense()))
#     words = []
#     for ix in wixs:
#         words.append({
#             'word': ivocab[ix],
#             'weight': float(x[pix, ix]),
#             'idf': float(idf[ix]),
#         })
#     words.sort(key=lambda w: w['weight'], reverse=True)

#     # package everything up and render
#     paper = render_pid(pid)
#     context = default_context()
#     context['paper'] = paper
#     context['words'] = words
#     context['words_desc'] = "The following are the tokens and their (tfidf) weight in the paper vector. This is the actual summary that feeds into the SVM to power recommendations, so hopefully it is good and representative!"
#     return render_template('inspect.html', **context)

@app.route('/profile')
def profile():
    context = default_context()
    with get_email_db() as edb:
        email = edb.get(g.user, '')
        context['email'] = email
    return render_template('profile.html', **context)

@app.route('/stats')
def stats():
    context = default_context()
    mdb = get_metas()
    kv = {k:v for k,v in mdb.items()} # read all of metas to memory at once, for efficiency
    times = [v['_time'] for v in kv.values()]
    tstr = lambda t: time.strftime('%b %d %Y', time.localtime(t))

    context['num_papers'] = len(kv)
    if len(kv) > 0:
        context['earliest_paper'] = tstr(min(times))
        context['latest_paper'] = tstr(max(times))
    else:
        context['earliest_paper'] = 'N/A'
        context['latest_paper'] = 'N/A'

    # count number of papers from various time deltas to now
    tnow = time.time()
    for thr in [1, 6, 12, 24, 48, 72, 96]:
        context['thr_%d' % thr] = len([t for t in times if t > tnow - thr*60*60])

    return render_template('stats.html', **context)

@app.route('/about')
def about():
    context = default_context()
    return render_template('about.html', **context)

# -----------------------------------------------------------------------------
# tag related endpoints: add, delete tags for any paper

@app.route('/add/<pid>/<tag>')
def add(pid=None, tag=None):
    if g.user is None:
        return "error, not logged in"
    if tag == 'all':
        return "error, cannot add the protected tag 'all'"
    elif tag == 'null':
        return "error, cannot add the protected tag 'null'"

    with get_tags_db(flag='c') as tags_db:

        # create the user if we don't know about them yet with an empty library
        if not g.user in tags_db:
            tags_db[g.user] = {}

        # fetch the user library object
        d = tags_db[g.user]

        # add the paper to the tag
        if tag not in d:
            d[tag] = set()
        d[tag].add(pid)

        # write back to database
        tags_db[g.user] = d

    print("added paper %s to tag %s for user %s" % (pid, tag, g.user))
    return "ok: " + str(d) # return back the user library for debugging atm

@app.route('/sub/<pid>/<tag>')
def sub(pid=None, tag=None):
    if g.user is None:
        return "error, not logged in"

    with get_tags_db(flag='c') as tags_db:

        # if the user doesn't have any tags, there is nothing to do
        if not g.user in tags_db:
            return "user has no library of tags ¯\_(ツ)_/¯"

        # fetch the user library object
        d = tags_db[g.user]

        # add the paper to the tag
        if tag not in d:
            return "user doesn't have the tag %s" % (tag, )
        else:
            if pid in d[tag]:

                # remove this pid from the tag
                d[tag].remove(pid)

                # if this was the last paper in this tag, also delete the tag
                if len(d[tag]) == 0:
                    del d[tag]

                # write back the resulting dict to database
                tags_db[g.user] = d
                return "ok removed pid %s from tag %s" % (pid, tag)
            else:
                return "user doesn't have paper %s in tag %s" % (pid, tag)

@app.route('/del/<tag>')
def delete_tag(tag=None):
    if g.user is None:
        return "error, not logged in"

    with get_tags_db(flag='c') as tags_db:

        if g.user not in tags_db:
            return "user does not have a library"

        d = tags_db[g.user]

        if tag not in d:
            return "user does not have this tag"

        # delete the tag
        del d[tag]

        # write back to database
        tags_db[g.user] = d

    print("deleted tag %s for user %s" % (tag, g.user))
    return "ok: " + str(d) # return back the user library for debugging atm

# -----------------------------------------------------------------------------
# endpoints to log in and out

@app.route('/login', methods=['POST'])
def login():

    # the user is logged out but wants to log in, ok
    if g.user is None and request.form['username']:
        username = request.form['username']
        if len(username) > 0: # one more paranoid check
            session['user'] = username

    return redirect(url_for('profile'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('profile'))

# -----------------------------------------------------------------------------
# user settings and configurations

@app.route('/register_email', methods=['POST'])
def register_email():
    email = request.form['email']

    if g.user:
        # do some basic input validation
        proper_email = re.match(r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$', email, re.IGNORECASE)
        if email == '' or proper_email: # allow empty email, meaning no email
            # everything checks out, write to the database
            with get_email_db(flag='c') as edb:
                edb[g.user] = email

    return redirect(url_for('profile'))

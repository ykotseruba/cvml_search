"""
This script is intended to wake up every 30 min or so (eg via cron),
it checks for any new arxiv papers via the arxiv API and stashes
them into a sqlite database.
"""

import sys
import os
import time
from datetime import datetime
import random
import logging
import argparse
import pandas as pd
from tqdm import tqdm

from aslite.arxiv import get_response, parse_response
from aslite.db import get_papers_db, get_metas_db

data_path = '/home/yulia/Documents/cv_search/data/'
venue_dates = pd.read_excel(os.path.join(data_path, 'venue_dates.xlsx'))

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO, format='%(name)s %(levelname)s %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    parser = argparse.ArgumentParser(description='Paper Daemon')
    parser.add_argument('-v', '--venue', type=str, default='CVPR2023', help='Fetch papers from this venue')
    args = parser.parse_args()
    print(args)

    pdb = get_papers_db(flag='c')
    mdb = get_metas_db(flag='c')
    prevn = len(pdb)

    def store(p):
        pdb[p['_id']] = p
        mdb[p['_id']] = {'_time': p['_time']}

    paperlist_path = os.path.join(data_path, 'paperlists_v2', f'{args.venue}.xlsx')
    if os.path.exists(paperlist_path):
        paperlist_df = pd.read_excel(paperlist_path)
    else:
        print('ERROR: Expected to find paperlist at {paperlist_path} but file does not exist!')
        sys.exit(-1)

    # load papers from the venue
    num_papers = len(paperlist_df)
    raw_date = venue_dates[venue_dates['Venue']==args.venue]['Date'].values[0].astype(str).split('T')[0]
    dt = datetime.strptime(raw_date, '%Y-%m-%d')
    timestamp = time.mktime(dt.timetuple())
    time_str = dt.strftime("%B %d, %Y") 

    for idx, row in tqdm(paperlist_df.iterrows(), desc=f'Loading {args.venue}', total=num_papers):
        try:
            p = {}
            p['_id'] = row['id']
            p['_time'] = timestamp
            p['_time_str'] = time_str
            p['authors'] = [{'name': an.strip()} for an in row['authors'].split(',')]
            p['title'] = row['title']
            p['tags'] = [{'term': args.venue}]
            p['link'] = row['link']
            p['code'] = row['code']
            p['summary'] = row['abstract']
            store(p)
        except Exception:
            print(p)
            sys.exit(-1)
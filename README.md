# cvml-sanity

cvml-sanity is a paper search engine for major computer vision, machine learning, and robotics venues. The code is repurposed from arxiv-sanity-lite (https://github.com/karpathy/arxiv-sanity-lite).

The database includes **117,672 papers** from the following conferences:

Computer vision: 
- **CVPR** 2010 -- 2024
- **ECCV** 2010 -- 2022
- **ICCV** 2011 -- 2023
- **ACCV** 2010 -- 2022
- **BMVC** 2010 -- 2023
- **WACV** 2014 -- 2024
  
Robotics:
- **ICRA** 1998 -- 2023
- **IROS** 2010 -- 2023
- **CoRL** 2017 -- 2023
- **RSS**  2005 -- 2023

Machine learning:
- **NeurIPS** 2010 -- 2023
- **ICML** 2010 -- 2023
- **ICLR** 2013 -- 2023

AI:
- **AAAI** 2010 -- 2024

#### Requirements

Install via requirements:

```bash
pip install -r requirements.txt
```

Download and install the xapian from https://xapian.org/download. The easiest option on Ubuntu is to add the PPA from https://launchpad.net/~xapian/+archive/ubuntu/backports and then install via `sudo apt-get install python3-xapian`
(If using virtualenv, you might need to add the installed xapian to python search path. For example, creating a [`.venv/lib/python3.8/site-packages/xapian.pth` file](https://docs.python.org/3.11/library/site.html) containing directory where xapian is installed.)

### Setup
Download paper database using the link below

https://drive.google.com/file/d/1iXQzyQSq4jMpAOa2Usx5qdB-9NqPJWlm/view?usp=drive_link

Extract the archive into the `cvml_search` directory. The database folder is called `xapiandb`.

To start the app locally, type in terminal:

```
./serve.sh
```

Then open http://127.0.0.1:5000/ in the browser.

### Search

Search relies on the [Xapian engine](https://xapian.org/).

## Queries

-- Regular text queries, e.g. 'visual attention'

-- Boolean expressions, e.g. 'visual AND attention', 'visual OR attention', 'visual NOT attention'. Note: pure NOT queries are not supported, e.g. 'NOT attention' will not work

-- Occurrences of terms close together, e.g. 'visual NEAR attention' will match only documents where these terms occur within a few words of one another.

## Filtering results

Filter by venue -- enter venue names separated by commas, e.g. cvpr,bmvc,iros. Not case sensitive.

Filter by year -- enter a range of years. Papers published between these values (inclusive) will be returned.

## Number of papers returned

By default, 1,000 top results are returned. If a higher number is desired, change the constant `pagesize' on line 137 of `serve.py`. Note that higher numbers (e.g. 10,000) may slow down the application.

### TODO: 
- [ ] ICLR 2024
- [ ] ICRA 2024
- [ ] full-text search for ICRA
- [ ] ~~add IJCAI?~~
- [ ] ~~add HCI?~~
- [ ] workshops papers? 
- [ ] show conference stats in README
- [ ] add option for searching specific fields (e.g. authors or titles)
- [ ] remove 'inspect' links
- [ ] fix 'stats' page

#### License

MIT

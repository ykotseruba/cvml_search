# cvml-sanity

cvml-sanity is a paper search engine for major computer vision, machine learning, robotics, and AI conferences and journals. The code is repurposed from [arxiv-sanity-lite](https://github.com/karpathy/arxiv-sanity-lite). 

The database includes **133,117 papers** from the following conferences (*excluding workshops*) and journals:

Computer vision: 
- **CVPR** 2009 -- 2024
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
- **R-AL** 2016 -- 2024 (up to August)

Machine learning:
- **NeurIPS** 2010 -- 2023
- **ICML** 2010 -- 2024
- **ICLR** 2013 -- 2024
- **JMLR** 2010 -- 2024 (up to August)

AI:
- **AAAI** 2010 -- 2024

<p align="center">
<img src="images/papers_per_year.png" alt="stats" align="middle" width="1000"/>
</p>
<br/><br/>


## Requirements

Install via requirements:

```bash
pip install -r requirements.txt
```

Download and install the xapian from https://xapian.org/download. The easiest option on Ubuntu is to add the PPA from https://launchpad.net/~xapian/+archive/ubuntu/backports:

```
sudo add-apt-repository ppa:xapian/backports
sudo apt update
sudo apt-get install python3-xapian`
```

(If using virtualenv, you might need to add the installed xapian to python search path. For example, creating a [`.venv/lib/python3.8/site-packages/xapian.pth` file](https://docs.python.org/3.11/library/site.html) containing directory where xapian is installed.)

## Setup
Download paper database using the link below

https://drive.google.com/file/d/1iXQzyQSq4jMpAOa2Usx5qdB-9NqPJWlm/view?usp=drive_link (approx. 6GB, updated Jul 28, 2024)

Extract the archive into the `cvml_search` directory. The database folder is called `xapiandb`.

To start the app locally, type in terminal:

```
./serve.sh
```

Then open http://127.0.0.1:5000/ in the browser.

## Search

Search relies on the [Xapian engine](https://xapian.org/).

### Queries

-- Regular text queries, e.g. 'visual attention'

-- Boolean expressions, e.g. 'visual AND attention', 'visual OR attention', 'visual NOT attention'. Note: pure NOT queries are not supported, e.g. 'NOT attention' will not work

-- Occurrences of terms close together, e.g. 'visual NEAR attention' will match only documents where these terms occur within a few words of one another.

A complete list of supported queries can be found [in the official Xapian documentation](https://getting-started-with-xapian.readthedocs.io/en/latest/concepts/search/queries.html#).

### Filtering results

Two additional text fields below the search results allow filtering the results.

Filter by venue -- enter venue names separated by commas, e.g. cvpr,bmvc,iros. Not case sensitive.

Filter by year -- enter a range of years. Papers published between these values (inclusive) will be returned (e.g. to find all papers from 2022, enter 2022-2022)

### Number of papers returned

By default, 1,000 top results are returned. This number is controlled by the `pagesize` constant on line 137 of `serve.py`. Note that setting it to a higher number (e.g., 10,000) may significantly slow down the application.

### TODO: 
- [ ] ICRA 2024
- [ ] full-text search for ICRA/IROS/R-AL
- [ ] R-AL
- [ ] JMLR
- [ ] ~~add IJCAI?~~
- [ ] ~~add HCI?~~
- [ ] workshops papers? 
- [ ] add option for searching specific fields (e.g. authors or titles)
- [ ] fix 'stats' page

#### License

MIT

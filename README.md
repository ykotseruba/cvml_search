# cvml-sanity

cvml-sanity is a paper search engine for major computer vision, machine learning, and robotics venues. The code is repurposed from arxiv-sanity-lite (https://github.com/karpathy/arxiv-sanity-lite).

The database includes **114,957 papers** from the following conferences:

Computer vision: 
- **CVPR** 2010 -- 2023
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

### How to use
Before the first use, run `make` to initialize the database:
```
make up
```


To start the app locally, in terminal:

```
./serve.sh
```

Then open http://127.0.0.1:5000/ in the browser.


### TODO: 
- [x] enable filtering results by year and conference
- [x] add ICML (2010-2012)
- [x] add ICLR (2017-2019)
- [x] add CoRL
- [x] add RSS
- [x] add AAAI
- [ ] add IJCAI?
- [ ] add HCI?
- [ ] workshops papers? 
- [x] add code links to IROS, ICRA
- [ ] show conference stats in README
- [ ] semantic search?
- [ ] full-text search, currently only abstracts and titles are searched

#### License

MIT

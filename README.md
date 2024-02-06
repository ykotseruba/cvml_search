# cvml-sanity

cvml-sanity is a paper search engine for major computer vision, machine learning, and robotics venues. The code is repurposed from arxiv-sanity-lite (https://github.com/karpathy/arxiv-sanity-lite).

The database includes approx. 80K papers from the following conferences:

Computer vision: 
- **CVPR** 2010 -- 2023
- **ECCV** 2010 -- 2022
- **ICCV** 2011 -- 2023
- **ACCV** 2010 -- 2022
- **BMVC** 2010 -- 2023
- **WACV** 2016 -- 2023
  
Robotics:
- **ICRA** 1998 -- 2023
- **IROS** 2010 -- 2023

Machine learning:
- **NeurIPS** 2010 -- 2022
- **ICML** 2013 -- 2023

#### Requirements

 Install via requirements:

 ```bash
 pip install -r requirements.txt
 ```

### How to use
Before first use, run `make` to initialize the database:
```
make up
```


Run in terminal:

```
./serve.sh
```

Then open http://127.0.0.1:5000/ in the browser.


### TODO: 
- [ ] enable filtering results by year and conference
- [ ] add ICML (2010-2012), ICLR, AR-L, NeurIPS 2023, CoRL, AAAI
- [ ] workshops papers? 
- [ ] add code links to IROS, ICRA
- [ ] show conference stats in README
- [ ] semantic search?
- [ ] full-text search, currently only abstracts and titles are searched

#### License

MIT

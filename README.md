# cvml-sanity

cvml-sanity is a paper search engine for major computer vision, machine learning, and robotics venues. The code is repurposed from arxiv-sanity-lite (https://github.com/karpathy/arxiv-sanity-lite).

Currently the database contains approx. 80K papers from the following conferences:

Computer vision: 
- **CVPR** 2010 -- present
- **ECCV** 2010 -- present
- **ICCV** 2011 -- present
- **ACCV** 2010 -- present
- **BMVC** 2010 -- present
- **WACV** 2016 -- present

Robotics:
- **ICRA** 1998 -- present
- **IROS** 2010 -- present

Machine learning:
- **NeurIPS** 2010 -- present
- **ICML** 2013 -- present

#### Requirements

 Install via requirements:

 ```bash
 pip install -r requirements.txt
 ```

### How to use

To run locally:

```
./serve.sh
```

Then open http://127.0.0.1:5000/ in your browser.


### TODO: 
- [ ] filter results by year and conference
- [ ] add ICML (2010-2012), ICLR, AR-L
- [ ] add code links to IROS, ICRA
- [ ] conference stats

#### License

MIT

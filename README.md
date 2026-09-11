This repository contains the code for our paper: Self-Defense: Optimal QIF Solutions and Application to Website Fingerprinting



## Dataset

The datasets used are in folders: channel, channel_with_levels, new_scrap and the csv's on the top level


## Plots

The plots of the paper are in the folder paper's plot



## Code

* self-defence.py: tests the LP of Section 3 and Section 4. the implementation of the related LPs are directly in the QIF library
* exp.py: extends self-defence.py; conducts the experiments of the experimental section
* cluster.py: helper file used to cluster data (for additional statistics - not used in paper)
* make_channel_new_scrape.py: scrapes the websites of the Appendix. Visits them and stores their behaviour. 

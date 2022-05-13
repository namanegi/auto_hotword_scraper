# auto_hotword_scraper
## Introduction
### Abstract
* An auto workflow for discovering recent hot topics from Japanese News sites
### Work Flow
1. Scraping sentences from recent Japanese News sites
2. Tokenizing sentences from Step 1 by fugashi
3. Word2Vec using gensim
4. Analysis
    1. Dimension reduction
    2. Autoly find best K value for Kmeans algorithm
    3. Clustering
5. Output each cluster
    1. Sentences near cluser centers
    2. Hot words
    3. Hot sentences (Sentences have most hot words)

import pandas as pd
from metapub import PubMedFetcher
fetch = PubMedFetcher()
keyword="sepsis"

# get the  PMID for first 3 articles with keyword sepsis
pmids = fetch.pmids_for_query(keyword)

# get  articles
articles = {}
for pmid in pmids:
    articles[pmid] = fetch.article_by_pmid(pmid)

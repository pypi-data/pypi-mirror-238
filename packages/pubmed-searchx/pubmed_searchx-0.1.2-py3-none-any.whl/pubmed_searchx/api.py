import requests
import json
SEARCH_PREF = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&sort=relevance&size=200&term="
SUMMARY_PUBMEDS_PREF = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id="

def __gen_query_by_pairs(ls):
    s = []
    for l in ls:
        p1, p2 = l
        p1 = p1.replace(" ","+")
        p2 = p2.replace(" ","+")
        cp = p1 + "+AND+" + p2
        s.append(cp)
    return "+OR+".join(s)

def __search_query_pubmed(query):
    url = SEARCH_PREF + query
    # print(url)
    response = requests.get(url)
    res =  response.text
    # print(res)
    return res
def search_pairs_pubmed(pairs):
    query = __gen_query_by_pairs(pairs)
    return __search_query_pubmed(query), query

def get_sum_pubmed_by_ids(ids):
    if type(ids) == list:
        ids = ",".join(ids)
    url = SUMMARY_PUBMEDS_PREF + ids
    response = requests.get(url)
    res = response.text

    return res




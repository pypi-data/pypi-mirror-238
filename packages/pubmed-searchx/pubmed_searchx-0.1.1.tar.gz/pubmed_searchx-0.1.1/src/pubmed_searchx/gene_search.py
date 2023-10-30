import time
from tqdm import tqdm
from .api import search_pairs_pubmed, get_sum_pubmed_by_ids
from .parser import parse_info_from_summary, parse_ids_from_response
from .utils import getCurrentTimeString, load_list_from_file, ensureDir, print_db
import json
from collections import OrderedDict

W_HITS = 0
W_INFO = 1

PUBMED_PREF = "https://pubmed.ncbi.nlm.nih.gov/"


def gene_search(pairs, authors=True, title=True, year=True, pubmed_id=True, path_out=None, max_retry=3):
    r"""

    :param pairs: [(gene_name_1, disease_name_1),(gene_name_1, disease_name_1)]

    :param authors: select authors
    :param title: select title
    :param year: select year
    :param pubmed_id: select pubmed_id
    :return:
    """
    info = {}
    is_success = False
    i_retry = 0

    while i_retry <= max_retry and is_success is False:
        try:
            selectors = OrderedDict([("authors", authors), ("title", title), ("year", year), ("pubmed_id", pubmed_id)])
            res, query = search_pairs_pubmed(pairs)
            ids = parse_ids_from_response(res)
            re_sum = get_sum_pubmed_by_ids(ids)
            info = parse_info_from_summary(re_sum, selectors)

            is_success = True
        except:
            i_retry += 1
            time.sleep(1)

    if path_out is not None:
        fout = open(path_out, "w")
        fout.write("QUERY: " + query + "\n")
        if not is_success:
            fout.write("Some error happens, please try again!\n")
        else:
            fout.write(json.dumps(info, indent=2))
        fout.close()
    return info, is_success


def write_info(fstats, gene_name, info, tp=W_INFO, json_dir=None):
    s = []
    gene = None
    pubmed_ids = []
    urls = []

    if tp == W_INFO:
        for ii in info:
            pubmed_ids.append(ii['pubmed_id'])
        if len(pubmed_ids) == 0:
            pubmed_ids = ["No_Hit"]
        fstats.write("%s\t%s\n" % (gene_name, ",".join(pubmed_ids)))
    else:
        fstats.write("%s\t%s\n" % (gene_name, len(info)))

    if json_dir is not None:
        fout = open("%s/%s.json" % (json_dir, gene_name), "w")
        fout.write(json.dumps(info, indent=2))
        fout.close()


def search_from_file(gene_list_path, term_list_path, dir_out=None, authors=True, title=True, year=True, pubmed_id=True, verbose=True):
    gene_list = load_list_from_file(gene_list_path)
    term_list = load_list_from_file(term_list_path)

    time_stamp = getCurrentTimeString()
    if dir_out is None:
        dir_out = "./"

    for term in term_list:
        term_result_dir = dir_out + "/" + "_".join(gene_list) + "_" + term + "_" + time_stamp
        ensureDir(term_result_dir)
        fpubmed_id = open("%s/pubmed_id_results.csv" % term_result_dir, "w")
        fpubmed_id.write("Gene\tPubmed_Ids\n")
        fcount = open("%s/count_hits.csv" % term_result_dir, "w")
        fpubmed_id.write("Gene\t#Hits\n")

        json_subdir = "%s/json_dir/" % term_result_dir
        ensureDir(json_subdir)
        print_db(verbose, "Searching for ", term, "...")
        print_db(True,"Result directory: ", term_result_dir)
        for gene in tqdm(gene_list):
            pairs = [(gene, term)]
            info, is_success = gene_search(pairs=pairs, authors=authors, title=title, year=year, pubmed_id=pubmed_id)
            write_info(fpubmed_id,gene,info,W_INFO, json_subdir)
            write_info(fcount, gene, info, W_HITS)
        fpubmed_id.close()
        fcount.close()
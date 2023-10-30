### Example

## Installation
```shell
    pip install pubmed_searchx     
```
## Running from command line
```shell
    python -m pubmed_searchx PATH_TO_GENE_LIST PATH_TO_TERM_LIST {-r: Optional for using hreflink pubmed} {-d PATH_TO_RESULT_DIR}  
```
Example:

Input:

gene_test.txt:

REST\
CJKG\
CORIN\
EGF1

term_test.txt:

depression\
migraine

```shell
    python -m pubmed_searchx -g gene_test.txt -t term_test.txt -d "./"
```

Output example:
Folder:
REST_CJKG_CORIN_EGF1_depression_{time_stamp}/
- pubmed_id_results.csv:

| Gene        | Pubmed_Ids                                                                                                                                                                           |
| ----------- |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| REST      | 35216520,35231204,31376646,34555652,32739332,34388482,35522984,34709765,25785575,30761967,23856279,28488270,30979801,17653294,30962366,24256499,15167093,27185312,21677641,24313703  |
| CJKG   | No_Hit                                                                                                                                                                               |
| CORIN | 26667411,7759658,36097420,30148170,32257992,37895290,7798487,2766190,1825625,3383412                                                                                                 |
| EGF1 | 15892860                                                                                                                                                                             |

(With -r option, the pubmed_id becomes: 35216520(https://pubmed.ncbi.nlm.nih.gov/35216520))

- cout_hist.csv:

| Gene	| #Hits |
|-------|-------|
| REST | 20 |
|CJKG | 0 |
|CORIN | 10 |
|EGF1 | 1 |

- json_dir/*.json: (e.g. CORIN.json)

[
  {
    "authors": "Monroe SM;Harkness KL",
    "title": "Major Depression and Its Recurrences: Life Course Matters.",
    "year": "2022",
    "pubmed_id": "35216520"
  },
....
]


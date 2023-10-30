### Example

```shell
    from pubmed_searchx import gene_search
    pairs = [("corin", "depression")]
    output_file = "out.json" # Set to None if do not write to file
    info_list, return_code = gene_search(pairs, authors=True, title=True,
    year=True, pubmed_id=True, path_out=output_file)  
     
```
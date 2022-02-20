New features for *airpg*
=======================

A set of new developments for *airpg* (https://doi.org/10.1186/s12859-021-04309-y)

### List of new features:
1. Identification of genus names in scientific abstracts using *sklearn*

![](https://github.com/michaelgruenstaeudl/airpg_newFeatures/blob/master/figure_matches.png)

### Generating input for new features

###### Identification of genus names in scientific abstracts using *sklearn*
```
while IFS="" read -u10 -r family || [ -n "$family" ]
do
  # Get genus names
  wget "http://www.theplantlist.org/1.1/browse/A/${family}/${family}.csv"
  awk -F',' '{print $5}' ${family}.csv | sort -u > ${family}_genera.txt
  # Get scientific abstracts
  esearch -db pubmed -query "${family} [TITLE]" | \
    efetch -format abstract 1>${family}_abstracts_full.txt
done 10< short_list_families.txt  #angiosperm_families.txt
```

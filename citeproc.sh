#!/bin/bash

# source bibliography
bibfn=$HOME/ccnlab_bib/ccnlab.bib

# mdcites is https://github.com/ccnlab/mdcites
# python version was waaaay tooo slow..
mdcites -bib=$bibfn -dir=book/ -out=book/references.bib 

cd book
pandoc-citeproc --format="American Psychological Association 6th edition" --bib2yaml references.bib > references.yaml

# need to remove the header from this for inclusion in metadata.yaml
tail -n +2 references.yaml > r.tmp
mv r.tmp references.yaml



# Description
A simple script that takes the entries of a BibTeX file and writes them into a CSV. If the specified CSV file exists only new entries in the BibTex will be updated.
This is useful when adding own information in the CSV that should not be overwritten.

# Installation
This project uses `pybtex`.
To run the file please install it via `conda install -c pybtex` or `pip install pybtex`.

# How to
`python convert.py <path to bib file> [-dl <Delimiter for CSV import>] [-o <path to csv file>] [-rf <field to remove> ...]`

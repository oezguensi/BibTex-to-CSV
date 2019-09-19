import sys
import csv
from pybtex.database.input import bibtex

assert len(sys.argv) > 1, 'Please specify the .bib file to convert.'

parser = bibtex.Parser()
input_fn = sys.argv[1] + ('' if sys.argv[1].endswith('.bib') else '.bib')
bib_data = parser.parse_file(input_fn)

fields = set([item for sublist in 
  [entry.fields.keys() for entry in bib_data.entries.values()] 
  for item in sublist])

dicts = [{field: value.fields[field] if field in value.fields.keys() else None for field in fields} 
  for key, value in bib_data.entries.items()]

output_fn = sys.argv[2] + ('' if sys.argv[2].endswith('.csv') else '.csv') if len(sys.argv) > 2 else input_fn.replace('bib', 'csv')
with open(output_fn, 'w') as output_file:
  dict_writer = csv.DictWriter(output_file, fields)
	dict_writer.writeheader()
	dict_writer.writerows(dicts)

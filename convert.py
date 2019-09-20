import csv
import os
import argparse
from pybtex.database.input import bibtex

parser = argparse.ArgumentParser()
parser.add_argument('path', help='Define the path of the BibTex file to convert.')
parser.add_argument('-out', help='Define the path of the CSV the data gets outputted to.', required=False)
parser.add_argument('-rf', '--rm-fields', nargs='*', help='Specify fields to remove from the output file.', required=False)
args = parser.parse_args()

parser = bibtex.Parser()

bib_data = parser.parse_file(args.path)

fields_to_remove = args.rm_fields if args.rm_fields else []

output_fn = args.out + ('' if args.out.endswith('.csv') else '.csv') if args.out else args.path.replace('bib', 'csv')

csv_fields = []
csv_data = []
if os.path.exists(output_fn):
	with open(output_fn) as csvfile:
		csv_data.extend(list(csv.DictReader(csvfile, delimiter=';')))
		csv_fields.extend([item for sublist in [row.keys() for row in csv_data] for item in sublist])

csv_ids = [value['id'] for value in csv_data]
fields = list(filter(lambda x: x not in fields_to_remove,
					 set([item for sublist in
						  [value.fields.keys() for value in bib_data.entries.values()]
						  for item in sublist] + csv_fields + ['id', 'type', 'authors'])))

rows = []
for key, value in bib_data.entries.items():
	if value.key not in csv_ids:
		row = {}
		for field in fields:
			if field == 'id':
				row[field] = value.key
			elif field == 'type':
				row[field] = value.type
			elif field == 'authors':
				row[field] = ', '.join([' '.join(list(filter(None, [' '.join(person.get_part(part)) for part in ['first', 'middle', 'last']])))
										 for person in value.persons['author']])
			else:
				row[field] = value.fields[field] if field in value.fields.keys() else None
		
		rows.append(row)

rows.extend([{field: value[field] if field in value.keys() else None for field in fields} for value in csv_data])

with open(output_fn, 'w') as output_file:
	dict_writer = csv.DictWriter(output_file, rows[0].keys())
	dict_writer.writeheader()
	dict_writer.writerows(rows)

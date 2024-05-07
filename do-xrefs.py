import os
import csv
import re

import networkx
import pandas

import do_tools

path = os.path.join('doid.obo')
do = do_tools.load_do(path)
dox = do_tools.do_to_networkx(do)

# Create a table of descriptions
pattern = re.compile(r'^"(.*?)"')
rows = list()
for term in dox:
    match = pattern.search(term.definition)
    description = match.group(1) if match else ''
    rows.append((term.id, term.name, description))
description_df = pandas.DataFrame(rows, columns = ['disease_id', 'name', 'description']).sort_values('disease_id')
##description_df.to_csv('Inferenced_data/description.tsv', sep='\t', index=False)
print(description_df.head(2))


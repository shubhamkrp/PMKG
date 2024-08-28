import os
import csv
import pandas as pd

relation_dir = 'relationships'

dc=[]
dis = set()
for symp_dir in os.listdir(relation_dir):
    symp_dir_path = os.path.join(relation_dir, symp_dir)
    # print(symp_dir_path)
    if os.path.isdir(symp_dir_path):
        term_file = os.path.join(symp_dir_path, f'{symp_dir}_disease.csv')
        # print(term_file)
        term = " ".join(symp_dir.split('_'))
        try:
            df = pd.read_csv(term_file)
            disease_count = len(df)-1
            # for row in df:
            #     dis.add(row['disease_term'].lower())
            # dis_df = df['disease_term']
            # dis.add()
        except:
            disease_count = 0
        dc.append(disease_count)

print(sum(dc)//len(dc))
print(len(dis))      
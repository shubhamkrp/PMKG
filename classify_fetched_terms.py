import pandas as pd
from similarity_bw_pubmed_do import similar

symptom_file="OUTPUT/active_symptom_terms.csv"
disease_file="OUTPUT/active_disease_terms.csv"
fetched_file="OUTPUT/fetched_terms_for_so.csv"

symptom_df=pd.read_csv(symptom_file)
disease_df=pd.read_csv(disease_file)
fetched_df=pd.read_csv(fetched_file)


column_name="Name"
symptom_column=symptom_df[column_name]
disease_column=disease_df[column_name]
# print(symptom_column.head())

related_symptoms={}
related_diseases={}
other_terms={}

for _,row in fetched_df.iterrows():
    # print(row)
    symptom=row["Symptom"]
    related_terms=row["Related terms"].split(";")
    # print(related_terms)
    
    #list of related symptoms
    symptom_list=[]
    disease_list=[]
    other_related_terms=[]

    for term in related_terms:
        s=0
        d=0
        for symp in symptom_column:
            if(term.lower()==symp):#if(similar(term.lower(),symp)):
                s=1
                symptom_list.append(symp)
        for dis in disease_column:
            if(term.lower()==dis):#if(similar(term.lower(),dis)):
                d=1
                disease_list.append(dis)
        if(s==0 and d==0):
            other_related_terms.append(term)
    related_diseases.update({symptom:disease_list})
    related_symptoms.update({symptom:symptom_list})
    other_terms.update({symptom:other_related_terms})

# print(related_symptoms)

import json

with open('OUTPUT/related_symptoms.json', 'w') as fp:
    fp.write(json.dumps(related_symptoms,indent=4))

with open('OUTPUT/related_diseases.json', 'w') as fp:
    fp.write(json.dumps(related_diseases,indent=4))

with open('OUTPUT/other_related_terms.json', 'w') as fp:
    fp.write(json.dumps(other_terms,indent=4))
Datasets
Symptom Data:
Two sources: 
1) MeSh Vocabulary (423 terms) - [C23.888] Signs and Symptoms branch in MeSH
https://meshb.nlm.nih.gov/treeView
2) Symptom Ontology (893 active* terms)
https://github.com/DiseaseOntology/SymptomOntology/blob/main/src/ontology/symp.obo
*The active terms in symptom ontology are the terms which have an “is_a” attribute.

Disease Data:
Consider all the 13,109 disease terms ([C] branch of MeSH) from MeSH vocabulary.
https://meshb.nlm.nih.gov/treeView

ICD9_CM data:
Total of 14,567 disease codes in ICD9_CM dataset (vol1 and vol2).
http://www.icd9data.com/2015/Volume1/default.htm

ICD10_CM data:
Total of 72,183 disease codes in ICD9_CM dataset.
https://www.icd10data.com/ICD10CM/Codes



Implementation

1. Symptom data collection 

From symptom ontology (get_active_terms.py)
Input - symp.obo from (symptom ontology github: https://github.com/DiseaseOntology/SymptomOntology/blob/main/src/ontology/symp.obo)

Output - .csv file containing active symptom terms

Usage - 
#########---------USAGE-----------#############
#get_active_term_name.py [-h] [--output_dir OUTPUT_DIR] input_file output_file
#python3 ./get_active_term_name.py --output_dir OUTPUT/ symp.obo active_symptom_terms.csv
###############################################

From MeSH vocabulary (get_branch_mesh_tree.py)
Input - MeSH vocabulary ('desc2024.xml') and branch_id to be extracted.

Output - .csv file containing id and name as columns

Usage - 
# Set the branch ID prefix
branch_id = ‘C23.888’
...
#python3 ./get_branch_mesh_tree.py

Downloading all PubMed articles using python script.
Input - NONE

Output - medline_data/all_the_PubMed_data_in_XML

Usage - 
#python3 ./extract_pubmed_articles_ftp.py

2. Extract the associated MeSH terms from PubMed using NCBI’s e-utilities Entrez API from PubMed Medline for each of the symptom terms obtained in the previous phase.

Related MeSH term extraction and their related articles.
Input - mesh_symptoms.csv and active_symptom_terms.csv

Output - Two files containing related MeSH terms and 
the related articles with following format:
37612654,"dry mouth in patients with a life-limiting condition or frailty: a study protocol for two intervention studies and a nested qualitative sub-study (the dry mouth project, drop).","despite its prevalent and impactful nature, dry mouth remains an underexposed and undertreated symptom in patients with a life-limiting condition or frailty. the main contributing factors are a lack of awareness and knowledge amongst both healthcare professionals and patients, and a scarcity of effective, evidence-based interventions. in the dry mouth project (drop), we address these factors by investigating both a non-pharmacological and a pharmacological intervention: a nurse-led patient education program and locally applied pilocarpine.",https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10463805/


Usage - 
Change the file input based on the symptom data source.
symp_file="mesh_symptoms.csv"

#python3 ./new_mining.py

This is a computationally expensive task and may take around 6-8 hours to execute depending on the terms in the datasource file and compute resource.

Unweighted Graph experiment
To get the related MeSH terms from PubMed related to each symptom from MeSH vocab and symptom ontology.

Input - Two .csv files namely, mesh_symptom.csv and active_symptom_terms.csv

Output - .csv files containing symptoms and their related MeSH terms. It also outputs the terms which could not fetch any MeSH terms from PubMed.
"symptom_with_no_terms.csv" and ”fetched_terms_for_mesh_symptoms.csv”

Usage - 
#python3 ./pubmedQuery.py


3. Overlap of obtained MeSH terms with ‘C’ branch to extract disease entities from MeSH.

To extract all MeSH disease terms.
Input - MeSH vocabulary ('desc2024.xml') and branch_id to be extracted.

Output - .csv file containing id and name as columns

Usage - 
# Set the branch ID prefix for diseases (e.g., 'C' for all diseases)
branch_id = ‘C’
...
#change file name accordingly
with open('mesh_disease_terms.csv', 'a', newline='', encoding='utf-8') as csvfile:


#python3 ./get_branch_mesh_tree.py

Fetching disease terms from obtained MeSH terms.
Input - .csv file containing the MeSH disease terms in C branch (mesh_disease_terms.csv) and the folder containing articles related to each symptom.

Output - .csv file containing the overlapped disease terms for each symptom in their respective folder with name {symp_dir}_disease.csv

Usage - 
#python3 ./exact_mesh_match.py


4. Get the associated count of each symptom with their related disease term in the automatically fetched PubMed articles which are saved in the step2.

Input - A directory containing the symptoms as folder, within each symptom folder contains a .csv file ({symp_dir}_disease.csv) with their related disease MeSH terms.
Another .csv file with the associated PubMed articles, namely ({symp_dir}_articles.csv)

Output - .txt file ({symp_dir}_count.txt) that contains the positive and negative co-occurrences of the symptoms and their associated diseases.

Usage - 
#python3 ./relation_cooccurrence.py


5. ICD9_CM mapping of the MeSH disease terms.
To map the ICD9 codes from english text, vector indexing is used. Firstly all the ICD9 codes are indexed in a vector database using FAISS and BioBERT. Then the disease term in English text is vectorized and mapped to the nearest ICD9 vector in terms of L2 distance within the vector space. 
 
ICD9 indexing:

Input - ICD9_CM codes as .txt file ('icd9_cm_codes.txt')

Output - FAISS index ('faiss_index_icd9.bin')

Usage - 
#python3 ./icd9_vector_db.py

For each symptom, mapping of disease terms to ICD9_CM codes and saving it as json.

Input - saved disease terms for each symptom.

Output - .json file ('mapped_terms_icd9.json') containing symptoms as key and value as diseases and their positive co-occurrence count.

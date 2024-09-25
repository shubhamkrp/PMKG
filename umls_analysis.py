# import pandas as pd

# df = pd.read_csv("mesh_disease_terms.csv")
# df_disease = df['Disease Name'] #.apply(str.lower)

# df_unique = df_disease.drop_duplicates()
# print(df_unique.head())
# print(len(df_unique)) #output 5032 unique disease terms from C branch



# import pandas as pd

# df = pd.read_csv("umls_terms_T047.csv")
# df_disease = df['cui'] #.apply(str.lower)

# df_unique = df_disease.drop_duplicates()
# print(df_unique.head())
# print(len(df_unique)) #output 118526 unique disease cui terms

# sdf = pd.read_csv("umls_terms_T184.csv")
# df_symptom =sdf['cui'] #.apply(str.lower)

# dfs_unique = df_symptom.drop_duplicates()
# print(dfs_unique.head())
# print(len(dfs_unique)) #output 14028 unique symptom cui terms

# dfs_unique.to_csv("umls_symptom_unique.csv", sep='\t', encoding='utf-8', index=False, header=False)
# df_unique.to_csv("umls_disease_unique.csv", sep='\t', encoding='utf-8', index=False, header=False)




# import csv
# import json

# # Load terms from CSV
# def load_terms_from_csv(file_path):
#     terms = {}
#     with open(file_path, 'r', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             term = row['term'].lower()  # Convert term to lowercase for case-insensitive comparison
#             cui = row['cui']
#             if term not in terms:
#                 terms[term] = set()
#             terms[term].add(cui)
#     return terms

# # Find overlapping terms
# def find_overlapping_terms(terms_T184, terms_T047):
#     overlapping_terms = {}
#     for term in terms_T184:
#         if term in terms_T047:
#             overlapping_terms[term] = {
#                 'cui_T184': list(terms_T184[term]),
#                 'cui_T047': list(terms_T047[term])
#             }
#     return overlapping_terms

# # Save overlapping terms as JSON
# def save_as_json(data, filename):
#     with open(filename, 'w', encoding='utf-8') as jsonfile:
#         json.dump(data, jsonfile, ensure_ascii=False, indent=2)

# # Main execution
# T184_FILE = "umls_terms_T184.csv"
# T047_FILE = "umls_terms_T047.csv"

# print("Loading terms for T184 (Signs or Symptoms)...")
# terms_T184 = load_terms_from_csv(T184_FILE)

# print("Loading terms for T047 (Diseases or Syndromes)...")
# terms_T047 = load_terms_from_csv(T047_FILE)

# print("Finding overlapping terms...")
# overlapping_terms = find_overlapping_terms(terms_T184, terms_T047)

# print(f"Found {len(overlapping_terms)} overlapping terms.")

# print("Saving overlapping terms as JSON...")
# save_as_json(overlapping_terms, "overlapping_terms_T184_T047.json")

# print("Overlap extraction complete. File saved as overlapping_terms_T184_T047.json.")

# import json
# import csv

# # Read JSON data from file
# json_file_path = 'overlapping_terms_T184_T047.json'  # Replace with your JSON file path
# with open(json_file_path, 'r') as json_file:
#     json_data = json.load(json_file)

# # Extract the keys (terms) from the JSON data
# terms = list(json_data.keys())

# # Write to CSV
# csv_file_path = 'overlapping_terms_T184_T047.csv'
# with open(csv_file_path, 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['term'])  # Write the header
#     for term in terms:
#         writer.writerow([term])

# print(f"CSV file '{csv_file_path}' has been created.")


# ########mesh and umls overlap
# import pandas as pd

# # Load MeSH terms from CSV
# def load_mesh_terms(csv_file):
#     mesh_df = pd.read_csv(csv_file)
#     print(mesh_df['Mesh terms'].head().apply(str.lower).tolist())
#     return mesh_df['Mesh terms'].apply(str.lower).tolist()

# # Load UMLS terms (symptom or disease) from CSV
# def load_umls_terms(csv_file):
#     umls_df = pd.read_csv(csv_file)
#     print(umls_df['term'].head().apply(str.lower).tolist())
#     return umls_df['term'].apply(str.lower).tolist()

# # Check overlap between MeSH and UMLS terms
# def compare_mesh_umls(mesh_terms, umls_terms):
#     overlap = set(mesh_terms).intersection(set(umls_terms))
#     return list(overlap)

# # Main workflow
# mesh_csv_file = 'cleaned_mesh_terms.csv'  # Path to MeSH CSV
# umls_symptom_csv = 'umls_terms_T184.csv'  # Path to UMLS symptom CSV (T184)
# umls_disease_csv = 'umls_terms_T047.csv'  # Path to UMLS disease CSV (T047)

# # Load the terms
# mesh_terms = load_mesh_terms(mesh_csv_file)
# umls_symptom_terms = load_umls_terms(umls_symptom_csv)
# umls_disease_terms = load_umls_terms(umls_disease_csv)

# # Compare MeSH terms with UMLS symptoms and diseases
# symptom_overlap = compare_mesh_umls(mesh_terms, umls_symptom_terms)
# disease_overlap = compare_mesh_umls(mesh_terms, umls_disease_terms)

# # Save the overlap results to CSV
# pd.DataFrame(symptom_overlap, columns=['Symptom Overlap']).to_csv('umls_symptom_overlap.csv', index=False)
# pd.DataFrame(disease_overlap, columns=['Disease Overlap']).to_csv('umls_disease_overlap.csv', index=False)

# print(f"Symptom overlap saved to 'umls_symptom_overlap.csv'")
# print(f"Disease overlap saved to 'umls_disease_overlap.csv'")




import csv
from collections import defaultdict

def read_csv(file_path, term_column):
    terms = set()
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            terms.add(row[term_column].lower())
    return terms

def compare_terms(mesh_terms, umls_disease_terms, umls_symptom_terms):
    all_umls_terms = umls_disease_terms.union(umls_symptom_terms)
    
    overlapping = mesh_terms.intersection(all_umls_terms)
    only_in_mesh = mesh_terms - all_umls_terms
    only_in_umls = all_umls_terms - mesh_terms
    
    umls_source = defaultdict(set)
    for term in all_umls_terms:
        if term in umls_disease_terms:
            umls_source[term].add('disease')
        if term in umls_symptom_terms:
            umls_source[term].add('symptom')
    
    return overlapping, only_in_mesh, only_in_umls, umls_source

def write_results(file_path, terms, header):
    with open(file_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([header])
        for term in sorted(terms):
            writer.writerow([term])

def write_umls_results(file_path, terms, umls_source):
    with open(file_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Term', 'UMLS Source'])
        for term in sorted(terms):
            writer.writerow([term, ', '.join(sorted(umls_source[term]))])

# File paths
mesh_file = 'mesh_disease_terms.csv'
umls_disease_file = 'umls_terms_T047.csv'
umls_symptom_file = 'umls_terms_T184.csv'

# Column names containing the terms in each file
mesh_column = 'Disease Name'  # replace with actual column name
umls_disease_column = 'term'  # replace with actual column name
umls_symptom_column = 'term'  # replace with actual column name

# Read terms
mesh_terms = read_csv(mesh_file, mesh_column)
umls_disease_terms = read_csv(umls_disease_file, umls_disease_column)
umls_symptom_terms = read_csv(umls_symptom_file, umls_symptom_column)

# Compare terms
overlapping, only_in_mesh, only_in_umls, umls_source = compare_terms(mesh_terms, umls_disease_terms, umls_symptom_terms)

# Write results
write_results('1overlapping_terms.csv', overlapping, 'Overlapping Terms')
write_results('2only_in_mesh.csv', only_in_mesh, 'Terms Only in MeSH')
write_umls_results('3only_in_umls.csv', only_in_umls, umls_source)

print(f"Total MeSH terms: {len(mesh_terms)}")
print(f"Total UMLS terms: {len(umls_disease_terms) + len(umls_symptom_terms)}")
print(f"Overlapping terms: {len(overlapping)}")
print(f"Terms only in MeSH: {len(only_in_mesh)}")
print(f"Terms only in UMLS: {len(only_in_umls)}")
print("Results have been written to CSV files.")


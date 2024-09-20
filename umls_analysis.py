import pandas as pd

df = pd.read_csv("umls_terms_T047.csv")
df_disease = df['cui'] #.apply(str.lower)

df_unique = df_disease.drop_duplicates()
print(df_unique.head())
print(len(df_unique)) #output 118526 unique disease cui terms

sdf = pd.read_csv("umls_terms_T184.csv")
df_symptom =sdf['cui'] #.apply(str.lower)

dfs_unique = df_symptom.drop_duplicates()
print(dfs_unique.head())
print(len(dfs_unique)) #output 14028 unique symptom cui terms







import csv
import json

# Load terms from CSV
def load_terms_from_csv(file_path):
    terms = {}
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            term = row['term'].lower()  # Convert term to lowercase for case-insensitive comparison
            cui = row['cui']
            if term not in terms:
                terms[term] = set()
            terms[term].add(cui)
    return terms

# Find overlapping terms
def find_overlapping_terms(terms_T184, terms_T047):
    overlapping_terms = {}
    for term in terms_T184:
        if term in terms_T047:
            overlapping_terms[term] = {
                'cui_T184': list(terms_T184[term]),
                'cui_T047': list(terms_T047[term])
            }
    return overlapping_terms

# Save overlapping terms as JSON
def save_as_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=2)

# Main execution
T184_FILE = "umls_terms_T184.csv"
T047_FILE = "umls_terms_T047.csv"

print("Loading terms for T184 (Signs or Symptoms)...")
terms_T184 = load_terms_from_csv(T184_FILE)

print("Loading terms for T047 (Diseases or Syndromes)...")
terms_T047 = load_terms_from_csv(T047_FILE)

print("Finding overlapping terms...")
overlapping_terms = find_overlapping_terms(terms_T184, terms_T047)

print(f"Found {len(overlapping_terms)} overlapping terms.")

print("Saving overlapping terms as JSON...")
save_as_json(overlapping_terms, "overlapping_terms_T184_T047.json")

print("Overlap extraction complete. File saved as overlapping_terms_T184_T047.json.")

import json
import csv

# Read JSON data from file
json_file_path = 'overlapping_terms_T184_T047.json'  # Replace with your JSON file path
with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)

# Extract the keys (terms) from the JSON data
terms = list(json_data.keys())

# Write to CSV
csv_file_path = 'overlapping_terms_T184_T047.csv'
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['term'])  # Write the header
    for term in terms:
        writer.writerow([term])

print(f"CSV file '{csv_file_path}' has been created.")


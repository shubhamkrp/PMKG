import csv
import json
from tqdm import tqdm

# File paths - UMLS files
MRCONSO_FILE = "/mnt/0C6C8FC06C8FA2D6/umls-2024AA-metathesaurus-full/2024AA/META/MRCONSO.RRF"
MRSTY_FILE = "/mnt/0C6C8FC06C8FA2D6/umls-2024AA-metathesaurus-full/2024AA/META/MRSTY.RRF"

def load_semantic_types(file_path, target_types):
    semantic_types = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('|')
            cui = parts[0]
            sty = parts[1]
            if sty in target_types:
                if cui not in semantic_types:
                    semantic_types[cui] = set()
                semantic_types[cui].add(sty)
    return semantic_types

def extract_terms(mrconso_file, semantic_types):
    terms = []
    with open(mrconso_file, 'r') as file:
        for line in tqdm(file, desc="Extracting terms"):
            parts = line.strip().split('|')
            cui = parts[0]
            lang = parts[1]
            term = parts[14]
            
            if cui in semantic_types and lang == 'ENG':
                for sty in semantic_types[cui]:
                    terms.append({
                        "cui": cui,
                        "term": term,
                        "semantic_type": sty
                    })
    return terms

def save_as_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['cui', 'term', 'semantic_type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def save_as_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=2)

# Main execution
print("Loading semantic types...")
target_types = {"T184", "T047"}  # T184: Sign or Symptom, T047: Disease or Syndrome
semantic_types = load_semantic_types(MRSTY_FILE, target_types)

print("Extracting terms...")
all_terms = extract_terms(MRCONSO_FILE, semantic_types)

# Filter terms by semantic type 
terms_T184 = [term for term in all_terms if term['semantic_type'] == 'T184']
terms_T047 = [term for term in all_terms if term['semantic_type'] == 'T047'] 
print("Saving T184 (Signs or Symptoms) as CSV and JSON...") 
save_as_csv(terms_T184, "umls_terms_T184.csv") 
save_as_json(terms_T184, "umls_terms_T184.json") 
print("Saving T047 (Diseases or Syndromes) as CSV and JSON...") 
save_as_csv(terms_T047, "umls_terms_T047.csv") 
save_as_json(terms_T047, "umls_terms_T047.json")

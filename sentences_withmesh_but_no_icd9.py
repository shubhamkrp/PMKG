import csv
import re

# Helper function to tokenize sentences
def sentence_tokenizer(text):
    # Basic sentence tokenizer using regex (you can use more sophisticated libraries like nltk or spacy if needed)
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    return sentences

# Helper function to check if any term is in a sentence
def contains_term(sentence, terms):
    for term in terms:
        if term.lower() in sentence.lower():
            return term
    return None

# Load disease MeSH terms
def load_mesh_terms(mesh_file):
    mesh_terms = []
    with open(mesh_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mesh_terms.append(row['Disease Name'].strip())
    return mesh_terms

# Load ICD-9 terms
def load_icd9_terms(icd9_file):
    icd9_terms = []
    with open(icd9_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            icd9_terms.append(row['Description'].strip())
    return icd9_terms

# Process PubMed articles to find sentences with MeSH terms but without ICD-9 codes
def find_sentences_without_icd9(pubmed_file, mesh_terms, icd9_terms, output_file):
    with open(pubmed_file, 'r') as f_in, open(output_file, 'w', newline='') as f_out:
        reader = csv.DictReader(f_in)
        writer = csv.writer(f_out)
        writer.writerow(['PMID', 'Sentence', 'MeSH Term Found', 'Title/Abstract'])

        for row in reader:
            pmid = row['PMID']
            title = row['Title']
            abstract = row['Abstract']
            
            # Tokenize title and abstract into sentences
            sentences = sentence_tokenizer(title) + sentence_tokenizer(abstract)
            
            for sentence in sentences:
                # Check if the sentence contains a MeSH term
                mesh_term_found = contains_term(sentence, mesh_terms)
                if mesh_term_found:
                    # Check if the sentence contains an ICD-9 term
                    icd9_term_found = contains_term(sentence, icd9_terms)
                    if not icd9_term_found:  # MeSH term found but no ICD-9 term
                        writer.writerow([pmid, sentence, mesh_term_found, 'Title' if sentence in title else 'Abstract'])

# Input files
pubmed_file = 'pubmed_articles.csv'  # Input PubMed articles file
mesh_file = 'mesh_disease_terms.csv'  # Input MeSH terms file
icd9_file = 'icd9_cm_names.csv'  # Input ICD-9 terms file
output_file = 'sentences_without_icd9.csv'  # Output CSV file

# Load terms
mesh_terms = load_mesh_terms(mesh_file)
icd9_terms = load_icd9_terms(icd9_file)

# Find sentences with MeSH terms but without ICD-9 terms
find_sentences_without_icd9(pubmed_file, mesh_terms, icd9_terms, output_file)

print(f"Processing completed. Results saved to {output_file}")



# import pandas as pd
# from Bio import Entrez
# import re
# import time
# import csv

# # Set up email for Entrez
# Entrez.email = "your.email@example.com"

# # Load the CSV file and extract unique names
# csv_file = "mesh_terms.csv"
# df = pd.read_csv(csv_file)
# terms = df['Mesh terms'].drop_duplicates().tolist()

# # Define the search parameters
# start_date = "2023/12/30"
# end_date = "2023/12/31"
# query = "(2023/12/30[PDAT] : 2023/12/31[PDAT])"
# batch_size = 10000  # Number of articles to fetch per batch

# # Perform the search to get the list of all PubMed IDs
# def fetch_pubmed_ids(query):
#     handle = Entrez.esearch(db="pubmed", term=query, retmax=100000000, usehistory="y")
#     search_results = Entrez.read(handle)
#     handle.close()
#     return search_results['IdList']

# # Fetch details for each batch of articles
# def fetch_details(id_list):
#     ids = ",".join(id_list)
#     handle = Entrez.efetch(db="pubmed", id=ids, rettype="medline", retmode="text")
#     records = handle.read()
#     handle.close()
#     return records

# # Search sentences in the article text
# def find_sentences_with_terms(article_text, terms):
#     sentences_with_terms = []
#     sentences = re.split(r'[.!?]', article_text)
    
#     for sentence in sentences:
#         found_terms = [term for term in terms if re.search(r'\b' + re.escape(term) + r'\b', sentence)]
#         if len(found_terms) >= 2:
#             print("matched", found_terms)
#             sentences_with_terms.append(sentence.strip())
    
#     return sentences_with_terms

# # Main processing loop
# def process_pubmed_articles(terms, query, batch_size):
#     # Fetch all PubMed IDs
#     pubmed_ids = fetch_pubmed_ids(query)
    
#     # Open CSV file for writing
#     with open("matching_sentences.csv", "w", newline="") as csvfile:
#         csvwriter = csv.writer(csvfile)
#         csvwriter.writerow(["ArticleID", "Sentence"])  # Write header

#         # Process in batches
#         for start in range(0, len(pubmed_ids), batch_size):
#             end = min(len(pubmed_ids), start + batch_size)
#             batch_ids = pubmed_ids[start:end]
            
#             # Fetch article details
#             articles = fetch_details(batch_ids)
            
#             # Find sentences with matching terms
#             for article_id in batch_ids:
#                 matching_sentences = find_sentences_with_terms(articles, terms)
#                 for sentence in matching_sentences:
#                     csvwriter.writerow([article_id, sentence])

#             time.sleep(1)  # Rate limiting
    
#     print("Processing complete! Results saved in 'matching_sentences.csv'.")
# start_time = time.time()
# # Run the main processing function
# process_pubmed_articles(terms, query, batch_size)
# print("---Execution time %s seconds ---" % (time.time() - start_time))



import csv
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

# Ensure the necessary NLTK models are downloaded
nltk.download('punkt')

# Function to find MeSH terms in a sentence (O(1) lookup using set)
def find_mesh_terms(sentence, mesh_terms_set):
    # Tokenize the sentence into words
    words = set(word_tokenize(sentence.lower()))  # Tokenized words as a set
    found_terms = []
    
    # Check if any of the MeSH terms are present in the words
    for term in mesh_terms_set:
        term_tokens = set(word_tokenize(term.lower()))
        if term_tokens.issubset(words):
            found_terms.append(term)
    
    return found_terms

# Read MeSH terms from CSV file
def load_mesh_terms(mesh_csv_path):
    mesh_terms_set = set()
    with open(mesh_csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            mesh_terms_set.add(row['Mesh terms'])
    return mesh_terms_set

# Process the PubMed data CSV file
def process_pubmed_data(pubmed_csv_path, mesh_terms_set, output_csv_path):
    with open(pubmed_csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        with open(output_csv_path, mode='w', newline='', encoding='utf-8') as output_file:
            fieldnames = ['PMID', 'Sentence', 'Found Terms']
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                pmid = row['PMID']
                title = row['Title']
                abstract = row['Abstract']

                # Split title and abstract into sentences
                sentences = sent_tokenize(title) + sent_tokenize(abstract)

                # Search for MeSH terms in each sentence
                for sentence in sentences:
                    found_terms = find_mesh_terms(sentence, mesh_terms_set)
                    if len(found_terms) >= 2:  # If two or more MeSH terms are found
                        writer.writerow({'PMID': pmid, 'Sentence': sentence, 'Found Terms': ', '.join(found_terms)})

# File paths
pubmed_csv_path = 'pubmed_articles.csv'  # PubMed CSV file
mesh_csv_path = 'cleaned_mesh_terms.csv'     # MeSH terms CSV file
output_csv_path = 'output_sentences_with_mesh.csv'  # Output file

# Load MeSH terms and process PubMed data
mesh_terms_set = load_mesh_terms(mesh_csv_path)
process_pubmed_data(pubmed_csv_path, mesh_terms_set, output_csv_path)

print("Processing complete. Results saved to:", output_csv_path)




# import pandas as pd

# # Load the CSV
# mesh_df = pd.read_csv('mesh_terms.csv')

# # Drop duplicates based on 'Mesh terms' column
# mesh_df = mesh_df.drop_duplicates(subset='Mesh terms')

# # Save the unique MeSH terms in a list
# mesh_terms = mesh_df['Mesh terms'].unique()

# # Optionally, save the cleaned CSV file
# mesh_df.to_csv('cleaned_mesh_terms.csv', index=False)



import pandas as pd
from Bio import Entrez
import re
import time
import csv

# Set up email for Entrez
Entrez.email = "your.email@example.com"

# Load the CSV file and extract unique names
csv_file = "mesh_terms.csv"
df = pd.read_csv(csv_file)
terms = df['Mesh terms'].drop_duplicates().tolist()

import os
import pandas as pd
import re

# Function to check if a sentence contains two or more unique MeSH terms
def contains_two_or_more_mesh_terms(sentence, mesh_terms):
    found_terms = [term for term in mesh_terms if term in sentence]
    return len(set(found_terms)) >= 2

# Directory to store month-wise CSV files
output_dir = "pubmed_sentences_monthwise"
os.makedirs(output_dir, exist_ok=True)

# Sample loop to iterate over months (e.g., Jan 1970 to Dec 2023)
for year in range(1970, 2024):
    for month in range(1, 13):
        # Simulate fetching articles for a given month (you need to implement this)
        articles = fetch_pubmed_articles(year, month)
        
        # Store results in a list of dictionaries for CSV export
        results = []

        for article in articles:
            pubmed_id = article['pubmed_id']  # Extract PubMed ID (you need to implement this)
            text = article['text']  # Extract text from the article (you need to implement this)
            
            # Split text into sentences
            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

            for sentence in sentences:
                # Check if the sentence contains two or more unique MeSH terms
                if contains_two_or_more_mesh_terms(sentence, mesh_terms):
                    results.append({
                        'pubmed_id': pubmed_id,
                        'sentence': sentence,
                    })

        # Save the results to a CSV file for the given month
        if results:
            df = pd.DataFrame(results)
            month_str = f"{year}_{month:02d}"
            df.to_csv(os.path.join(output_dir, f"pubmed_sentences_{month_str}.csv"), index=False)


# # Define the search parameters
# start_date = "2023/12/20"
# end_date = "2023/12/31"
# query = "(2023/12/20[PDAT] : 2023/12/31[PDAT])"
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
#         words = set(l.lower() for l in sentence)
#         if terms.lower() in words:
#             sentences_with_terms.append(sentence.strip())
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



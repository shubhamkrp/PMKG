# import pandas as pd
# from Bio import Entrez
# import time
# import csv
# from xml.etree import ElementTree as ET

# # Set up email for Entrez
# Entrez.email = "your.email@example.com"

# # Define the search parameters
# start_date = "2023/12/01"
# end_date = "2023/12/31"
# query = "(2023/12/01[PDAT] : 2023/12/31[PDAT])"
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
#     handle = Entrez.efetch(db="pubmed", id=ids, rettype="xml", retmode="text")
#     records = handle.read()
#     handle.close()
#     return records

# # Extract article details (ID, title, abstract)
# def extract_article_details(records):
#     root = ET.fromstring(records)
#     articles = []
    
#     for article in root.findall('.//PubmedArticle'):
#         article_id = article.find('.//PMID').text
#         title_elem = article.find('.//ArticleTitle')
#         abstract_elem = article.find('.//Abstract/AbstractText')

#         title = title_elem.text if title_elem is not None else "No Title"
#         abstract = abstract_elem.text if abstract_elem is not None else "No Abstract"
        
#         articles.append({
#             "PMID": article_id,
#             "Title": title,
#             "Abstract": abstract
#         })
    
#     return articles

# # Main processing loop
# def process_pubmed_articles(query, batch_size):
#     # Fetch all PubMed IDs
#     pubmed_ids = fetch_pubmed_ids(query)
    
#     # Open CSV file for writing
#     with open("pubmed_articles.csv", "w", newline="", encoding='utf-8') as csvfile:
#         csvwriter = csv.DictWriter(csvfile, fieldnames=["PMID", "Title", "Abstract"])
#         csvwriter.writeheader()

#         # Process in batches
#         for start in range(0, len(pubmed_ids), batch_size):
#             end = min(len(pubmed_ids), start + batch_size)
#             batch_ids = pubmed_ids[start:end]
            
#             # Fetch article details
#             records = fetch_details(batch_ids)
            
#             # Extract article details
#             articles = extract_article_details(records)
            
#             # Write articles to CSV
#             csvwriter.writerows(articles)
            
#             print(f"Processed articles {start + 1} to {end}")
#             time.sleep(1)  # Rate limiting
    
#     print("Processing complete! Articles saved in 'pubmed_articles.csv'.")
# start_time = time.time()
# # Run the main processing function
# process_pubmed_articles(query, batch_size)
# print("---Execution time %s seconds ---" % (time.time() - start_time))


import pandas as pd
from Bio import Entrez
import time
import csv
from xml.etree import ElementTree as ET


Entrez.email="your.email@example.com"

# Define the search parameters
start_date = "2023/12/01"
end_date = "2023/12/31"
query = "(2023/12/01[PDAT] : 2023/12/31[PDAT])"
batch_size = 10000  # Number of articles to fetch per batch

# Perform the search to get the list of all PubMed IDs with history tracking
def fetch_pubmed_history(query):
    handle = Entrez.esearch(db="pubmed", term=query, retmax=100000000, usehistory="y")
    search_results = Entrez.read(handle)
    handle.close()
    return search_results['WebEnv'], search_results['QueryKey'], int(search_results['Count'])

# Fetch details for each batch of articles
def fetch_details(webenv, query_key, start, batch_size):
    handle = Entrez.efetch(db="pubmed", rettype="xml", retmode="text",
                           retstart=start, retmax=batch_size,
                           webenv=webenv, query_key=query_key)
    records = handle.read()
    handle.close()
    return records

# Extract article details (ID, title, abstract)
def extract_article_details(records):
    root = ET.fromstring(records)
    articles = []
    
    for article in root.findall('.//PubmedArticle'):
        article_id = article.find('.//PMID').text
        title_elem = article.find('.//ArticleTitle')
        abstract_elem = article.find('.//Abstract/AbstractText')

        title = title_elem.text if title_elem is not None else "No Title"
        abstract = abstract_elem.text if abstract_elem is not None else "No Abstract"
        
        articles.append({
            "PMID": article_id,
            "Title": title,
            "Abstract": abstract
        })
    
    return articles

# Main processing loop
def process_pubmed_articles(query, batch_size):
    # Fetch history information to allow batch processing
    webenv, query_key, total_count = fetch_pubmed_history(query)
    x=0
    # Open CSV file for writing
    with open("pubmed_articles.csv", "w", newline="", encoding='utf-8') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=["PMID", "Title", "Abstract"])
        csvwriter.writeheader()

        # Process in batches
        for start in range(0, total_count, batch_size):
            records = fetch_details(webenv, query_key, start, batch_size)
            
            # Extract article details
            articles = extract_article_details(records)
            
            # Write articles to CSV
            csvwriter.writerows(articles)
            
            print(f"Processed articles {start + 1} to {start + len(articles)} of {total_count}")
            time.sleep(10)  # Rate limiting
    
    print("Processing complete! Articles saved in 'pubmed_articles.csv'.")


start_time = time.time()
# Run the main processing function
process_pubmed_articles(query, batch_size)
print("---Execution time %s seconds ---" % (time.time() - start_time))

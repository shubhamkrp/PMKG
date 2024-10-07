

# from Bio import Entrez
# import csv, os

# # Function to search PubMed
# def search_pubmed(term, max_results=10):
#     Entrez.email = "youemail@example.com"
#     handle = Entrez.esearch(db="pubmed", term=term, retmax=max_results)
#     record = Entrez.read(handle)
#     handle.close()
#     return record["IdList"]

# # Function to fetch article details
# def fetch_details(id_list):
#     ids = ",".join(id_list)
#     handle = Entrez.efetch(db="pubmed", id=ids, retmode="xml")
#     records = Entrez.read(handle)
#     handle.close()
#     return records

# # Function to extract MeSH terms
# def extract_mesh_terms(records):
#     mesh_terms = set()
#     for record in records["PubmedArticle"]:
#         if "MeshHeadingList" in record["MedlineCitation"]:
#             for mesh_heading in record["MedlineCitation"]["MeshHeadingList"]:
#                 mesh_terms.add(mesh_heading["DescriptorName"])
#     return mesh_terms

# # Function to extract title, abstract, and full text link
# def extract_article_details(records):
#     articles = []
#     mesh_terms = set()
#     for record in records["PubmedArticle"]:
#         if "MeshHeadingList" in record["MedlineCitation"]:
#             for mesh_heading in record["MedlineCitation"]["MeshHeadingList"]:
#                 mesh_terms.add(mesh_heading["DescriptorName"].lower())
#         pubmed_id=record["MedlineCitation"]["PMID"]
#         article = record["MedlineCitation"]["Article"]
#         title = article.get("ArticleTitle", "No title available")
#         abstract = article.get("Abstract", {}).get("AbstractText", ["No abstract available"])[0]
#         full_text_link = None

#         # Try to find full text link from PubmedData
#         if "PubmedData" in record and "ArticleIdList" in record["PubmedData"]:
#             for article_id in record["PubmedData"]["ArticleIdList"]:
#                 if article_id.attributes["IdType"] == "pmc":
#                     full_text_link = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{article_id}/"

#         articles.append({
#             "pubmed_id": pubmed_id,
#             "title": title.lower(),
#             "abstract": abstract.lower(),
#             "full_text_link": full_text_link,
#         })
#     return mesh_terms, articles

# def save_to_csv(articles, filename):
#     keys=["pubmed_id", "title", "abstract", "full_text_link"]
#     with open(filename, 'w', newline='', encoding='utf-8') as output_file: 
#         dict_writer = csv.DictWriter(output_file, fieldnames=keys) 
#         dict_writer.writeheader() 
#         dict_writer.writerows(articles)


# import pandas as pd
# dis_file="Neurology.csv"
# dis_df=pd.read_csv(dis_file)
# dis_term=dis_df["Name"]
# # dis_term=dis_term.loc[321:330]
# print(dis_term.head())

# # term = "Prosopagnosia"
# for term in dis_term:
#     term=term.lower()
#     term=f'"{term}"'
#     ids = search_pubmed(term, max_results=999999)
#     details = fetch_details(ids)
#     mesh_terms, articles = extract_article_details(details)
#     print(len(mesh_terms))

#     print(len(articles))
#     term_name = "_".join(term.split(" "))

#     if not os.path.exists(term_name):
#         os.mkdir(term_name)

#     with open(os.path.join(term_name, f'{term_name}.txt'), 'w') as f:
#         f.write(f"{term}\n")
#         for line in mesh_terms:
#             f.write(f"{line.lower()}\n")

#     save_to_csv(articles, os.path.join(term_name, f'{term_name}_articles.csv'))





import os
import csv
from Bio import Entrez
import time

# Email for Entrez API
Entrez.email = "jayewi8873@craftapk.com"

# Function to fetch PubMed articles based on disease name with no limit
def fetch_all_pubmed_articles(disease_name):
    pmids = []
    retstart = 0
    batch_size = 100  # Number of articles to fetch in each batch

    # Fetch all results in batches until no more PMIDs are returned
    while True:
        handle = Entrez.esearch(db="pubmed", term=disease_name, retmax=9999999)
        record = Entrez.read(handle)
        handle.close()
        
        pmids_batch = record["IdList"]
        if not pmids_batch:
            break
        
        pmids.extend(pmids_batch)
        retstart += batch_size
        time.sleep(0.5)  # Pause to avoid overloading the API

    articles = []
    
    # Fetch details for all collected PMIDs
    for pmid in pmids:
        handle = Entrez.efetch(db="pubmed", id=pmid, retmode="xml") #, rettype="abstract"
        articles_data = Entrez.read(handle)
        handle.close()
        
        for article in articles_data["PubmedArticle"]:
            title = article["MedlineCitation"]["Article"]["ArticleTitle"]
            abstract = article["MedlineCitation"]["Article"].get("Abstract", {}).get("AbstractText", [""])[0]
            articles.append([pmid, title, abstract])
        
        time.sleep(0.5)  # Pause to avoid overloading the API

    return articles

# Create a folder for each disease and save related articles
def create_folders_and_save_articles(disease_name, articles):
    folder_name = disease_name.replace(" ", "_")
    os.makedirs(folder_name, exist_ok=True)
    
    with open(f"icd9_diseases/{folder_name}/related_articles.csv", mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["PMID", "Title", "Abstract"])
        writer.writerows(articles)

no_articles=[]
# Read diseases from Neurology.csv
def fetch_articles_for_diseases(csv_file):
    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            disease_name = row['Name']
            disease_search = f'"{disease_name}"  AND (1970/01/01[PDAT] : 2023/12/31[PDAT])'
            # disease_name=disease_name.loc[:5]
            print(f"Fetching articles for: {disease_name}")
            articles = fetch_all_pubmed_articles(disease_search)
            if articles:
                create_folders_and_save_articles(disease_name, articles)
            else:
                no_articles.append(disease_name)
                print(f"No articles found for: {disease_name}")

if __name__ == "__main__":
    fetch_articles_for_diseases("Neurology.csv")
    with open('diseases_with_no_articles.txt', 'w') as f:
        for disease in no_articles:
            f.write(f"{disease}\n")


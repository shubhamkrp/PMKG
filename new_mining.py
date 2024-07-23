# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# from similarity_bw_pubmed_do import similar


# # Define the base URL for the PubMed API
# PUBMED_API_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

# # Define the function to fetch disease terms related to the given symptom
# def fetch_terms(symptom):
#     # Replace spaces with '+' for URL encoding
#     symptom_query = symptom.replace(" ", "+")

#     # Construct the search query URL
#     search_url = f"{PUBMED_API_BASE_URL}esearch.fcgi?db=pubmed&term={symptom_query}[MeSH Terms]&retmax=99999"

#     # Send the request to PubMed API
#     response = requests.get(search_url)
#     response.raise_for_status()  # Raise an error if the request failed

#     soup = BeautifulSoup(response.content, 'xml')

#     # Extract the PubMed IDs (PMIDs) from the response
#     pmids = [id_tag.text for id_tag in soup.find_all('Id')]

#     # Initialize a set to store fetched terms
#     disease_terms = set()

#     # Fetch details for each PMID
#     for pmid in pmids:
#         # Construct the fetch details URL
#         fetch_url = f"{PUBMED_API_BASE_URL}efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"

#         # Send the request to PubMed API
#         fetch_response = requests.get(fetch_url)
#         fetch_response.raise_for_status()

#         # Parse the response XML
#         fetch_soup = BeautifulSoup(fetch_response.content, 'xml')

#         # Extract MeSH terms related to diseases
#         mesh_headings = fetch_soup.find_all('MeshHeading')
#         for mesh_heading in mesh_headings:
#             descriptor = mesh_heading.DescriptorName
#             if descriptor and descriptor.get('MajorTopicYN') == 'Y':
#                 disease_terms.add(descriptor.text)

#     return disease_terms


# symptom_file="mesh_symptoms.csv"
# symptom_df=pd.read_csv(symptom_file, delimiter=';')

# #select name column
# column_name="Name"
# symptom_term=symptom_df[column_name]

# symptom_term=symptom_term.loc[431:]
# print(symptom_term.head(2))


# # symptom_term=["fever", "joint pain", "night sweat", "cough", "vomiting"]
# # symptom_term=["joint pain"]

# COLUMN_NAMES=["Symptom", "Related terms"]
# df=pd.DataFrame(columns=COLUMN_NAMES)

# no_df=pd.DataFrame(columns=["Symptom with no terms"])

# for symptom in symptom_term:
#     terms = fetch_terms(symptom)
#     print(f"\nTerms associated with '{symptom}': {len(terms)}")
#     if(len(terms)==0):
#         no_df.loc[len(no_df)]=[symptom]
#         continue
#     term_string = ';'.join(terms)
#     df.loc[len(df)]=[symptom,term_string]




# terms = fetch_terms(symptom)
# print(f"\nTerms associated with '{symptom}': {len(terms)}")



# no_df.to_csv("OUTPUT/mesh_symptom_with_no_terms.csv", sep=",", mode='a', index=False, header=False)
# df.to_csv("OUTPUT/fetched_terms_for_mesh_symptoms.csv", sep=",", mode='a', index=False, header=False)

# from Bio import Entrez
# import json

# # Function to search PubMed
# def search_pubmed(term):
#     Entrez.email = "your-email@example.com"
#     handle = Entrez.esearch(db="pubmed", term=term, retmax=99999)
#     record = Entrez.read(handle)
#     handle.close()
#     return record["IdList"]

# # Function to fetch article details
# def fetch_details(id_list):
#     ids = ",".join(id_list)
#     handle = Entrez.efetch(db="pubmed", id=ids, retmode="xml")
#     records = Entrez.read(handle)
#     with open('zrecords.json', 'w') as json_file:
#         json.dump(records, json_file, indent=4)
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

# # Example usage
# term = "abdominal cramp"
# ids = search_pubmed(term)
# print(len(ids))
# details = fetch_details(ids)
# mesh_terms = extract_mesh_terms(details)
# print(len(details))
# # Print MeSH terms
# print(len(mesh_terms))
# # for term in mesh_terms:
# #     print(term)



from Bio import Entrez
import csv, os

# Function to search PubMed
def search_pubmed(term, max_results=10):
    Entrez.email = "your-email@example.com"
    handle = Entrez.esearch(db="pubmed", term=term, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]

# Function to fetch article details
def fetch_details(id_list):
    ids = ",".join(id_list)
    handle = Entrez.efetch(db="pubmed", id=ids, retmode="xml")
    records = Entrez.read(handle)
    handle.close()
    return records

# Function to extract MeSH terms
def extract_mesh_terms(records):
    mesh_terms = set()
    for record in records["PubmedArticle"]:
        if "MeshHeadingList" in record["MedlineCitation"]:
            for mesh_heading in record["MedlineCitation"]["MeshHeadingList"]:
                mesh_terms.add(mesh_heading["DescriptorName"])
    return mesh_terms

# Function to extract title, abstract, and full text link
def extract_article_details(records):
    articles = []
    mesh_terms = set()
    for record in records["PubmedArticle"]:
        if "MeshHeadingList" in record["MedlineCitation"]:
            for mesh_heading in record["MedlineCitation"]["MeshHeadingList"]:
                mesh_terms.add(mesh_heading["DescriptorName"].lower())
        pubmed_id=record["MedlineCitation"]["PMID"]
        article = record["MedlineCitation"]["Article"]
        title = article.get("ArticleTitle", "No title available")
        abstract = article.get("Abstract", {}).get("AbstractText", ["No abstract available"])[0]
        full_text_link = None

        # Try to find full text link from PubmedData
        if "PubmedData" in record and "ArticleIdList" in record["PubmedData"]:
            for article_id in record["PubmedData"]["ArticleIdList"]:
                if article_id.attributes["IdType"] == "pmc":
                    full_text_link = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{article_id}/"

        articles.append({
            "pubmed_id": pubmed_id,
            "title": title.lower(),
            "abstract": abstract.lower(),
            "full_text_link": full_text_link,
        })
    return mesh_terms, articles

def save_to_csv(articles, filename):
    keys=["pubmed_id", "title", "abstract", "full_text_link"]
    with open(filename, 'w', newline='', encoding='utf-8') as output_file: 
        dict_writer = csv.DictWriter(output_file, fieldnames=keys) 
        dict_writer.writeheader() 
        dict_writer.writerows(articles)

term = "Tardive Dyskinesia"
term=term.lower()
ids = search_pubmed(term, max_results=999999)
details = fetch_details(ids)
mesh_terms, articles = extract_article_details(details)
print(len(mesh_terms))

print(len(articles))
term_name = "_".join(term.split(" "))

if not os.path.exists(term_name):
    os.mkdir(term_name)

with open(os.path.join(term_name, f'{term_name}.txt'), 'w') as f:
    f.write(f"{term}\n")
    for line in mesh_terms:
        f.write(f"{line.lower()}\n")

save_to_csv(articles, os.path.join(term_name, f'{term_name}_articles.csv'))


from Bio import Entrez
import xmltodict
import json

# Function to fetch PubMed articles
def fetch_pubmed_articles(query, max_results=100):
    Entrez.email = "xiporo2675@noefa.com"
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    
    id_list = record["IdList"]
    articles = []

    for pubmed_id in id_list:
        handle = Entrez.efetch(db="pubmed", id=pubmed_id, rettype="xml")
        records = handle.read()
        handle.close()
        
        record_dict = xmltodict.parse(records)
        
        pubmed_article = record_dict.get('PubmedArticleSet', {}).get('PubmedArticle', {})
        
        if pubmed_article:
            articles.append(pubmed_article)
    
    return articles

articles = fetch_pubmed_articles("(guideline[title]) OR (guidelines[title])", max_results=20000000)

with open('pubmed_guideline_articles_all_attributes_all.json', 'w') as json_file:
    json.dump(articles, json_file, indent=4)

print("Articles saved to pubmed_guideline_articles_all_attributes_all.json")

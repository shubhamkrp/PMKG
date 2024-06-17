from Bio import Entrez
import json

def fetch_pubmed_articles(query, max_results=200):
    Entrez.email = "kumarshubham209@example.com"
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    
    id_list = record["IdList"]
    articles = []

    for pubmed_id in id_list:
        handle = Entrez.efetch(db="pubmed", id=pubmed_id, rettype="xml")
        records = Entrez.read(handle)
        handle.close()

        for article in records['PubmedArticle']:
            doi = None
            for article_id in article['PubmedData']['ArticleIdList']:
                if article_id.attributes['IdType'] == 'doi':
                    doi = article_id
                    break
            article_dict = {
                "PMID": article['MedlineCitation']['PMID'],
                "Title": article['MedlineCitation']['Article']['ArticleTitle'],
                "Abstract": article['MedlineCitation']['Article'].get('Abstract', {}).get('AbstractText', []),
                "Journal": article['MedlineCitation']['Article']['Journal']['Title'],
                "PublicationDate": article['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate'],
                "DOI": doi,
                "FullTextLink": f"https://doi.org/{doi}" if doi else None
            }
            articles.append(article_dict)
    
    return articles

articles = fetch_pubmed_articles("(guideline[title]) OR (guidelines[title])", max_results=20000000)

# Save articles to a JSON file
with open('pubmed_guideline_articles_all.json', 'w') as json_file:
    json.dump(articles, json_file, indent=4)

print("Articles saved to pubmed_guideline_articles_all.json")

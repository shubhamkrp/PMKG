from Bio import Entrez
import csv, os


# Function to search PubMed
def search_pubmed(term, max_results=10):
    Entrez.email = "yemail@example.com"
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


###############new_relation.py#################
import csv
import re
import os
from collections import defaultdict
import spacy
from negspacy.negation import Negex
from spacy.pipeline import Sentencizer


# Function to create pairs of the first term with all the other terms
def create_pairs(term, terms):
    pairs = [(term, terms[i]) for i in range(0, len(terms))]
    return pairs


# Function to detect if a pair is negatively related in a sentence using negex
def is_negative(sentence, term1, term2):
    doc = nlp(sentence)
    for entity in doc.ents:
        if entity.text.lower() == term1.lower() or entity.text.lower() == term2.lower():
            if entity._.negex:
                return True
    return False


# Function to search for pairs in titles and abstracts sentence-wise
def count_co_occurrences(pairs, articles):
    pair_counts = defaultdict(lambda: {'positive_count': 0, 'negative_count': 0})


    for article in articles:
        text = f"{article['title']} {article['abstract']}"
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)


        for sentence in sentences:
            for pair in pairs:
                term1, term2 = pair
                if re.search(r'\b' + re.escape(term1) + r'\b', sentence) and re.search(r'\b' + re.escape(term2) + r'\b', sentence):
                    if is_negative(sentence, term1, term2):
                        pair_counts[pair]['negative_count'] += 1
                    else:
                        pair_counts[pair]['positive_count'] += 1


    return pair_counts


import pandas as pd
import time
symp_file="mesh_symptoms.csv"
symp_df=pd.read_csv(symp_file, delimiter=';')
symp_term=symp_df["Name"]
symp_term=symp_term.loc[229:230]
print(symp_term.head())


for term in symp_term:
    term=term.lower()
    while True:
        try:
            ids = search_pubmed(term, max_results=999999)
        except ConnectionResetError:
            time.sleep(5)
            pass
        except RuntimeError:
            no_articles_term = open("terms_with_no_article.txt", "a")
            no_articles_term.write(f"{term}\n")
            no_articles_term.close()
            pass
        except ValueError:
            no_articles_term = open("terms_with_no_article.txt", "a")
            no_articles_term.write(f"{term}\n")
            no_articles_term.close()
            pass
        else:
            break
    details = fetch_details(ids)
    mesh_terms, articles = extract_article_details(details)
    print(len(mesh_terms))


    print(len(articles))
    term_name = "_".join(term.split(" "))


    # Initialize spaCy model with negex
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("negex", config={"ent_types": ["NOUN", "PROPN", "VERB", "ADJ"]})
    nlp.add_pipe("sentencizer")


    if not os.path.exists("relation"):
        os.mkdir("relation")
    # terms_filename = os.path.join(term_name, f'{term_name}.txt')
    # csv_filename = os.path.join(term_name, f'{term_name}_articles.csv')

    mesh_terms=list(mesh_terms)
    pairs = create_pairs(term, mesh_terms)

    # Count co-occurrences of pairs
    pair_counts = count_co_occurrences(pairs, articles)


    # Print the results
    # for pair, counts in pair_counts.items():
    #     print(f"Pair: {pair[0]} | {pair[1]}, Positive Count: {counts['positive_count']}, Negative Count: {counts['negative_count']}")


    with open(os.path.join("relation", f'{term_name}_relation_count.txt'), 'w') as count_file:
        for pair, counts in pair_counts.items():
            count_file.write(f"{pair[0]}, {pair[1]}, {counts['positive_count']}, {counts['negative_count']}\n")




# from pyserini.search import SimpleSearcher
import json
import os
import pandas as pd
from pyserini.search.lucene import LuceneSearcher

# Initialize searcher with the indexed data
index_dir = '/mnt/0C6C8FC06C8FA2D6/indexes/pubmed-index'
searcher = LuceneSearcher(index_dir)

# Set BM25 parameters (if needed)
searcher.set_bm25(k1=0.9, b=0.4)
bm25_threshold = 9.8

def search_disease(disease_name, k=10):
    hits = searcher.search(disease_name, k=k)
    results = []
    for i in range(len(hits)):
        if hits[i].score>=bm25_threshold:
            doc = searcher.doc(hits[i].docid).raw()
            results.append(json.loads(doc))
    return results

# Search for articles related to a specific disease
dis_file="Neurology.csv"
dis_df=pd.read_csv(dis_file, delimiter=';', on_bad_lines='skip')
dis_term=dis_df["Name"]
print(dis_term.head())

for disease in dis_term:
    # disease = 'Carotid sinus syndrome'
    print(disease)
    top_k = 3000
    results = search_disease(disease, k=top_k)
    
    if(len(results))==0:
        continue

    term_name = "_".join(disease.split(" "))
    with open(os.path.join("sparse_retrieval", f'{term_name}.json'), 'w') as fp:
        json.dump(results, fp, indent=4)


# # Display top results
# for result in results:
#     print(f"PMID: {result['id']}")
#     # print(f"Title: {result['contents'].split('.')[0]}")
#     print(f"Title&Abstract: {result['contents']}")
#     print()



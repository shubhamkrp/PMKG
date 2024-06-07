# from icdcodex import hierarchy

# import networkx as nx
# import matplotlib.pyplot as plt
# from networkx.drawing.nx_agraph import to_agraph

# # Get the ICD-10-CM hierarchy
# icd10_hierarchy = hierarchy.icd10cm()

# # Print the hierarchical tree
# print((icd10_hierarchy[0]))


# G=nx.DiGraph(icd10_hierarchy[0])
# nx.draw(G)
# plt.savefig("icd10.png")

# Convert to AGraph (Graphviz format)
# A = to_agraph(G)

# # Set graph attributes (optional)
# A.graph_attr.update(rankdir="LR")  # Left-to-right layout

# # Render the graph
# A.draw("large_graph.png", format="png", prog="dot")

# # Show the plot (optional)
# plt.imshow(plt.imread("large_graph.png"))
# plt.axis("off")
# plt.show()


# import simple_icd_10 as icd10
# all_codes=icd10.get_all_codes()
# print(all_codes[:15])


# Install required libraries if not already installed
# pip install sentence-transformers faiss-cpu

import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import re, json, time



# Step 1: Read ICD-10-CM Data from Text File
def read_icd10_cm_terms(file_path):
    icd10_terms = []
    with open(file_path, 'r') as file:
        for line in file:
            # Use regular expression to split on multiple spaces
            parts = re.split(r'\s{2,}', line.strip())
            if len(parts) == 2:
                code, name = parts
                icd10_terms.append(f"{code} - {name}")
    return icd10_terms

# Path to your text file
file_path = 'icd10cm_codes.txt'
icd10_terms = read_icd10_cm_terms(file_path)

# Step 2: Generate Embeddings
# Load pre-trained SBERT model
# model = SentenceTransformer('all-MiniLM-L6-v2')
model = SentenceTransformer('dmis-lab/biobert-base-cased-v1.1')

# Generate embeddings for ICD-10-CM terms
icd10_embeddings = model.encode(icd10_terms)

# Step 3: Set Up FAISS Vector Database
# Convert embeddings to a format suitable for FAISS
icd10_embeddings = np.array(icd10_embeddings).astype('float32')

# Create a FAISS index
index = faiss.IndexFlatL2(icd10_embeddings.shape[1])
index.add(icd10_embeddings)


# Step 4: Query the Database
def search_icd10(query, k=5):
    query_embedding = model.encode([query]).astype('float32')
    D, I = index.search(query_embedding, k)
    return [icd10_terms[i] for i in I[0]]

# Step 4: Batch Processing for Queries
def batch_search_icd10(query_terms, batch_size=100, k=5):
    results = []
    for i in range(0, len(query_terms), batch_size):
        batch_queries = query_terms[i:i + batch_size]
        batch_embeddings = model.encode(batch_queries).astype('float32')
        D, I = index.search(batch_embeddings, k)
        batch_results = [[icd10_terms[idx] for idx in indices] for indices in I]
        results.extend(batch_results)
    return results

#step5: load queries from other_related_terms.json
def load_queries_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Example JSON file path
json_file_path = 'OUTPUT/related_diseases.json'

# Load queries
queries_dict = load_queries_from_json(json_file_path)
print(queries_dict)

# Process all query terms in batches
start_time = time.time()


# Initialize results dictionary
results_dict = {}

# # Search and collect results for each query
# for category, queries in queries_dict.items():
#     category_results = {}
#     for query in queries:
#         results = search_icd10(query)
#         category_results[query] = results
#     results_dict[category] = category_results

# Search and collect results for each query
for category, queries in queries_dict.items():
    category_results = []
    for query in queries:
        results = search_icd10(query,k=1)
        category_results.extend(results)
    results_dict[category] = category_results

search_time = time.time() - start_time
# Step 6: Save results to JSON file
output_json_file_path = 'OUTPUT/disease_icd10_mapping.json'
with open(output_json_file_path, 'w') as outfile:
    json.dump(results_dict, outfile, indent=4)

print(f"Results saved to {output_json_file_path}")

# query_terms = ["Recurrence","Blindness","Quality of Life","Eye, Artificial","Feeding Behavior","Characidae","Corneal Diseases","Corneal Transplantation","Cornea","Prostheses and Implants","Autoimmune Diseases","Uveitis","Visual Acuity","Glaucoma","Intraocular Pressure","Quality of Life","Laser Therapy","Visually Impaired Persons","Touch","Hand Strength","Genetic Therapy","Blindness","CRISPR-Cas Systems","Gene Editing","Blindness","Deaf-Blind Disorders","Communication","Pan troglodytes","Ape Diseases","Mycobacterium tuberculosis","Blindness","Meningoencephalitis","Allergy and Immunology","Books","Art","Allergy and Immunology","Blindness, Cortical","Vertebroplasty","Retinitis Pigmentosa","Sexual Behavior","Blindness","Employment","Hemianopsia","Positron-Emission Tomography","Fluorodeoxyglucose F18","Visual Cortex","Glucose","Blindness","Magnetic Resonance Imaging","Entorhinal Cortex","Brain Mapping","Cataract Extraction","Parks, Recreational","Social Class","Motivation","Popular Culture","Global Burden of Disease","Blood Glucose","Glaucoma","Uveitis","Cornea","Keratitis","Blindness","Mental Disorders","Diabetes Mellitus","Diabetic Retinopathy","Usher Syndromes","Hearing Loss, Sensorineural","Postoperative Complications","Blindness","Blindness","Touch Perception","Theft","Attention","Wolfram Syndrome","Endocrinology","Trigeminal Neuralgia","Nerve Block","Characidae","Carpal Tunnel Syndrome","Shoulder","Trust","Blindness","Medically Underserved Area","Task Shifting","Blindness","Cataract","Glaucoma, Open-Angle","Cataract Extraction"] * 2000  # 10,000 queries


# results = batch_search_icd10(query_terms, batch_size=100)
# search_time = time.time() - start_time

# Display execution times
print(f"Time taken to search query terms: {search_time:.2f} seconds")

# Display results for the first few queries (optional)
# for i, query in enumerate(query_terms[:5]):
#     print(f"Search results for query '{query}':")
#     for result in results[i]:
#         print(result)
#     print()


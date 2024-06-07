# import faiss
# from transformers import AutoTokenizer, AutoModel
# import torch
# import numpy as np
# import pandas as pd

# # Load BioBERT model and tokenizer
# model_name = "dmis-lab/biobert-base-cased-v1.1"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModel.from_pretrained(model_name)

# def embed_text(text, tokenizer, model):
#     # Tokenize the input text and get embeddings
#     inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
#     with torch.no_grad():
#         outputs = model(**inputs)
#     embeddings = outputs.last_hidden_state.mean(dim=1)  # Use the mean of the token embeddings
#     return embeddings.squeeze().numpy()

# # Load the FAISS index from disk
# index = faiss.read_index('faiss_index.bin')

# # Load the original data to retrieve names
# symp_df = pd.read_csv('OUTPUT/active_symptom_terms.csv')
# mesh_df = pd.read_csv('mesh_symptoms.csv', delimiter=';')

# # Convert text to lowercase
# symp_df['Name'] = symp_df['Name'].str.lower()
# mesh_df['Name'] = mesh_df['Name'].str.lower()

# # Concatenate names from both datasets
# names = pd.concat([symp_df['Name'], mesh_df['Name']], ignore_index=True)

# # Function to perform a query on the index
# def query_index(query, index, tokenizer, model, k=5):
#     query_embedding = embed_text(query, tokenizer, model)
#     query_embedding = np.expand_dims(query_embedding, axis=0)  # Add batch dimension
#     distances, indices = index.search(query_embedding, k)
#     return distances, indices

# # Example query
# query = "fever"
# distances, indices = query_index(query, index, tokenizer, model)

# print("Distances:", distances)
# print("Indices:", indices)

# # Print the top 5 nearest neighbors with their corresponding names
# print(f"Query: {query}")
# print("Top 5 nearest neighbors:")
# for i, idx in enumerate(indices[0]):
#     print(f"{i+1}. {names[idx]} (Distance: {distances[0][i]})")



import faiss
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

# Load BioBERT model and tokenizer
model_name = "dmis-lab/biobert-base-cased-v1.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def embed_text(text, tokenizer, model):
    # Tokenize the input text and get embeddings
    inputs = tokenizer(text.lower(), return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)  # Use the mean of the token embeddings
    return embeddings.squeeze().numpy()

# Load the FAISS index and other necessary data from disk
index = faiss.read_index('faiss_index.bin')
names = np.load('names.npy', allow_pickle=True)
sources = np.load('sources.npy', allow_pickle=True)

# Function to perform a query on the index
def query_index(query, index, tokenizer, model, names, sources, k=5):
    query_embedding = embed_text(query, tokenizer, model)
    query_embedding = np.expand_dims(query_embedding, axis=0)  # Add batch dimension
    distances, indices = index.search(query_embedding, k*2)  # Retrieve more to handle duplicates
    seen_names = set()
    results = []
    for distance, idx in zip(distances[0], indices[0]):
        name = names[idx]
        source = sources[idx]
        if name not in seen_names:
            seen_names.add(name)
            results.append((name, source, distance))
        if len(results) == k:
            break
    return results

# Example query
query = "SHORTNESS OF BREATH".lower()
results = query_index(query, index, tokenizer, model, names, sources)

# Print the top 5 nearest neighbors with their corresponding names
print(f"Query: {query}")
print("Top 5 nearest neighbors:")
for i, (name, source, distance) in enumerate(results):
    print(f"{i+1}. {name} (Source: {source}, Distance: {distance})")


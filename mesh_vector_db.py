# import pandas as pd
# from transformers import AutoTokenizer, AutoModel
# import torch
# import faiss
# import numpy as np

# # Load the CSV files
# symp_df = pd.read_csv('OUTPUT/active_symptom_terms.csv')
# mesh_df = pd.read_csv('mesh_symptoms.csv', delimiter=';')

# # Convert text to lowercase
# symp_df['Name'] = symp_df['Name'].str.lower()
# mesh_df['Name'] = mesh_df['Name'].str.lower()

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

# # Generate embeddings for the 'Name' column in symp_df
# symp_embeddings = []
# for name in symp_df['Name']:
#     embedding = embed_text(name, tokenizer, model)
#     symp_embeddings.append(embedding)
# symp_embeddings = np.stack(symp_embeddings)

# # Generate embeddings for the 'Name' column in mesh_df
# mesh_embeddings = []
# for name in mesh_df['Name']:
#     embedding = embed_text(name, tokenizer, model)
#     mesh_embeddings.append(embedding)
# mesh_embeddings = np.stack(mesh_embeddings)

# # Create a FAISS index
# dimension = symp_embeddings.shape[1]
# index = faiss.IndexFlatL2(dimension)

# # Add the embeddings to the index
# index.add(symp_embeddings)
# index.add(mesh_embeddings)

# # Save the FAISS index to disk
# faiss.write_index(index, 'faiss_index.bin')

# print("FAISS index created and saved successfully.")


import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch
import faiss
import numpy as np

# Load the CSV files
symp_df = pd.read_csv('OUTPUT/active_symptom_terms.csv')
mesh_df = pd.read_csv('mesh_symptoms.csv', delimiter=';')

# Convert text to lowercase
symp_df['Name'] = symp_df['Name'].str.lower()
mesh_df['Name'] = mesh_df['Name'].str.lower()

# Create a set to store unique names and prioritize mesh dataset
unique_names = {}
for name in mesh_df['Name']:
    unique_names[name] = 'mesh'

for name in symp_df['Name']:
    if name not in unique_names:
        unique_names[name] = 'symp'

# Create lists of names and their sources
names = list(unique_names.keys())
sources = list(unique_names.values())

# Load BioBERT model and tokenizer
model_name = "dmis-lab/biobert-base-cased-v1.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def embed_text(text, tokenizer, model):
    # Tokenize the input text and get embeddings
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)  # Use the mean of the token embeddings
    return embeddings.squeeze().numpy()

# Generate embeddings for the unique names
embeddings = []
for name in names:
    embedding = embed_text(name, tokenizer, model)
    embeddings.append(embedding)
embeddings = np.stack(embeddings)

# Create a FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

# Add the embeddings to the index
index.add(embeddings)

# Save the FAISS index and other necessary data to disk
faiss.write_index(index, 'faiss_index.bin')
np.save('names.npy', names)
np.save('sources.npy', sources)

print("FAISS index created and saved successfully.")

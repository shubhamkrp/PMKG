import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
from icd9_vector_db import model, icd9_index, icd9_terms

# Read the CSV file into a DataFrame
df = pd.read_csv('hkg_data.csv', delimiter='|')

# Display the DataFrame
print(df.head())

def search_icd9(query, k=1):
    query_embedding = model.encode([query]).astype('float32')
    D, I = icd9_index.search(query_embedding, k)
    # neighbors_list=[]
    
    for i in range(len(I[0])):
        res=icd9_terms[I[0][i]]
    return res

# Function to perform the operation (e.g., converting to uppercase)
def operation_on_row(disease_name):
    return search_icd9(disease_name)

# Get the disease names from the DataFrame
diseases = df['disease'].tolist()

icd9_mapping = search_icd9(diseases, k=1)  # k=1 for the nearest neighbor

# Map the FAISS indices to ICD-9 terms
# icd9_mappings = [search_icd9(idx) for idx in indices.flatten()]

# Add the ICD-9 mappings to the DataFrame
# df['icd9_code'] = icd9_mapping
df['icd9_code'] = df['disease'].apply(operation_on_row)

# Display the updated DataFrame
print(df.head())

# Save the DataFrame to a new CSV file
df.to_csv('mapped_diseases_to_icd9.csv', index=False, sep='|')

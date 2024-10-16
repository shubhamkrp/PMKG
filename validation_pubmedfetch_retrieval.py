import os
import json, csv
import matplotlib.pyplot as plt
from Bio import Entrez

# Set up your email and API key for BioPython Entrez
Entrez.email = "sks@example.com"
# Entrez.api_key = "your_pubmed_api_key"   # Replace with your actual PubMed API key

# Define the folder path containing the JSON files
folder_path = 'sparse_retrieval'

output_csv_file = "validation_pubmed_N_sretrieval.csv"

# Initialize lists to store data for visualization
file_names = []
json_object_counts = []
pubmed_article_counts = []

# Function to fetch article count using BioPython Entrez
def get_pubmed_article_count(query):
    handle = Entrez.esearch(db="pubmed", term=query, retmode="xml")
    record = Entrez.read(handle)
    handle.close()
    return int(record["Count"])

with open(output_csv_file, mode='w', newline='') as csv_file:
    fieldnames = ['Disease', 'Retrieval count', 'Pubmed count']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter='|')
    writer.writeheader()

    # Iterate over each file in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):  # Check if the file is a JSON file
            file_path = os.path.join(folder_path, file_name)
            
            # Open and load the JSON file
            with open(file_path, 'r') as json_file:
                try:
                    data = json.load(json_file)
                    
                    # Count the number of JSON objects in the file
                    if isinstance(data, list):
                        num_json_objects = len(data)
                    else:
                        num_json_objects = 1  # Single JSON object
                    
                    # Modify file_name to match PubMed search format (remove .json and replace _ with space)
                    search_query = file_name.replace('_', ' ').replace('.json', '')
                    
                    # Get the number of articles from PubMed using BioPython
                    pubmed_count = get_pubmed_article_count(f'"{search_query}"' + " AND (1970/01/01[PDAT] : 2023/12/31[PDAT])")
                    
                    # Store the counts for visualization
                    file_names.append(search_query)
                    json_object_counts.append(num_json_objects)
                    pubmed_article_counts.append(pubmed_count)
                    
                    # Print the comparison
                    print(f"File: {search_query}")
                    print(f"JSON object count: {num_json_objects}")
                    print(f"PubMed article count: {pubmed_count}\n")
                    
                    writer.writerow({
                        'Disease': search_query,
                        'Retrieval count': num_json_objects,
                        'Pubmed count': pubmed_count
                    })

                except json.JSONDecodeError as e:
                    print(f"Error reading {file_name}: {e}")

# Visualize the comparison using a bar chart
plt.figure(figsize=(10, 6))

# Set bar width
bar_width = 0.35

# Define positions of bars
positions = range(len(file_names))

# Plot bars for JSON object counts and PubMed article counts
plt.bar(positions, json_object_counts, width=bar_width, label='JSON Object Count', color='b', align='center')
plt.bar([p + bar_width for p in positions], pubmed_article_counts, width=bar_width, label='PubMed Article Count', color='r', align='center')

# Add labels and title
plt.xlabel('File Names (Search Query)')
plt.ylabel('Count')
plt.title('Comparison of JSON Object Counts and PubMed Article Counts')
plt.xticks([p + bar_width / 2 for p in positions], file_names, rotation=90)
plt.legend()

# Display the plot
plt.tight_layout()
plt.show()


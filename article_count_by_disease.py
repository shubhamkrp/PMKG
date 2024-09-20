import csv
from Bio import Entrez
import time

# Provide your email to NCBI
Entrez.email = "sk@example.com"

# List of disease names
diseases = [
    "Heart disease","Coronary artery disease", "Chronic kidney disease", "Migraine", "Tension headache",
    "Type 2 diabetes", "Hypertension", "Asthma", "Osteoarthritis", "Rheumatoid arthritis",
    "Alzheimer's disease", "Parkinson's disease", "Multiple sclerosis", "Celiac disease",
    "Crohn's disease", "Ulcerative colitis", "Psoriasis", "Eczema", "Hypothyroidism",
    "Hyperthyroidism", "Fibromyalgia", "Lupus", "Epilepsy", "Glaucoma", "Cataracts",
    "Macular degeneration", "Pneumonia", "Bronchitis", "Gastroesophageal reflux disease",
    "Irritable bowel syndrome", "Osteoporosis"
]

def get_pubmed_count(query):
    try:
        handle = Entrez.esearch(db="pubmed", term=query, retmax=0)
        record = Entrez.read(handle)
        return int(record["Count"])
    except Exception as e:
        print(f"Error fetching count for {query}: {e}")
        return 0

# Fetch article counts and store results
results = []
for disease in diseases:
    count = get_pubmed_count(disease + " AND (1970/01/01[PDAT] : 2023/12/31[PDAT])")
    results.append({"Disease": disease, "Article Count": count})
    time.sleep(1)

csv_filename = "disease_article_counts.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Disease", "Article Count"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print(f"Results have been saved to {csv_filename}")

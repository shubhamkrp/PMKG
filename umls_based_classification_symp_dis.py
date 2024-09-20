import csv

# Load overlap terms from the CSV file
def load_overlap_terms(overlap_csv_path):
    overlap_terms = set()
    with open(overlap_csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            term = row['term'].lower().strip()  # Normalize the term
            overlap_terms.add(term)
    return overlap_terms

# Load symptom terms from the CSV file
def load_symptom_terms(symptom_csv_path):
    symptom_terms = set()
    with open(symptom_csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            term = row['term'].lower().strip()  # Normalize the term
            symptom_terms.add(term)
    return symptom_terms

# Load disease terms from the CSV file
def load_disease_terms(disease_csv_path):
    disease_terms = set()
    with open(disease_csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            term = row['term'].lower().strip()  # Normalize the term
            disease_terms.add(term)
    return disease_terms

# Function to classify found terms as symptoms or diseases
def classify_terms(found_terms, overlap_terms, symptom_terms, disease_terms):
    classifications = []
    
    for term in found_terms:
        term_normalized = term.lower().strip()  # Normalize the term for comparison
        
        if term_normalized in overlap_terms:
            classifications.append((term, 'Overlap'))
        elif term_normalized in symptom_terms:
            classifications.append((term, 'Symptom'))
        elif term_normalized in disease_terms:
            classifications.append((term, 'Disease'))
        else:
            classifications.append((term, 'Unknown'))
    
    return classifications

# Function to process the sentences and classify terms
def process_sentences_with_classification(input_csv_path, overlap_csv_path, symptom_csv_path, disease_csv_path, output_csv_path):
    # Load symptom and disease terms from CSV files
    overlap_terms = load_disease_terms(overlap_csv_path)
    symptom_terms = load_symptom_terms(symptom_csv_path)
    disease_terms = load_disease_terms(disease_csv_path)

    with open(input_csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        with open(output_csv_path, mode='w', newline='', encoding='utf-8') as output_file:
            fieldnames = ['PMID', 'Sentence', 'Found Terms', 'Classification']
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                pmid = row['PMID']
                sentence = row['Sentence']
                found_terms = row['Found Terms'].split(", ")  # Split found terms by comma and space

                # Classify the terms as symptoms or diseases
                classified_terms = classify_terms(found_terms, overlap_terms, symptom_terms, disease_terms)

                # Write classification results to the output CSV file
                for term, classification in classified_terms:
                    writer.writerow({
                        'PMID': pmid,
                        'Sentence': sentence,
                        'Found Terms': term,
                        'Classification': classification
                    })

# File paths
input_csv_path = 'output_sentences_with_mesh.csv'  # Input file with sentences and found terms
overlap_csv_path = 'overlapping_terms_T184_T047.csv' #both symptom and disease overlap file
symptom_csv_path = 'umls_terms_T184.csv'  # Symptom CSV file
disease_csv_path = 'umls_terms_T047.csv'  # Disease CSV file
output_csv_path = 'umls_classified_sentences_union.csv'  # Output file for classification

# Process the sentences and classify the terms
process_sentences_with_classification(input_csv_path, overlap_csv_path, symptom_csv_path, disease_csv_path, output_csv_path)

print("Classification complete. Results saved to:", output_csv_path)


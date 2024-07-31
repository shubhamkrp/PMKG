# Function to load terms from a file
def load_terms(filename):
    terms = []
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():  # skip empty lines
                term = line.split(':')[0].strip()
                terms.append(term)
    return terms

# Load symptoms and diseases from files
symptoms = load_terms('symptom.txt')
diseases = load_terms('icd_diseases.txt')

# Create pairs of each symptom and disease
pairs = [(symptom, disease) for symptom in symptoms for disease in diseases]

# Write pairs to a text file
with open('symptom_disease_pairs.txt', 'w') as file:
    for symptom, disease in pairs:
        file.write(f"{symptom}| {disease}\n")

print("Pairs of symptoms and diseases have been saved to 'symptom_disease_pairs.txt'.")

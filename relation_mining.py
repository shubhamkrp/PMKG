# import re
# from collections import defaultdict

# # Function to load synonyms from a file into a dictionary
# def load_synonyms(filename):
#     synonyms = {}
#     with open(filename, 'r') as file:
#         for line in file:
#             if line.strip():  # skip empty lines
#                 parts = line.split(':')
#                 term = parts[0].strip()
#                 synonym_list = [syn.strip() for syn in parts[1].split(',')]
#                 synonyms[term] = synonym_list
#     import itertools
#     out = dict(itertools.islice(synonyms.items(), 7)) 
         
#     print("Dictionary limited by K is : " + str(out))
#     return synonyms

# # Function to count occurrences of terms and their synonyms in a text
# def count_occurrences(text, terms_dict):
#     term_counts = defaultdict(int)
#     for term, synonyms in terms_dict.items():
#         # Add the term itself to the list of synonyms for searching
#         all_terms = [term] + synonyms
#         for t in all_terms:
#             if t!="":
#             # Use regex to find exact word matches, case insensitive
#                 matches = re.findall(r'\b' + re.escape(t) + r'\b', text, re.IGNORECASE)
#                 term_counts[term] += len(matches)
#     return term_counts

# # Load the synonyms from the symptom and disease files
# symptom_synonyms = load_synonyms('symptom.txt')
# disease_synonyms = load_synonyms('disease.txt')

# # Paragraph to analyze
# paragraph = """During a 16-year period (1972-1988), 40 out of 477 thyroid cancer patients underwent thyroidectomy for undifferentiated thyroid carcinoma.
# To analyse the significance of "radical" versus "palliative" surgical procedures with regard to early postoperative course, operative complications and survival,
# all patients records were reviewed and actually followed up. A significant better survival was correlated with radical (n = 17) versus palliative tumor resection (n = 23) (p less than 0.001),
# and total thyroidectomy (n = 22) versus subtotal thyroidectomy (n = 18) (p less than 0.006).
# Radical surgery with early postoperative external irradiation revealed no postoperative mortality and only one symptomatic cervical tumor recurrence.
# In contrast, palliative surgery, particularly in the case of synchronous tracheotomy, was attended with a relatively high mortality (30%) and symptomatic local recurrences.
# The results of this study suggest that in undifferentiated thyroid carcinoma without infiltration of the esophageal or tracheal mucosa an attempt of radical tumor resection should be undertaken,
# since palliative surgical procedures revealed a significantly lower survival due to complications of persistent or recurrent cervical tumor infiltration
# and frequently were accompanied by local cowpox lattice corneal dystrophy complications during the postoperative course."""

# # Count occurrences of symptoms and diseases
# symptom_counts = count_occurrences(paragraph, symptom_synonyms)
# disease_counts = count_occurrences(paragraph, disease_synonyms)

# # Combine counts into a single dictionary
# combined_counts = {'symptom': symptom_counts, 'disease': disease_counts}

# # Print the combined counts
# for category, counts in combined_counts.items():
#     print(f"\nCounts for {category}:")
#     for term, count in counts.items():
#         print(f"{term}: {count}")


import re
import csv
from collections import defaultdict

# Function to load pairs from a file
def load_pairs(filename):
    pairs = []
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():  # skip empty lines
                parts = line.strip().split(',')
                symptom = parts[0].strip()
                disease = parts[1].strip()
                pairs.append((symptom, disease))
    return pairs

# Function to count occurrences of term pairs in a text
def count_pair_occurrences(text, pairs):
    pair_counts = defaultdict(int)
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    for sentence in sentences:
        print(sentence)
        sentence = sentence.strip()
        for symptom, disease in pairs:
            if re.search(r'\b' + re.escape(symptom) + r'\b', sentence, re.IGNORECASE) and re.search(r'\b' + re.escape(disease) + r'\b', sentence, re.IGNORECASE):
                pair_counts[(symptom, disease)] += 1
    return pair_counts

# Load pairs from the file
pairs = load_pairs('symptom_disease_pairs.txt')

# Paragraph to analyze
paragraph = """During a 16-year period (1972-1988), 40 out of 477 thyroid cancer patients underwent thyroidectomy for undifferentiated thyroid carcinoma.
To analyse the significance of "radical" versus "palliative" surgical procedures with regard to early postoperative course, operative complications and survival,
all patients records were reviewed and actually followed up. A significant better survival was correlated with radical (n = 17) versus palliative tumor resection (n = 23) (p less than 0.001),
and total thyroidectomy (n = 22) versus subtotal thyroidectomy (n = 18) (p less than 0.006).
Radical surgery with early postoperative external irradiation revealed no postoperative mortality and only one symptomatic cervical tumor recurrence.
In contrast, palliative surgery, particularly in the case of synchronous tracheotomy, was attended with a relatively high mortality (30%) and symptomatic local recurrences.
The results of this study suggest that in undifferentiated thyroid carcinoma without infiltration of the esophageal or tracheal mucosa an attempt of radical tumor resection should be undertaken,
since palliative surgical procedures revealed a significantly lower survival due to complications of persistent or recurrent cervical tumor infiltration
and frequently were accompanied by local complications cowpox ataxia during the postoperative course."""

# Count occurrences of symptom-disease pairs
pair_counts = count_pair_occurrences(paragraph, pairs)

# Function to save counts to CSV in parts with a limit of 10,000 rows per file
def save_counts_to_csv(pair_counts, limit=10000):
    items = list(pair_counts.items())
    num_files = (len(items) + limit - 1) // limit  # Calculate the number of files needed
    for i in range(num_files):
        with open(f'symptom_disease_counts_part_{i+1}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Symptom', 'Disease', 'Count'])
            for pair, count in items[i*limit:(i+1)*limit]:
                writer.writerow([pair[0], pair[1], count])
            print(f'symptom_disease_counts_part_{i+1}.csv saved.')

# Save the pair counts to CSV files
save_counts_to_csv(pair_counts)

print("All pairs have been processed and saved to CSV files.")

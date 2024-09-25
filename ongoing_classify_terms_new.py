# import csv
# import spacy
# from transformers import BertTokenizer, BertForSequenceClassification
# import torch

# # Load the spacy model
# nlp = spacy.load("en_core_web_sm")

# # Load custom MeSH terms from CSV
# def load_mesh_terms(csv_file):
#     mesh_terms = {}
#     with open(csv_file, newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             mesh_terms[row['Mesh terms'].lower()] = row['Tree Number']
#     return mesh_terms

# # Load pre-trained BERT model for symptom vs disease classification
# def load_bert_model(model_name='bert-base-uncased', num_labels=2):
#     tokenizer = BertTokenizer.from_pretrained(model_name)
#     model = BertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
#     return tokenizer, model

# # Predict whether the term is a symptom or disease using BERT
# def classify_term_with_bert(term, sentence, tokenizer, model):
#     inputs = tokenizer(f"{sentence} [SEP] {term}", return_tensors="pt", padding=True, truncation=True)
#     with torch.no_grad():
#         outputs = model(**inputs)
#     logits = outputs.logits
#     predicted_class = torch.argmax(logits, dim=1).item()
    
#     # Assuming label 0 = "symptom" and label 1 = "disease"
#     if predicted_class == 0:
#         return "symptom"
#     elif predicted_class == 1:
#         return "disease"
#     return "unknown"

# # Main function to find and classify MeSH terms in a sentence
# def find_and_classify_mesh_terms(sentence, mesh_terms, tokenizer, model):
#     doc = nlp(sentence.lower())  # Process the sentence with spaCy
#     identified_terms = []
    
#     # Check for MeSH terms in the sentence
#     for token in doc:
#         if token.text in mesh_terms:
#             # Classify the term using BERT
#             context_classification = classify_term_with_bert(token.text, sentence, tokenizer, model)
#             identified_terms.append((token.text, context_classification))
    
#     return identified_terms

# # Example usage
# if __name__ == "__main__":
#     # Load your custom MeSH terms from the CSV file
#     mesh_terms = load_mesh_terms("mesh_terms.csv")
    
#     # Load the BERT model and tokenizer
#     tokenizer, model = load_bert_model()

#     # Example sentence
#     sentence = "Chest pain, shortnness of breath, and common cold are the findings on the effects of fever, asthma, and other respiratory diseases."

#     # Find and classify MeSH terms in the sentence
#     identified_terms = find_and_classify_mesh_terms(sentence, mesh_terms, tokenizer, model)
    
#     # Output the results
#     for term, classification in identified_terms:
#         print(f"Term: {term}, Classified as: {classification}")



# import torch
# from transformers import BertTokenizer, BertForTokenClassification
# from transformers import pipeline

# model_name = "dmis-lab/biobert-base-cased-v1.1"
# tokenizer = BertTokenizer.from_pretrained(model_name)
# model = BertForTokenClassification.from_pretrained(model_name)

# nlp_ner = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# sentence = "The patient has fever and cough, which may indicate an upper respiratory tract infection."

# entities = nlp_ner(sentence)

# for entity in entities:
#     print(f"Entity: {entity['word']}, Label: {entity['entity_group']}, Score: {entity['score']:.4f}")




# import spacy
# import csv
# from transformers import pipeline

# # Load a spaCy model for dependency parsing and POS tagging
# nlp_spacy = spacy.load("en_core_web_sm")  # SciSpacy for biomedical texts en_core_sci_md

# # Load a BioBERT-based NER model
# ner_model = pipeline("ner", model="dmis-lab/biobert-v1.1", tokenizer="dmis-lab/biobert-v1.1", aggregation_strategy="simple")

# # Classify terms as symptom or disease using the NER model
# def classify_terms(sentence, found_terms):
#     doc = nlp_spacy(sentence)  # Process the sentence with spaCy
    
#     # Dependency Parsing and POS tagging using spaCy
#     parsed_info = [(token.text, token.dep_, token.head.text, token.pos_) for token in doc]
    
#     # Use BioBERT for NER
#     ner_results = ner_model(sentence)
    
#     classified_terms = []
    
#     # Classify each found term
#     for term in found_terms:
#         for entity in ner_results:
#             if entity['word'].lower() in term.lower():  # Match found term with NER output
#                 entity_label = entity['entity_group']  # NER label (e.g., DISEASE, SYMPTOM)
                
#                 # Append classification to the term
#                 classified_terms.append({
#                     'term': term,
#                     'classification': entity_label,
#                     'parsed_info': parsed_info
#                 })
    
#     return classified_terms

# # Function to process and classify the found terms
# def process_sentences_with_context(input_csv_path, output_csv_path):
#     with open(input_csv_path, mode='r', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         with open(output_csv_path, mode='w', newline='', encoding='utf-8') as output_file:
#             fieldnames = ['PMID', 'Sentence', 'Found Terms', 'Classification']
#             writer = csv.DictWriter(output_file, fieldnames=fieldnames)
#             writer.writeheader()

#             for row in reader:
#                 pmid = row['PMID']
#                 sentence = row['Sentence']
#                 found_terms = row['Found Terms'].split(", ")

#                 # Classify the terms as symptoms or diseases using context
#                 classified_terms = classify_terms(sentence, found_terms)

#                 # Prepare the classification result for each found term
#                 for term_data in classified_terms:
#                     writer.writerow({
#                         'PMID': pmid,
#                         'Sentence': sentence,
#                         'Found Terms': term_data['term'],
#                         'Classification': term_data['classification']
#                     })

# # File paths
# input_csv_path = 'output_sentences_with_mesh.csv'  # Input file with sentences and found terms
# output_csv_path = 'classified_sentences_with_context.csv'  # Output file for classification

# # Process the sentences and classify the terms
# process_sentences_with_context(input_csv_path, output_csv_path)

# print("Classification complete. Results saved to:", output_csv_path)




# import csv
# from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# # Load a NER model from Hugging Face
# model_name = "microsoft/BioGPT-Large-PubMedQA" #"emilyalsentzer/Bio_ClinicalBERT" #"microsoft/BiomedNLP-PubMedBERT-base-uncased-ner"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForTokenClassification.from_pretrained(model_name)

# # Create a pipeline for Named Entity Recognition (NER)
# ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# # Function to classify terms as disease or symptom
# def classify_terms(sentence, found_terms):
#     # Get NER results for the sentence
#     ner_results = ner_pipeline(sentence)
    
#     classified_terms = []
    
#     # Classify each found term based on NER results
#     for term in found_terms:
#         term_found = False
#         for entity in ner_results:
#             if entity['word'].lower() in term.lower():  # Match found term with NER output
#                 entity_label = entity['entity_group']  # NER label (e.g., DISEASE, SYMPTOM)
#                 classified_terms.append({
#                     'term': term,
#                     'classification': entity_label
#                 })
#                 term_found = True
#                 break
        
#         # If no entity found, mark as 'Unknown'
#         if not term_found:
#             classified_terms.append({
#                 'term': term,
#                 'classification': 'Unknown'
#             })
    
#     return classified_terms

# # Function to process and classify the found terms
# def process_sentences_with_context(input_csv_path, output_csv_path):
#     with open(input_csv_path, mode='r', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         with open(output_csv_path, mode='w', newline='', encoding='utf-8') as output_file:
#             fieldnames = ['PMID', 'Sentence', 'Found Terms', 'Classification']
#             writer = csv.DictWriter(output_file, fieldnames=fieldnames)
#             writer.writeheader()

#             for row in reader:
#                 pmid = row['PMID']
#                 sentence = row['Sentence']
#                 found_terms = row['Found Terms'].split(", ")

#                 # Classify the terms as symptoms or diseases using context
#                 classified_terms = classify_terms(sentence, found_terms)

#                 # Write classification results for each found term
#                 for term_data in classified_terms:
#                     writer.writerow({
#                         'PMID': pmid,
#                         'Sentence': sentence,
#                         'Found Terms': term_data['term'],
#                         'Classification': term_data['classification']
#                     })

# # File paths
# input_csv_path = 'output_sentences_with_mesh.csv'  # Input file with sentences and found terms
# output_csv_path = 'classified_sentences_with_context_bioGPT.csv'  # Output file for classification

# # Process the sentences and classify the terms
# process_sentences_with_context(input_csv_path, output_csv_path)

# print("Classification complete. Results saved to:", output_csv_path)



# import stanza
# import pandas as pd
# import networkx as nx
# import matplotlib.pyplot as plt

# # Initialize Stanford NLP pipeline
# stanza.download('en')  # Make sure to download the necessary models
# nlp = stanza.Pipeline('en')

# # Load MeSH terms from CSV
# def load_mesh_terms(csv_file):
#     mesh_df = pd.read_csv(csv_file)
#     return mesh_df['Mesh terms'].tolist()

# # Function to build dependency parse tree and visualize
# def visualize_dependency_tree(sentence, mesh_terms):
#     doc = nlp(sentence)
#     G = nx.DiGraph()

#     mesh_indices = {}

#     for sent in doc.sentences:
#         for word in sent.words:
#             # Add nodes for each word in the sentence
#             G.add_node(word.id, label=word.text)
#             if word.head != 0:  # Root has no head
#                 # Add edges for dependency relations
#                 G.add_edge(word.head, word.id, label=word.deprel)
            
#             # Check if the word matches a MeSH term
#             for mesh_term in mesh_terms:
#                 if mesh_term.lower() in word.text.lower():
#                     # Save MeSH term indices for highlighting later
#                     mesh_indices[word.id] = word.text

#     # Plot the dependency tree
#     plt.figure(figsize=(12, 8))
#     pos = nx.spring_layout(G, seed=42)

#     # Draw nodes
#     node_labels = nx.get_node_attributes(G, 'label')
#     nx.draw(G, pos, with_labels=True, labels=node_labels, node_color='lightblue', node_size=2000, font_size=10, font_color='black')

#     # Highlight MeSH terms
#     mesh_node_ids = list(mesh_indices.keys())
#     nx.draw_networkx_nodes(G, pos, nodelist=mesh_node_ids, node_color='yellow', node_size=2500)

#     # Draw edges with dependency labels
#     edge_labels = nx.get_edge_attributes(G, 'label')
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

#     plt.title(f"Dependency Parse Tree for Sentence:\n'{sentence}'")
#     plt.show()

# # Example sentence input
# sentences = [
#     "Cardiovascular disease remains a leading cause of death worldwide despite important advances in modern medical and surgical therapies.",
#     "Atherosclerosis is a chronic inflammatory disease of the arteries that can lead to thrombosis, infarction and stroke, underlying the first cause of mortality worldwide.",
#     "COPD is characterized by chronic bronchitis and emphysema, and is often accompanied by malnutrition with fatigue, muscle weakness, and an increased risk of infection."
# ]

# # Load the MeSH terms from CSV file (replace 'mesh_terms.csv' with your actual file path)
# mesh_csv_file = 'mesh_terms.csv'  # Replace with the path to your MeSH CSV file
# mesh_terms = load_mesh_terms(mesh_csv_file)

# # Visualize dependency trees for each sentence
# for sentence in sentences:
#     visualize_dependency_tree(sentence, mesh_terms)



# import stanza
# import pandas as pd

# # Initialize Stanford NLP pipeline
# stanza.download('en')
# nlp = stanza.Pipeline('en')

# # Load MeSH terms from CSV
# def load_mesh_terms(csv_file):
#     mesh_df = pd.read_csv(csv_file)
#     return mesh_df['Mesh terms'].apply(str.lower).tolist()

# # Function to identify dependency relations between MeSH terms in a sentence
# def find_mesh_to_mesh_dependencies(sentence, mesh_terms):
#     doc = nlp(sentence)
#     mesh_indices = {}
#     dependencies = []

#     for sent in doc.sentences:
#         for word in sent.words:
#             # Check if the word matches a MeSH term (ignoring case)
#             for mesh_term in mesh_terms:
#                 if mesh_term.lower() in word.text.lower():
#                     # Save the index of MeSH term for relation checks later
#                     mesh_indices[word.id] = word.text
        
#         # Find dependency relations between MeSH terms
#         for word in sent.words:
#             if word.id in mesh_indices and word.head in mesh_indices:
#                 # Extract both the dependent and head words that are MeSH terms
#                 dep_term = mesh_indices[word.id]
#                 head_term = mesh_indices[word.head]
#                 dep_type = word.deprel
#                 dependencies.append({
#                     'dependent_term': dep_term,
#                     'head_term': head_term,
#                     'dependency_type': dep_type
#                 })

#     return dependencies

# # Example sentence input
# sentences = [
#     "Cardiovascular disease remains a leading cause of death worldwide despite important advances in modern medical and surgical therapies.",
#     "Atherosclerosis is a chronic inflammatory disease of the arteries that can lead to thrombosis, infarction and stroke, underlying the first cause of mortality worldwide.",
#     "COPD is characterized by chronic bronchitis and emphysema, and is often accompanied by malnutrition with fatigue, muscle weakness, and an increased risk of infection.",
#     "Arrhythmogenic right ventricular cardiomyopathy (ARVC) is a fatal genetic heart disease characterized by cardiac arrhythmias, in which fibrofatty deposition leads to heart failure, with no effective treatments.",
#     "The most common symptoms include fatigue, dyspnea, and other symptoms involving multiple organs.",
#     "Interstitial lung disease (ILD) is a critical extra-articular manifestation of rheumatoid arthritis (RA)."
# ]

# # Load the MeSH terms from CSV file (replace 'mesh_terms.csv' with your actual file path)
# mesh_csv_file = 'cleaned_mesh_terms.csv'  # Replace with the path to your MeSH CSV file
# mesh_terms = load_mesh_terms(mesh_csv_file)

# # Process each sentence and list only the dependency relations between MeSH terms
# for sentence in sentences:
#     print(f"\nProcessing sentence: {sentence}")
#     dependencies = find_mesh_to_mesh_dependencies(sentence, mesh_terms)
#     if dependencies:
#         for dep in dependencies:
#             print(f"MeSH Term (Dependent): '{dep['dependent_term']}' -> MeSH Term (Head): '{dep['head_term']}', Dependency Type: '{dep['dependency_type']}'")
#     else:
#         print("No MeSH term-to-MeSH term dependency relations found.")



import stanza
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import re

# Initialize Stanford NLP pipeline
stanza.download('en')  # Make sure to download the necessary models
nlp = stanza.Pipeline('en')

# Load MeSH terms from CSV and normalize them to lowercase for matching
def load_mesh_terms(csv_file):
    mesh_df = pd.read_csv(csv_file)
    return set(mesh_df['Mesh terms'].str.lower().tolist())  # Convert to lowercase and use a set for faster lookup

# Function to build dependency parse tree and visualize
def visualize_dependency_tree(sentence, mesh_terms):
    doc = nlp(sentence)
    G = nx.DiGraph()

    mesh_indices = {}
    dependencies = []
    for sent in doc.sentences:
        for word in sent.words:
            # Add nodes for each word in the sentence
            G.add_node(word.id, label=word.text)
            if word.head != 0:  # Root has no head
                # Add edges for dependency relations
                G.add_edge(word.head, word.id, label=word.deprel)
            
            # Check if the word matches a MeSH term using exact match (ignoring case)
            for mesh_term in mesh_terms:
                # Ensure full word match (not substring match)
                if re.fullmatch(r'\b' + re.escape(mesh_term) + r'\b', word.text.lower()):
                    # Save MeSH term indices for highlighting later
                    mesh_indices[word.id] = word.text
            
        # Find dependency relations between MeSH terms
        for word in sent.words:
            if word.id in mesh_indices and word.head in mesh_indices:
                # Extract both the dependent and head words that are MeSH terms
                dep_term = mesh_indices[word.id]
                head_term = mesh_indices[word.head]
                dep_type = word.deprel
                dependencies.append({
                    'dependent_term': dep_term,
                    'head_term': head_term,
                    'dependency_type': dep_type
                })
    

    # Plot the dependency tree
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)

    # Draw nodes
    node_labels = nx.get_node_attributes(G, 'label')
    nx.draw(G, pos, with_labels=True, labels=node_labels, node_color='lightblue', node_size=2000, font_size=10, font_color='black')

    # Highlight MeSH terms
    mesh_node_ids = list(mesh_indices.keys())
    nx.draw_networkx_nodes(G, pos, nodelist=mesh_node_ids, node_color='yellow', node_size=2500)

    # Draw edges with dependency labels
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    plt.title(f"Dependency Parse Tree for Sentence:\n'{sentence}'")
    plt.show()
    return dependencies

# Example sentence input
sentences = [
    "Atherosclerosis is a chronic inflammatory disease of the arteries that can lead to thrombosis, infarction and stroke, underlying the first cause of mortality worldwide.",
    "Adaptive immunity plays critical roles in atherosclerosis, and numerous studies have ascribed both atheroprotective and atherogenic functions to specific subsets of T and B cells.",
    "Arrhythmogenic right ventricular cardiomyopathy (ARVC) is a fatal genetic heart disease characterized by cardiac arrhythmias, in which fibrofatty deposition leads to heart failure, with no effective treatments.",
    "The most common symptoms include fatigue, dyspnea, and other symptoms involving multiple organs.",
    "COPD is characterized by chronic bronchitis and emphysema, and is often accompanied by malnutrition with fatigue, muscle weakness, and an increased risk of infection.",
    "A 38-year-old patient diagnosed with asthma and anxiety, who takes two medications (salbutamol 100 mcg inhaler (2 puffs every 6 hours), and diazepam 5 mg (0-0-1), visited the Community Pharmacy to pick up a treatment prescribed by the Primary Care Physician (PCP) following a diagnosis of anxious-depressive symptoms.During the Dispensing Service, a potential Drug-Related Problem (DRP) of prescription error is detected, which could be related with a Negative Outcomes Releated to Medicines (NOM) due to the concurrent use of desvenlafaxine and mirtazapine.",
    "Residual pulmonary vascular obstruction (RPVO) following pulmonary embolism (PE) is associated with residual dyspnea, recurrent venous thromboembolism, and chronic thromboembolic pulmonary hypertension.",
    "Cachexia is a metabolic syndrome defined by a loss of more than 5% of body weight in patients with chronic diseases.",
    "Interstitial lung disease (ILD) is a critical extra-articular manifestation of rheumatoid arthritis (RA).",
    "Residual pulmonary vascular obstruction (RPVO) following pulmonary embolism (PE) is associated with residual dyspnea, recurrent venous thromboembolism, and chronic thromboembolic pulmonary hypertension."
]

# Load the MeSH terms from CSV file (replace 'mesh_terms.csv' with your actual file path)
mesh_csv_file = 'cleaned_mesh_terms.csv'
mesh_terms = load_mesh_terms(mesh_csv_file)

# Visualize dependency trees for each sentence
# Process each sentence and list only the dependency relations between MeSH terms
for sentence in sentences:
    print(f"\nProcessing sentence: {sentence}")
    dependencies = visualize_dependency_tree(sentence, mesh_terms)
    if dependencies:
        for dep in dependencies:
            print(f"MeSH Term (Dependent): '{dep['dependent_term']}' -> MeSH Term (Head): '{dep['head_term']}', Dependency Type: '{dep['dependency_type']}'")
    else:
        print("No MeSH term-to-MeSH term dependency relations found.")
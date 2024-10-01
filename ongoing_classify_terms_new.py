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



# import stanza
# import pandas as pd
# import networkx as nx
# import matplotlib.pyplot as plt
# import re

# # Initialize Stanford NLP pipeline
# stanza.download('en')  # Make sure to download the necessary models
# nlp = stanza.Pipeline('en')

# # Load MeSH terms from CSV and normalize them to lowercase for matching
# def load_mesh_terms(csv_file):
#     mesh_df = pd.read_csv(csv_file)
#     return set(mesh_df['Mesh terms'].str.lower().tolist())  # Convert to lowercase and use a set for faster lookup

# # Function to build dependency parse tree and visualize
# def visualize_dependency_tree(sentence, mesh_terms):
#     doc = nlp(sentence)
#     G = nx.DiGraph()

#     mesh_indices = {}
#     dependencies = []
#     for sent in doc.sentences:
#         for word in sent.words:
#             # Add nodes for each word in the sentence
#             G.add_node(word.id, label=word.text)
#             if word.head != 0:  # Root has no head
#                 # Add edges for dependency relations
#                 G.add_edge(word.head, word.id, label=word.deprel)
            
#             # Check if the word matches a MeSH term using exact match (ignoring case)
#             for mesh_term in mesh_terms:
#                 # Ensure full word match (not substring match)
#                 if re.fullmatch(r'\b' + re.escape(mesh_term) + r'\b', word.text.lower()):
#                     # Save MeSH term indices for highlighting later
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
#     return dependencies

# # Example sentence input
# sentences = [
#     "Atherosclerosis is a chronic inflammatory disease of the arteries that can lead to thrombosis, infarction and stroke, underlying the first cause of mortality worldwide.",
#     "Adaptive immunity plays critical roles in atherosclerosis, and numerous studies have ascribed both atheroprotective and atherogenic functions to specific subsets of T and B cells.",
#     "Arrhythmogenic right ventricular cardiomyopathy (ARVC) is a fatal genetic heart disease characterized by cardiac arrhythmias, in which fibrofatty deposition leads to heart failure, with no effective treatments.",
#     "The most common symptoms include fatigue, dyspnea, and other symptoms involving multiple organs.",
#     "COPD is characterized by chronic bronchitis and emphysema, and is often accompanied by malnutrition with fatigue, muscle weakness, and an increased risk of infection.",
#     "A 38-year-old patient diagnosed with asthma and anxiety, who takes two medications (salbutamol 100 mcg inhaler (2 puffs every 6 hours), and diazepam 5 mg (0-0-1), visited the Community Pharmacy to pick up a treatment prescribed by the Primary Care Physician (PCP) following a diagnosis of anxious-depressive symptoms.During the Dispensing Service, a potential Drug-Related Problem (DRP) of prescription error is detected, which could be related with a Negative Outcomes Releated to Medicines (NOM) due to the concurrent use of desvenlafaxine and mirtazapine.",
#     "Residual pulmonary vascular obstruction (RPVO) following pulmonary embolism (PE) is associated with residual dyspnea, recurrent venous thromboembolism, and chronic thromboembolic pulmonary hypertension.",
#     "Cachexia is a metabolic syndrome defined by a loss of more than 5% of body weight in patients with chronic diseases.",
#     "Interstitial lung disease (ILD) is a critical extra-articular manifestation of rheumatoid arthritis (RA).",
#     "Residual pulmonary vascular obstruction (RPVO) following pulmonary embolism (PE) is associated with residual dyspnea, recurrent venous thromboembolism, and chronic thromboembolic pulmonary hypertension."
# ]

# # Load the MeSH terms from CSV file (replace 'mesh_terms.csv' with your actual file path)
# mesh_csv_file = 'cleaned_mesh_terms.csv'
# mesh_terms = load_mesh_terms(mesh_csv_file)

# # Visualize dependency trees for each sentence
# # Process each sentence and list only the dependency relations between MeSH terms
# for sentence in sentences:
#     print(f"\nProcessing sentence: {sentence}")
#     dependencies = visualize_dependency_tree(sentence, mesh_terms)
#     if dependencies:
#         for dep in dependencies:
#             print(f"MeSH Term (Dependent): '{dep['dependent_term']}' -> MeSH Term (Head): '{dep['head_term']}', Dependency Type: '{dep['dependency_type']}'")
#     else:
#         print("No MeSH term-to-MeSH term dependency relations found.")


########### working dependency tree visualization ##############
# import stanza
# import pandas as pd
# import networkx as nx
# import matplotlib.pyplot as plt
# import re

# # Initialize Stanford NLP pipeline
# stanza.download('en')  # Download necessary models
# nlp = stanza.Pipeline('en')

# # Load MeSH terms from CSV and normalize to lowercase for matching
# def load_mesh_terms(csv_file):
#     mesh_df = pd.read_csv(csv_file)
#     return set(mesh_df['Mesh terms'].str.lower().tolist())  # Convert to lowercase and use set for faster lookup

# # Function to build and visualize a hierarchical dependency tree using NetworkX
# def visualize_dependency_tree(sentence, mesh_terms):
#     doc = nlp(sentence)
#     G = nx.DiGraph()

#     mesh_indices = {}
#     root_node = None  # To track the root node dynamically

#     # Build the dependency graph
#     for sent in doc.sentences:
#         for word in sent.words:
#             # Add nodes for each word in the sentence along with POS tags
#             G.add_node(word.id, label=f"{word.text} ({word.upos})")  # Including POS tags

#             # Identify the root node (head = 0 means root)
#             if word.head == 0:
#                 root_node = word.id

#             if word.head != 0:  # Root has no head
#                 # Add edges for dependency relations
#                 G.add_edge(word.head, word.id, label=word.deprel)
            
#             # Check if the word matches a MeSH term using exact match (ignoring case)
#             for mesh_term in mesh_terms:
#                 if re.fullmatch(r'\b' + re.escape(mesh_term) + r'\b', word.text.lower()):
#                     # Save MeSH term indices for highlighting later
#                     mesh_indices[word.id] = word.text

#     if root_node is None:
#         print("Root node not found. Skipping this sentence.")
#         return
    
#     # Create the tree-like layout (layered layout)
#     pos = hierarchy_pos(G, root_node)  # Start layout with detected root node

#     # Plot the tree
#     plt.figure(figsize=(12, 8))

#     # Draw nodes with MeSH terms highlighted
#     node_colors = ['yellow' if node in mesh_indices else 'lightblue' for node in G.nodes()]
#     node_labels = nx.get_node_attributes(G, 'label')  # POS tags included in labels

#     nx.draw(G, pos, with_labels=True, labels=node_labels, node_color=node_colors, node_size=2000, font_size=10, font_color='black')

#     # Draw edges with dependency labels
#     edge_labels = nx.get_edge_attributes(G, 'label')
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

#     plt.title(f"Dependency Parse Tree for Sentence:\n'{sentence}'")
#     plt.show()

# # Helper function for hierarchical tree layout
# def hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
#     """
#     Create a hierarchical layout for the nodes in the tree, starting from the root node.
#     This function recursively positions the nodes at different vertical levels.
#     """
#     pos = _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
#     return pos

# def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=[]):
#     if pos is None:
#         pos = {root: (xcenter, vert_loc)}
#     else:
#         pos[root] = (xcenter, vert_loc)
    
#     children = list(G.neighbors(root))
#     if not isinstance(G, nx.DiGraph) and parent is not None:
#         children.remove(parent)
    
#     if len(children) != 0:
#         dx = width / len(children)
#         nextx = xcenter - width/2 - dx/2
#         for child in children:
#             nextx += dx
#             pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, parent=root, parsed=parsed)
    
#     return pos

# # Example sentences
# sentences = [
#     "Physical examination revealed a compromised general condition, fever, pallor, hepatomegaly and lymphadenopathy.",
#     "Fibromyalgia (FM) is a chronic pain disorder characterised by widespread pain, fatigue and cognitive symptoms.",
#     "This brief viewpoint attempts to reason why phantom limb paresthesia or pain should be included in the fold of refereed pain discussions.",
#     "Lateral medullary syndrome is a common presentation of posterior circulation ischemia that presents with ipsilateral Horner syndrome, ipsilateral facial numbness, contralateral body numbness, vestibular symptoms, ataxia, dysphagia, and dysarthria.",
#     "In the initial days or weeks after infection, patients with early, localized, or disseminated Lyme disease often present with non-specific signs and symptoms resembling a viral infection: fatigue, headache, loss of appetite, joint pain, and regional lymphadenopathy.",
#     "Abdominal pain is the most common symptom of chronic pancreatitis (CP) and is often debilitating for patients and very difficult to treat.",
#     "Associations between nutritional intake, stress and hunger biomarkers, and anxiety and depression during the treatment of anorexia nervosa in adolescents and young adults.",
#     "Polymyositis is a chronic autoimmune disease that presents with symmetrical progressive proximal muscle weakness.",
#     "Progressive myoclonic epilepsies (PMEs) are a group of neurodegenerative disorders, predominantly affecting adolescents and, characterized by generalized worsening myoclonus epilepsies, ataxia, cognitive deficits, and dementia.",
#     "Total knee arthroplasty (TKA) improves patient-reported function by alleviating joint pain, however the surgical trauma exacerbates already impaired muscle function, which leads to further muscle weakness and disability after surgery.",
#     "The patient suffered from anorexia and epigastric pain for a month, and a local physician suspected a diagnosis of gastric ulcer.",
# ]

# # Load the MeSH terms from CSV file (replace 'mesh_terms.csv' with your actual file path)
# mesh_csv_file = 'cleaned_mesh_terms.csv'  # Replace with the path to your MeSH CSV file
# mesh_terms = load_mesh_terms(mesh_csv_file)

# # Visualize dependency trees for each sentence
# for sentence in sentences:
#     visualize_dependency_tree(sentence, mesh_terms)


import stanza
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import re

# Initialize Stanza pipeline
# stanza.download('en')
nlp = stanza.Pipeline('en')

# Load MeSH terms from CSV and normalize to lowercase for matching
def load_mesh_terms(csv_file):
    mesh_df = pd.read_csv(csv_file)
    return set(mesh_df['Mesh terms'].str.lower().tolist())

# Helper function for hierarchical tree layout
def hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    """
    Create a hierarchical layout for the nodes in the tree, starting from the root node.
    """
    pos = _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
    return pos

def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    
    children = list(G.neighbors(root))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        children.remove(parent)
    
    if len(children) != 0:
        dx = width / len(children)
        nextx = xcenter - width/2 - dx/2
        for child in children:
            nextx += dx
            pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, parent=root)
    
    return pos


# Heuristic Classification Function 
def classify_mesh_term(word, G): 
    """ Classify a MeSH term as 'Symptom' or 'Disease' based on structural features. """ 
    # Initialize classification 
    classification = 'Unknown' 
    # Extract features 
    dep_label = G.nodes[word.id]['dep_label'] 
    pos_tag = G.nodes[word.id]['pos_tag'] 
    parent = word.head 
    parent_dep_label = G.nodes[parent]['dep_label'] if parent in G.nodes else None 
    parent_pos_tag = G.nodes[parent]['pos_tag'] if parent in G.nodes else None 
    # Heuristic Rules # Rule 1: Dependency Label 
    if dep_label in ['ROOT', 'nsubj', 'nsubjpass']: 
        classification = 'Disease' 
    elif dep_label in ['dobj', 'amod', 'nmod' 'compound', 'appos']: 
        classification = 'Symptom' 
    # Rule 2: POS Tag (if not classified yet) 
    if classification == 'Unknown': 
        if pos_tag == 'NOUN': 
            classification = 'Symptom' 
        elif pos_tag == 'ADJ': 
            classification = 'Symptom' 
    # Rule 3: Parent Dependency Label 
    if classification == 'Symptom' and parent_dep_label in ['advmod', 'amod', 'conj']: 
        classification = 'Symptom' 
    elif classification == 'Disease' and parent_dep_label in ['nsubj', 'nsubjpass', 'conj']: 
        classification = 'Disease'
    return classification 


def classify_mesh_term_with_context(word, G, sentence_text):
    """
    Classify a MeSH term as 'Symptom' or 'Disease' based on structural features and sentence context.
    """
    classification = classify_mesh_term(word, G)
    
    # Additional context-based rules
    sentence_lower = sentence_text.lower()
    
    # Define verb phrases associated with diseases or symptoms
    disease_verbs = ['diagnosed with', 'suffer from', 'is', 'are', 'has', 'have', 'presented with', 'characterized by', 'examine', 'diminish', 'worsen', 'lead to', 'induce']
    symptom_verbs = ['experience', 'exhibit', 'present with', 'presents with' 'suffer from', 'show', 'display', 'manifest', 'indicate', 'represent', 'signify', 'associate', 'persist', 'trigger', 'suffer', 'develop']
    
    # Check if any disease verbs are in proximity to the MeSH term
    for verb in disease_verbs:
        if verb in sentence_lower:
            # Simple proximity check: if verb is within 3 words before the term
            pattern = r'{} .*?\b{}\b'.format(re.escape(verb), re.escape(word.text.lower()))
            if re.search(pattern, sentence_lower):
                classification = 'Disease'
                break
    
    # Check if any symptom verbs are in proximity to the MeSH term
    if classification == 'Unknown' or classification == 'Symptom':
        for verb in symptom_verbs:
            if verb in sentence_lower:
                # Simple proximity check: if verb is within 3 words before the term
                pattern = r'{} .*?\b{}\b'.format(re.escape(verb), re.escape(word.text.lower()))
                if re.search(pattern, sentence_lower):
                    classification = 'Symptom'
                    break
    
    return classification


# Function to build, visualize, extract features, and classify MeSH terms
def visualize_extract_classify_with_context(sentence, mesh_terms, sentence_id, classification_results):
    doc = nlp(sentence)
    G = nx.DiGraph()

    mesh_indices = {}
    root_node = None  # To track the root node dynamically

    # Build the dependency graph
    for sent in doc.sentences:
        for word in sent.words:
            # Add nodes with labels
            G.add_node(word.id, label=f"{word.text} ({word.upos})", pos_tag=word.upos, dep_label=word.deprel)
            
            # Identify the root node (head = 0 means root)
            if word.head == 0:
                root_node = word.id

            if word.head != 0:  # Root has no head
                # Add edges for dependency relations
                G.add_edge(word.head, word.id, label=word.deprel)
            
            # Check if the word matches a MeSH term using exact match (ignoring case)
            for mesh_term in mesh_terms:
                if re.fullmatch(r'\b' + re.escape(mesh_term) + r'\b', word.text.lower()):
                    # Save MeSH term indices for highlighting and analysis
                    mesh_indices[word.id] = word.text

    if root_node is None:
        print(f"Root node not found for sentence {sentence_id}. Skipping this sentence.")
        return

    # Create the tree-like layout (layered layout)
    pos = hierarchy_pos(G, root_node)  # Start layout with detected root node

    # Plot the tree
    plt.figure(figsize=(12, 8))

    # Draw nodes with MeSH terms highlighted
    node_colors = ['yellow' if node in mesh_indices else 'lightblue' for node in G.nodes()]
    node_labels = nx.get_node_attributes(G, 'label')  # POS tags included in labels

    nx.draw(G, pos, with_labels=True, labels=node_labels, node_color=node_colors, node_size=2000, font_size=10, font_color='black')

    # Draw edges with dependency labels
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    plt.title(f"Dependency Parse Tree for Sentence {sentence_id}:\n'{sentence}'")
    plt.show()

    # Classification with advanced context
    for mesh_id, mesh_text in mesh_indices.items():
        # Retrieve the Word object
        word = next((w for s in doc.sentences for w in s.words if w.id == mesh_id), None)
        if word:
            classification = classify_mesh_term_with_context(word, G, sentence)
            classification_results.append({
                'Sentence_ID': sentence_id,
                'Sentence': sentence,
                'Mesh_Term': mesh_text,
                'Classification': classification
            })

# Example sentences
sentences = [
   "Physical examination revealed a compromised general condition, fever, pallor, hepatomegaly and lymphadenopathy.",
   "Fibromyalgia (FM) is a chronic pain disorder characterised by widespread pain, fatigue and cognitive symptoms.",
   "This brief viewpoint attempts to reason why phantom limb paresthesia or pain should be included in the fold of refereed pain discussions.",
   "Lateral medullary syndrome is a common presentation of posterior circulation ischemia that presents with ipsilateral Horner syndrome, ipsilateral facial numbness, contralateral body numbness, vestibular symptoms, ataxia, dysphagia, and dysarthria.",
   "In the initial days or weeks after infection, patients with early, localized, or disseminated Lyme disease often present with non-specific signs and symptoms resembling a viral infection: fatigue, headache, loss of appetite, joint pain, and regional lymphadenopathy.",
   "Abdominal pain is the most common symptom of chronic pancreatitis (CP) and is often debilitating for patients and very difficult to treat.",
   "Associations between nutritional intake, stress and hunger biomarkers, and anxiety and depression during the treatment of anorexia nervosa in adolescents and young adults.",
   "Polymyositis is a chronic autoimmune disease that presents with symmetrical progressive proximal muscle weakness.",
   "Progressive myoclonic epilepsies (PMEs) are a group of neurodegenerative disorders, predominantly affecting adolescents and, characterized by generalized worsening myoclonus epilepsies, ataxia, cognitive deficits, and dementia.",
   "Total knee arthroplasty (TKA) improves patient-reported function by alleviating joint pain, however the surgical trauma exacerbates already impaired muscle function, which leads to further muscle weakness and disability after surgery.",
   "The patient suffered from anorexia and epigastric pain for a month, and a local physician suspected a diagnosis of gastric ulcer.",
]

# Load the MeSH terms from CSV file
mesh_csv_file = 'mesh_terms.csv'  # Ensure the correct file path and column name
mesh_terms = load_mesh_terms(mesh_csv_file)

# Initialize a list to store classification results
classification_results = []

# Visualize dependency trees and classify MeSH terms for each sentence
for idx, sentence in enumerate(sentences, 1):
    visualize_extract_classify_with_context(sentence, mesh_terms, idx, classification_results)

# Convert classification results to DataFrame for analysis
classification_df = pd.DataFrame(classification_results)

# Display the classification results
print("\nClassification Results:")
print(classification_df)



# import stanza
# import pandas as pd
# import networkx as nx
# import re

# # Initialize the Stanford NLP pipeline
# stanza.download('en')  # Download necessary models
# nlp = stanza.Pipeline('en')

# # Load the MeSH terms from a CSV and normalize to lowercase for matching
# def load_mesh_terms(csv_file):
#     mesh_df = pd.read_csv(csv_file)
#     return set(mesh_df['Mesh terms'].str.lower().tolist())  # Convert to lowercase for matching

# # Function to classify each MeSH term as either symptom or disease
# def classify_mesh_terms_stanza(sentence, found_terms):
#     doc = nlp(sentence)
#     term_classifications = {}
    
#     found_terms = [term.strip().lower() for term in found_terms.split(',')]
    
#     G = nx.DiGraph()
#     root_node = None

#     # Process the sentence using Stanza's dependency parser
#     for sent in doc.sentences:
#         for word in sent.words:
#             G.add_node(word.id, label=f"{word.text} ({word.upos})")
#             if word.head == 0:
#                 root_node = word.id
#             if word.head != 0:
#                 G.add_edge(word.head, word.id, label=word.deprel)

#         for term in found_terms:
#             term_word = None

#             # Match MeSH terms in the sentence
#             for word in sent.words:
#                 if re.fullmatch(r'\b' + re.escape(term) + r'\b', word.text.lower()):
#                     term_word = word
#                     break

#             # If the MeSH term is found, classify it as symptom or disease
#             if term_word:
#                 classification = None

#                 # Heuristics based on dependency relations
#                 if term_word.deprel in ['nsubj', 'amod', 'nmod', 'advmod']:
#                     # Closer to descriptors or subject, likely a symptom
#                     classification = 'Symptom'

#                 elif term_word.deprel in ['dobj', 'obl', 'iobj']:
#                     # Acting as an object, likely a disease
#                     classification = 'Disease'
                
#                 # Heuristics based on POS tags and specific keywords in the sentence
#                 if classification is None:
#                     if term_word.upos == 'ADJ':
#                         classification = 'Symptom'
#                     elif term_word.upos == 'NOUN':
#                         if 'pain' in sentence.lower() or any(x in sentence.lower() for x in ["caused by", "diagnosis", "treatment"]):
#                             classification = 'Disease'
#                         else:
#                             classification = 'Symptom'

#                 # Fallback: Use proximity to key medical verbs like "treatment", "diagnosed"
#                 if classification is None:
#                     if any(verb in sentence.lower() for verb in ["treated", "caused", "indicates"]):
#                         classification = 'Disease'
#                     else:
#                         classification = 'Symptom'

#                 # Save the classification
#                 term_classifications[term] = classification

#     return term_classifications

# # Load the sentences and MeSH terms from the CSV
# def classify_sentences_from_csv(csv_file):
#     df = pd.read_csv(csv_file)
#     classifications = {}

#     for idx, row in df.iterrows():
#         pmid, sentence, found_terms = row['PMID'], row['Sentence'], row['Found Terms']
#         classifications[pmid] = classify_mesh_terms_stanza(sentence, found_terms)

#     return classifications

# # Example usage
# csv_file = 'om.csv'
# mesh_classifications = classify_sentences_from_csv(csv_file)

# # Output the results for review
# for pmid, classification in mesh_classifications.items():
#     print(f"PMID: {pmid}, Classifications: {classification}")



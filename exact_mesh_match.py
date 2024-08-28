import os
import pandas as pd

# Load the disease terms from the mesh_disease_terms.csv file
disease_terms_df = pd.read_csv('mesh_disease_terms.csv')
disease_terms = disease_terms_df['Disease Name'].tolist()

relation_dir = 'relationships'

for symp_dir in os.listdir(relation_dir):
    symp_dir_path = os.path.join(relation_dir, symp_dir)
    print(symp_dir_path)
    if os.path.isdir(symp_dir_path):
        term_file = os.path.join(symp_dir_path, f'{symp_dir}.txt')
        term = " ".join(symp_dir.split('_'))
        if os.path.exists(term_file):
            with open(term_file, 'r') as file:
                extracted_terms = [line.strip() for line in file if line.strip()]

                similarity_scores = []
                for extracted_term in extracted_terms:
                    for disease_term in disease_terms:
                        
                        if extracted_term.lower() == disease_term.lower():
                            similarity_scores.append({
                                'extracted_term': extracted_term,
                                'disease_term': disease_term,
                            })


                # Convert the results to a DataFrame
                similarity_df = pd.DataFrame(similarity_scores)
                similarity_df = similarity_df.drop_duplicates()
                # Save the results to a CSV file
                similarity_df.to_csv(f'relationships/{symp_dir}/{symp_dir}_disease.csv', index=False)

                print("Similarity scores saved.")
import os
import pandas as pd
from difflib import SequenceMatcher

def calculate_similarity(term1, term2):
    # Calculate a similarity score using SequenceMatcher
    return SequenceMatcher(None, term1, term2).ratio()

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

                # # Combine both lists for TF-IDF vectorization
                # all_terms = extracted_terms + disease_terms

                # # Compute TF-IDF vectors for all terms
                # vectorizer = TfidfVectorizer().fit_transform(all_terms)
                # vectors = vectorizer.toarray()

                # # Compute cosine similarity between each extracted term and all disease terms
                # similarity_scores = []
                # for i, extracted_term in enumerate(extracted_terms):
                #     # Get the vector for the extracted term
                #     extracted_vector = vectors[i].reshape(1, -1)
                    
                #     # Compute cosine similarity with all disease terms
                #     similarities = cosine_similarity(extracted_vector, vectors[len(extracted_terms):])[0]
                    
                #     # Find the best matching disease term for each extracted term
                #     for j, sim_score in enumerate(similarities):
                #         if sim_score > 0.3:
                #             similarity_scores.append({
                #                 'extracted_term': extracted_term,
                #                 'disease_term': disease_terms[j],
                #                 'sim_score': sim_score
                #             })
                # Calculate similarity scores between each extracted term and all disease terms
                similarity_scores = []
                for extracted_term in extracted_terms:
                    for disease_term in disease_terms:
                        sim_score = calculate_similarity(extracted_term, disease_term)
                        if sim_score > 0.8:
                            similarity_scores.append({
                                'extracted_term': extracted_term,
                                'disease_term': disease_term,
                                'sim_score': sim_score
                            })


                # Convert the results to a DataFrame
                similarity_df = pd.DataFrame(similarity_scores)
                similarity_df = similarity_df.drop_duplicates()
                # Save the results to a CSV file
                similarity_df.to_csv(f'disease_overlap_score/{symp_dir}_scores.csv', index=False)

                print("Similarity scores saved.")
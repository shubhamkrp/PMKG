# import pandas as pd

# # File paths
# xls_file_path = 'rel.csv'
# csv_file_path = 'z.csv'
# umls_T047_path = 'umls_terms_T047.csv'  
# umls_T184_path = 'umls_terms_T184.csv'

# # Read the input .xls file and UMLS files
# df = pd.read_excel(xls_file_path)
# umls_T047 = pd.read_csv(umls_T047_path)  # Read UMLS T047 data (disease terms)
# umls_T184 = pd.read_csv(umls_T184_path)  # Read UMLS T184 data (symptom terms)

# # Rename columns for clarity if needed (assuming columns are 'cui' and 'term')
# umls_T047.rename(columns={'cui': 'disease_cui', 'term': 'disease_term'}, inplace=True)
# umls_T184.rename(columns={'cui': 'symptom_cui', 'term': 'symptom_term'}, inplace=True)

# # Merge the original DataFrame with UMLS term data based on CUI
# df = df.merge(umls_T047, on='disease_cui', how='left')
# df = df.merge(umls_T184, on='symptom_cui', how='left')

# # Save the result as a CSV file
# df.to_csv(csv_file_path, index=False)

# print(f"File with terms has been saved to {csv_file_path}")

import pandas as pd

# Load the main CSV file, symptom file, and disease file
main_df = pd.read_csv('rel.csv')  # The main file with symptom and disease CUIs
symptom_df = pd.read_csv('umls_terms_T184.csv')  # Contains 'cui' and 'term' columns for symptoms
disease_df = pd.read_csv('umls_terms_T047.csv')  # Contains 'cui' and 'term' columns for diseases

# Merge the main file with the symptom file on the 'symptom_cui' column
main_df = main_df.merge(symptom_df, left_on='symptom_cui', right_on='cui', how='left')
main_df.rename(columns={'term': 'symptom_name'}, inplace=True)

# Merge the resulting file with the disease file on the 'disease_cui' column
main_df = main_df.merge(disease_df, left_on='disease_cui', right_on='cui', how='left')
main_df.rename(columns={'term': 'disease_name'}, inplace=True)

# Drop the extra 'cui' columns
main_df.drop(columns=['cui_x', 'cui_y'], inplace=True)

# Group by 'symptom_cui' and 'disease_cui' to aggregate names with multiple CUIs
main_df = main_df.groupby(['symptom_cui', 'disease_cui'], as_index=False).agg({
    'symptom_name': lambda x: '; '.join(x.dropna().unique()),
    'disease_name': lambda x: '; '.join(x.dropna().unique())
})

# Save the result to a new CSV
main_df.to_csv('rel_updated.csv', index=False)

print("Updated CSV with symptom and disease names added.")

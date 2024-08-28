# import os
# import pandas as pd

# # Define file paths (update these paths to match your file locations)
# umls_dir = '/mnt/0C6C8FC06C8FA2D6/umls-2024AA-metathesaurus-full/2024AA/META'
# mrconso_path = os.path.join(umls_dir, 'MRCONSO.RRF')
# mrhier_path = os.path.join(umls_dir, 'MRHIER.RRF')

# # Load MRCONSO and MRHIER files into DataFrames
# mrconso_df = pd.read_csv(mrconso_path, sep='|', header=None, dtype=str)
# mrhier_df = pd.read_csv(mrhier_path, sep='|', header=None, dtype=str)

# # Define column names based on UMLS documentation
# mrconso_df.columns = [
#     'CUI', 'LAT', 'TS', 'LUI', 'STT', 'SUI', 'ISPREF', 'AUI', 'SAUI', 'SCUI', 
#     'SDUI', 'SAB', 'TTY', 'CODE', 'STR', 'SRL', 'SUPPRESS', 'CVF', '_'
# ]
# mrhier_df.columns = [
#     'CUI', 'AUI', 'CXN', 'PAUI', 'SAB', 'REL', 'PTR', 'HCD', 'CVF', '_'
# ]

# # Filter MRHIER for MeSH entries (SAB == 'MSH') and Tree Numbers starting with 'C'
# mesh_hier_df = mrhier_df[mrhier_df['SAB'] == 'MSH']
# c_branch_hier_df = mesh_hier_df[mesh_hier_df['HCD'].str.startswith('C')]

# # Extract CUIs for the C branch
# c_branch_cuis = c_branch_hier_df['CUI'].unique()

# # Filter MRCONSO for entries matching these CUIs
# c_branch_concepts_df = mrconso_df[mrconso_df['CUI'].isin(c_branch_cuis)]

# # Save results to a CSV file
# c_branch_concepts_df.to_csv('c_branch_diseases.csv', index=False)



import xml.etree.ElementTree as ET
import csv

# Load the XML file
tree = ET.parse('desc2024.xml')
root = tree.getroot()

# Set the branch ID prefix for diseases (e.g., 'C' for all diseases)
branch_id = 'C'

# Open a CSV file for writing
with open('mesh_disease_terms.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    # Write the header
    csvwriter.writerow(['Tree Number', 'Disease Name'])

    # Iterate through the MeSH terms
    for record in root.findall('.//DescriptorRecord'):
        descriptor_name = record.find('.//DescriptorName/String').text
        tree_numbers = [tn.text for tn in record.findall('.//TreeNumber')]

        # Filter by the 'C' branch ID
        for tree_number in tree_numbers:
            if tree_number.startswith(branch_id):
                csvwriter.writerow([tree_number, descriptor_name])

print("MeSH disease terms saved to 'mesh_disease_terms.csv'")


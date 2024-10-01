
# import pandas as pd

# # Paths to your UMLS files
# mrsty_file = '/mnt/0C6C8FC06C8FA2D6/umls-2024AA-metathesaurus-full/2024AA/META/MRSTY.RRF'
# mrconso_file = '/mnt/0C6C8FC06C8FA2D6/umls-2024AA-metathesaurus-full/2024AA/META/MRCONSO.RRF'
# mrsab_file = '/mnt/0C6C8FC06C8FA2D6/umls-2024AA-metathesaurus-full/2024AA/META/MRSAB.RRF'

# # Load MRSTY.RRF (Semantic Types)
# mrsty_columns = ['CUI', 'TUI', 'STN', 'STY', 'ATUI', 'CVF', 'EXTRA']
# mrsty = pd.read_csv(mrsty_file, sep='|', header=None, names=mrsty_columns, dtype=str)

# # Filter for T047 (Disease terms)
# t047_cuis = mrsty[mrsty['TUI'] == 'T047']['CUI'].unique()

# # Load MRCONSO.RRF (Concept Information)
# mrconso_columns = ['CUI', 'LAT', 'TS', 'LUI', 'STT', 'SUI', 'ISPREF', 'AUI', 'SAUI', 'SCUI', 'SDUI', 'SAB', 'TTY', 'CODE', 'STR', 'SRL', 'SUPPRESS', 'CVF', 'EXTRA']
# mrconso = pd.read_csv(mrconso_file, sep='|', header=None, names=mrconso_columns, dtype=str)

# # Filter MRCONSO for CUIs that match T047 terms
# t047_terms = mrconso[mrconso['CUI'].isin(t047_cuis)]

# # Load MRSAB.RRF (Source Vocabularies)
# mrsab_columns = ['VCUI', 'RCUI', 'VSAB', 'RSAB', 'SON', 'SF', 'SVER', 'VSTART', 'VEND', 'IMETA', 'RMETA', 'SLC', 'SRL', 'TFR', 'CFR', 'TTV', 'CTV', 'VSID', 'SYNONYM', 'HW', 'LAT', 'CENC', 'CURVER', 'SABIN', 'SSN', 'SCIT', 'EXTRA']
# mrsab = pd.read_csv(mrsab_file, sep='|', header=None, names=mrsab_columns, dtype=str)

# # Check unique values in SAB and VSAB for diagnosis
# print("Unique SAB values in MRCONSO:")
# print(t047_terms['SAB'].unique())
# print("\nUnique VSAB values in MRSAB:")
# print(mrsab['VSAB'].unique())

# # Convert both columns to uppercase to avoid case sensitivity issues
# t047_terms['SAB'] = t047_terms['SAB'].str.upper()
# mrsab['VSAB'] = mrsab['VSAB'].str.upper()

# # Merge T047 terms with their corresponding source vocabularies
# t047_terms_with_source = pd.merge(t047_terms, mrsab[['VSAB', 'SON']], left_on='SAB', right_on='VSAB', how='left')

# # Final columns: CUI (Concept Unique Identifier), Source Vocabulary (SON), Source Code (CODE), Term String (STR)
# final_df = t047_terms_with_source[['CUI', 'SON', 'CODE', 'STR']]

# # Save results to CSV
# final_df.to_csv('umls_t047_disease_terms_with_sources.csv', index=False)

# # Display the first few rows of the final DataFrame
# print(final_df.head())
# print("\nCount of NaN values in SON column:")
# print(final_df['SON'].isna().sum())



# import csv
# from collections import defaultdict
# import matplotlib.pyplot as plt

# # File paths - update these to match your UMLS data directory
# mrsty_file = '/mnt/0C6C8FC06C8FA2D6/umls-2024AA-metathesaurus-full/2024AA/META/MRSTY.RRF'
# mrconso_file = '/mnt/0C6C8FC06C8FA2D6/umls-2024AA-metathesaurus-full/2024AA/META/MRCONSO.RRF'
# output_file = 'umls_t047_distribution.csv'

# # Step 1: Extract all CUIs with semantic type T047
# t047_cuis = set()
# with open(mrsty_file, 'r') as f:
#     for line in f:
#         parts = line.strip().split('|')
#         if len(parts) >= 2:
#             cui, sty = parts[:2]
#             if sty == 'T047':
#                 t047_cuis.add(cui)

# print(f"Found {len(t047_cuis)} unique CUIs with semantic type T047")

# if len(t047_cuis) == 0:
#     print("No T047 CUIs found. Please check the MRSTY.RRF file and its path.")
#     exit()

# # Step 2: Extract source vocabulary information for T047 CUIs
# t047_info = defaultdict(lambda: defaultdict(set))

# with open(mrconso_file, 'r') as f:
#     for line in f:
#         parts = line.strip().split('|')
#         if len(parts) >= 13:
#             cui, lang, ts, lui, stt, sui, ispref, aui, saui, scui, sdui, sab, tty = parts[:13]
#             code = parts[13] if len(parts) > 13 else ''
#             str_ = parts[14] if len(parts) > 14 else ''
            
#             if cui in t047_cuis:
#                 t047_info[cui][sab].add((code, str_))

# # Step 3: Write results to a CSV file
# output_file = 'umls_t047_distribution.csv'

# with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(['CUI', 'Source', 'Source ID', 'Term'])

#     for cui, sources in t047_info.items():
#         for sab, codes_and_terms in sources.items():
#             for code, term in codes_and_terms:
#                 csvwriter.writerow([cui, sab, code, term])

# print(f"Results written to {output_file}")

# # Optional: Print some statistics
# source_counts = defaultdict(int)
# for sources in t047_info.values():
#     for sab in sources:
#         source_counts[sab] += 1

# print("\nTop 10 sources by number of T047 concepts:")
# for sab, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
#     print(f"{sab}: {count}")

# # Print sample of the data
# print("\nSample of extracted data:")
# for cui in list(t047_info.keys())[:5]:
#     for sab in list(t047_info[cui].keys())[:2]:
#         for code, term in list(t047_info[cui][sab])[:1]:
#             print(f"CUI: {cui}, Source: {sab}, Code: {code}, Term: {term}")



# # Prepare data for visualization
# source_counts = defaultdict(int)
# for sources in t047_info.values():
#     for sab in sources:
#         source_counts[sab] += 1

# # Sort sources by count
# sorted_sources = sorted(source_counts.items(), key=lambda x: x[1], reverse=True)

# # Prepare data for top 15 sources
# top_15_sources = sorted_sources[:15]
# other_count = sum(count for _, count in sorted_sources[15:])

# labels = [sab for sab, _ in top_15_sources] + ['Other']
# sizes = [count for _, count in top_15_sources] + [other_count]

# # Create a bar chart
# plt.figure(figsize=(12, 6))
# plt.bar(labels, sizes)
# plt.title('Distribution of T047 Concepts Across Top 15 Sources')
# plt.xlabel('Source')
# plt.ylabel('Number of Concepts')
# plt.xticks(rotation=45, ha='right')
# plt.tight_layout()
# plt.savefig('t047_distribution_bar.png')
# plt.close()

# # Create a pie chart
# plt.figure(figsize=(10, 10))
# plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
# plt.title('Distribution of T047 Concepts Across Sources')
# plt.axis('equal')
# plt.tight_layout()
# plt.savefig('t047_distribution_pie.png')
# plt.close()

# print("Visualizations saved as 't047_distribution_bar.png' and 't047_distribution_pie.png'")

# # Optional: Print some additional statistics
# total_concepts = sum(sizes)
# print(f"\nTotal number of T047 concepts: {total_concepts}")
# print(f"Number of unique sources: {len(source_counts)}")
# print("\nTop 5 sources:")
# for sab, count in sorted_sources[:5]:
#     percentage = (count / total_concepts) * 100
#     print(f"{sab}: {count} concepts ({percentage:.2f}%)")


import csv
from collections import defaultdict
import matplotlib.pyplot as plt

# File paths - update these to match your UMLS data directory
mrsty_file = '/mnt/0C6C8FC06C8FA2D6/umls-2024AA-metathesaurus-full/2024AA/META/MRSTY.RRF'
mrconso_file = '/mnt/0C6C8FC06C8FA2D6/umls-2024AA-metathesaurus-full/2024AA/META/MRCONSO.RRF'
output_file = 'umls_t047_distribution.csv'

# Step 1: Extract all CUIs with semantic type T047
t047_cuis = set()
with open(mrsty_file, 'r') as f:
    for line in f:
        parts = line.strip().split('|')
        if len(parts) >= 2:
            cui, sty = parts[:2]
            if sty == 'T047':
                t047_cuis.add(cui)

print(f"Found {len(t047_cuis)} unique CUIs with semantic type T047")

if len(t047_cuis) == 0:
    print("No T047 CUIs found. Please check the MRSTY.RRF file and its path.")
    exit()

# Step 2: Extract source vocabulary information for T047 CUIs
t047_info = defaultdict(lambda: defaultdict(set))

with open(mrconso_file, 'r') as f:
    for line in f:
        parts = line.strip().split('|')
        if len(parts) >= 13:
            cui, lang, ts, lui, stt, sui, ispref, aui, saui, scui, sdui, sab, tty = parts[:13]
            code = parts[13] if len(parts) > 13 else ''
            str_ = parts[14] if len(parts) > 14 else ''
            
            if cui in t047_cuis:
                t047_info[cui][sab].add((code, str_))

# Step 3: Write results to a CSV file
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['CUI', 'Source', 'Source ID', 'Term'])

    for cui, sources in t047_info.items():
        for sab, codes_and_terms in sources.items():
            for code, term in codes_and_terms:
                csvwriter.writerow([cui, sab, code, term])

print(f"Results written to {output_file}")

# Prepare data for visualization
source_counts = defaultdict(int)
for sources in t047_info.values():
    for sab in sources:
        source_counts[sab] += 1

# Sort sources by count
sorted_sources = sorted(source_counts.items(), key=lambda x: x[1], reverse=True)

# Create a horizontal bar chart for all sources
plt.figure(figsize=(15, max(8, len(sorted_sources) * 0.3)))  # Adjust height based on number of sources
y_pos = range(len(sorted_sources))
sources = [sab for sab, _ in sorted_sources]
counts = [count for _, count in sorted_sources]

bars = plt.barh(y_pos, counts)
plt.yticks(y_pos, sources)
plt.xlabel('Number of Concepts')
plt.title('Distribution of T047 Concepts Across All Sources')

# Add count labels to the end of each bar
for i, bar in enumerate(bars):
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2, f'{counts[i]}', 
             ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('t047_distribution_all_sources.png', dpi=300, bbox_inches='tight')
plt.close()

print("Visualization saved as 't047_distribution_all_sources.png'")

# Print all sources with their counts
print("\nAll sources and their concept counts:")
for sab, count in sorted_sources:
    print(f"{sab}: {count}")

# Print some additional statistics
total_concepts = sum(counts)
print(f"\nTotal number of T047 concepts: {total_concepts}")
print(f"Number of unique sources: {len(source_counts)}")
print("\nTop 5 sources:")
for sab, count in sorted_sources[:5]:
    percentage = (count / total_concepts) * 100
    print(f"{sab}: {count} concepts ({percentage:.2f}%)")


import csv
from collections import defaultdict
import matplotlib.pyplot as plt

# File paths - update these to match your UMLS data directory
mrsty_file = '/mnt/0C6C8FC06C8FA2D6/umls-2024AA-metathesaurus-full/2024AA/META/MRSTY.RRF'
mrconso_file = '/mnt/0C6C8FC06C8FA2D6/umls-2024AA-metathesaurus-full/2024AA/META/MRCONSO.RRF'
output_file = 'umls_t184_distribution.csv'

# Step 1: Extract all CUIs with semantic type t184
t184_cuis = set()
with open(mrsty_file, 'r') as f:
    for line in f:
        parts = line.strip().split('|')
        if len(parts) >= 2:
            cui, sty = parts[:2]
            if sty == 'T184':
                t184_cuis.add(cui)

print(f"Found {len(t184_cuis)} unique CUIs with semantic type T184")

if len(t184_cuis) == 0:
    print("No T184 CUIs found. Please check the MRSTY.RRF file and its path.")
    exit()

# Step 2: Extract source vocabulary information for T184 CUIs
t184_info = defaultdict(lambda: defaultdict(set))

with open(mrconso_file, 'r') as f:
    for line in f:
        parts = line.strip().split('|')
        if len(parts) >= 13:
            cui, lang, ts, lui, stt, sui, ispref, aui, saui, scui, sdui, sab, tty = parts[:13]
            code = parts[13] if len(parts) > 13 else ''
            str_ = parts[14] if len(parts) > 14 else ''
            
            if cui in t184_cuis:
                t184_info[cui][sab].add((code, str_))

# Step 3: Write results to a CSV file
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['CUI', 'Source', 'Source ID', 'Term'])

    for cui, sources in t184_info.items():
        for sab, codes_and_terms in sources.items():
            for code, term in codes_and_terms:
                csvwriter.writerow([cui, sab, code, term])

print(f"Results written to {output_file}")

# Prepare data for visualization
source_counts = defaultdict(int)
for sources in t184_info.values():
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
plt.title('Distribution of T184 Concepts Across All Sources')

# Add count labels to the end of each bar
for i, bar in enumerate(bars):
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2, f'{counts[i]}', 
             ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('t184_distribution_all_sources.png', dpi=300, bbox_inches='tight')
plt.close()

print("Visualization saved as 't184_distribution_all_sources.png'")

# Print all sources with their counts
print("\nAll sources and their concept counts:")
for sab, count in sorted_sources:
    print(f"{sab}: {count}")

# Print some additional statistics
total_concepts = sum(counts)
print(f"\nTotal number of T184 concepts: {total_concepts}")
print(f"Number of unique sources: {len(source_counts)}")
print("\nTop 5 sources:")
for sab, count in sorted_sources[:5]:
    percentage = (count / total_concepts) * 100
    print(f"{sab}: {count} concepts ({percentage:.2f}%)")


import json, time
from icd10_vector_db import model, index, icd10_terms


# Step 4: Query the Database
def search_icd10(query, k=5):
    query_embedding = model.encode([query]).astype('float32')
    D, I = index.search(query_embedding, k)
    neighbors_list=[]
    
    for i in range(len(I[0])):
        res=icd10_terms[I[0][i]]
        res+=" - " + str(D[0][i])
        # print(res)
        neighbors_list.append(res)
    return neighbors_list

# Step 4: Batch Processing for Queries
def batch_search_icd10(query_terms, batch_size=100, k=5):
    results = []
    for i in range(0, len(query_terms), batch_size):
        batch_queries = query_terms[i:i + batch_size]
        batch_embeddings = model.encode(batch_queries).astype('float32')
        D, I = index.search(batch_embeddings, k)
        batch_results = [[icd10_terms[idx] for idx in indices] for indices in I]
        results.extend(batch_results)
    return results

#step5: load queries from other_related_terms.json
def load_queries_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

json_file_path = 'OUTPUT/all_terms.json'

queries_dict = load_queries_from_json(json_file_path)
# print(queries_dict)

start_time = time.time()

results_dict = {}

# # Search and collect results for each query
# for category, queries in queries_dict.items():
#     category_results = {}
#     for query in queries:
#         results = search_icd10(query)
#         category_results[query] = results
#     results_dict[category] = category_results

# Search and collect results for each query
for category, queries in queries_dict.items():
    category_results = []
    for query in queries:
        results = search_icd10(query,k=1)
        category_results.extend(results)
    results_dict[category] = category_results

search_time = time.time() - start_time
# Step 6: Save results to JSON file
output_json_file_path = 'OUTPUT/temp.json'
with open(output_json_file_path, 'w') as outfile:
    json.dump(results_dict, outfile, indent=4)

print(f"Results saved to {output_json_file_path}")

# query_terms = ["Recurrence","Blindness","Quality of Life","Eye, Artificial","Feeding Behavior","Characidae","Corneal Diseases","Corneal Transplantation","Cornea","Prostheses and Implants","Autoimmune Diseases","Uveitis","Visual Acuity","Glaucoma","Intraocular Pressure","Quality of Life","Laser Therapy","Visually Impaired Persons","Touch","Hand Strength","Genetic Therapy","Blindness","CRISPR-Cas Systems","Gene Editing","Blindness","Deaf-Blind Disorders","Communication","Pan troglodytes","Ape Diseases","Mycobacterium tuberculosis","Blindness","Meningoencephalitis","Allergy and Immunology","Books","Art","Allergy and Immunology","Blindness, Cortical","Vertebroplasty","Retinitis Pigmentosa","Sexual Behavior","Blindness","Employment","Hemianopsia","Positron-Emission Tomography","Fluorodeoxyglucose F18","Visual Cortex","Glucose","Blindness","Magnetic Resonance Imaging","Entorhinal Cortex","Brain Mapping","Cataract Extraction","Parks, Recreational","Social Class","Motivation","Popular Culture","Global Burden of Disease","Blood Glucose","Glaucoma","Uveitis","Cornea","Keratitis","Blindness","Mental Disorders","Diabetes Mellitus","Diabetic Retinopathy","Usher Syndromes","Hearing Loss, Sensorineural","Postoperative Complications","Blindness","Blindness","Touch Perception","Theft","Attention","Wolfram Syndrome","Endocrinology","Trigeminal Neuralgia","Nerve Block","Characidae","Carpal Tunnel Syndrome","Shoulder","Trust","Blindness","Medically Underserved Area","Task Shifting","Blindness","Cataract","Glaucoma, Open-Angle","Cataract Extraction"] * 2000  # 10,000 queries


# results = batch_search_icd10(query_terms, batch_size=100)
# search_time = time.time() - start_time

# Display execution times
print(f"Time taken to search query terms: {search_time:.2f} seconds")

# Display results for the first few queries (optional)
# for i, query in enumerate(query_terms[:5]):
#     print(f"Search results for query '{query}':")
#     for result in results[i]:
#         print(result)
#     print()


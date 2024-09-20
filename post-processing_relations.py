import json
import re

# Function to convert the JSON format
def convert_json(data):
    for condition in data:
        for item in data[condition]:
            # Split the 'disease' field into code, description, and distance
            disease_info = re.split(r' - ', item['disease'])
            item['disease_code'] = disease_info[0]
            item['disease_desc'] = disease_info[1]
            item['euclidean_distance'] = float(disease_info[2])
            # Convert pos_weight to an integer if needed, else keep it as a string
            item['pos_weight'] = int(item['pos_weight']) // 18  # Example transformation
            # Remove the original 'disease' field
            del item['disease']
    return data

# Load the input JSON file
with open('mapped_terms_icd9.json', 'r') as infile:
    data = json.load(infile)

# Process the JSON data
processed_data = convert_json(data)

# Write the processed data to a new JSON file
with open('output.json', 'w') as outfile:
    json.dump(processed_data, outfile, indent=4)

print("Processing complete. The output has been saved to 'output.json'.")


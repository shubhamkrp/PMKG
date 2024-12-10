import json
import os

# Prepare the JSONL format for Pyserini
def prepare_jsonl(data, output_jsonl):
    with open(output_jsonl, 'a', encoding='utf-8') as f:
        for article in data:
            doc = {
                'id': article['PMID'],
                'contents': f"{article['Title']} {article['Abstract']}"
            }
            f.write(json.dumps(doc) + '\n')

# Load the data from JSON and convert to JSONL format
input_json = '/mnt/0C6C8FC06C8FA2D6/output/json/'
output_jsonl = '/mnt/0C6C8FC06C8FA2D6/pubmed_data.jsonl'


for i in range(1, 1220):
    file_number = str(i).zfill(4)
    json_file = os.path.join(input_json, f'pubmed24n{file_number}.json')

    if os.path.exists(json_file):
        print(f'Processing {json_file}...')

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract data from the current file
        file_data = prepare_jsonl(data,output_jsonl)

    else:
        print(f'{json_file} does not exist. Skipping...')


print(f"Data saved in JSONL format: {output_jsonl}")

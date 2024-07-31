import pandas as pd

symptom_file="mesh_symptoms.csv"
symptom_df=pd.read_csv(symptom_file, delimiter=';')

#select name column
column_name="Name"
symptom_term=symptom_df[column_name]

processed_lines = []
for line in symptom_term:
    # Append the processed line to the list, followed by a colon
    processed_lines.append(f"{line}:")

with open('ms.txt', 'w') as file:
    file.write('\n'.join(processed_lines))

print("File processed successfully.")
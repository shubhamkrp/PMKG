# Read input file
with open('icd10cm_codes.txt', 'r') as file:
    lines = file.readlines()

# Process each line
processed_lines = []
for line in lines:
    # Split the line by spaces and remove the first element (the code)
    processed_line = ' '.join(line.split()[1:])
    # Append the processed line to the list, followed by a colon
    processed_lines.append(f"{processed_line}:")

# Write the processed lines to the output file
with open('output.txt', 'w') as file:
    file.write('\n'.join(processed_lines))

print("File processed successfully.")

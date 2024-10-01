
input_file_path = "icd9_cm_codes.txt"
output_file_path = "icd9_cm_names.csv"

with open(input_file_path, 'r', encoding='ISO-8859-1') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
    outfile.write("Description\n")  # Writing header for the CSV file
    for line in infile:
        # Split the line by whitespace after the code (the first word)
        parts = line.strip().split(maxsplit=1)
        if parts and len(parts) > 1:
            # Check if the first part is a number or starts with 'V'
            if parts[0][0].isdigit() or parts[0][0] == 'V' or parts[0][0] == 'E':
                # Write the second part (description) to the CSV file
                outfile.write(f"{parts[1]}\n")


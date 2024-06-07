import pandas as pd
import argparse
import os

def extract_name_from_terms(fname):
    data = open(fname, 'r', encoding="utf8")
    # print(data)

    df=pd.DataFrame(columns=["ids","name","connected_id","connected_name"])

    # Split data into individual terms
    terms = data.read().split("\n\n")
    # print(len(terms))

    # Process each term
    for term in terms:
        lines = term.split("\n")
        ids = None
        name = None
        connection = None
        for line in lines:
            if line.startswith("id:"):
                ids = ":".join(line.split(":")[1:]).strip()
            elif line.startswith("name:"):
                name = line.split(":")[1].strip()
            elif line.startswith("is_a:"):
                connection = ":".join(line.split(":")[1:]).strip()
                connection_split = connection.split("!")
                connected_id = connection_split[0].strip()
                connected_name = connection_split[1].strip()
                df.loc[len(df)]=[ids,name,connected_id,connected_name]
                break

    return df

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parse .obo file to find term name.')
    parser.add_argument('input_file', help='Input file path. File should be the *.obo file.')
    parser.add_argument('--output_dir', help='Directory to output files', default='.')
    parser.add_argument('output_file', help='Output file path. File should be in csv format.')
    args = parser.parse_args()

    output_fname = os.path.join(args.output_dir, args.output_file)

    extracted_data = extract_name_from_terms(args.input_file)
    if len(extracted_data)==0:
        raise Exception("An exception occurred since parsed entity is empty")
    
    extracted_data.to_csv(output_fname,sep="|",index=False)

    # # Save extracted names to a CSV file
    # with open(output_fname, "w", newline="") as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(["Name"])
    #     for name in extracted_names:
    #         writer.writerow([name])

    print(f"Extracted terms saved to {output_fname}")


#########---------USAGE-----------#############
#get_active_term_name.py [-h] [--output_dir OUTPUT_DIR] input_file output_file
###############################################
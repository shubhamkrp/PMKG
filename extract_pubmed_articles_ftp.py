# import os
# import gzip
# import shutil
# import csv
# import requests
# from xml.etree import ElementTree as ET

# # URL for the Medline baseline data FTP directory
# BASELINE_URL = "https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/"

# # Function to download and extract the XML files
# def download_and_extract_file(url, output_dir):
#     local_filename = os.path.join(output_dir, url.split("/")[-1])
    
#     # Download the file
#     with requests.get(url, stream=True) as r:
#         r.raise_for_status()
#         with open(local_filename, 'wb') as f:
#             shutil.copyfileobj(r.raw, f)
    
#     # Decompress the file if it's a .gz
#     if local_filename.endswith('.gz'):
#         with gzip.open(local_filename, 'rb') as f_in:
#             with open(local_filename[:-3], 'wb') as f_out:
#                 shutil.copyfileobj(f_in, f_out)
    
#     # Return the path to the extracted XML file
#     return local_filename[:-3] if local_filename.endswith('.gz') else local_filename

# # Function to process a single XML file
# def process_xml_file(file_path, csvwriter):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         context = ET.iterparse(file, events=("end",))
#         for event, elem in context:
#             if elem.tag == 'PubmedArticle':
#                 try:
#                     pmid = elem.find('.//PMID').text
#                     title_elem = elem.find('.//ArticleTitle')
#                     abstract_elem = elem.find('.//Abstract/AbstractText')

#                     title = title_elem.text if title_elem is not None else "No Title"
#                     abstract = abstract_elem.text if abstract_elem is not None else "No Abstract"
                    
#                     csvwriter.writerow({
#                         "PMID": pmid,
#                         "Title": title,
#                         "Abstract": abstract
#                     })
#                 except Exception as e:
#                     print(f"Error processing element: {e}")
                
#                 elem.clear()  # Clear the element to free up memory

# # Main function to download, extract, and process the files
# def download_and_process_baseline_files(output_dir="medline_data", csv_file="ftp_pubmed_articles.csv"):
#     # Create output directory if it doesn't exist
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
    
#     # Get the list of files from the FTP server
#     response = requests.get(BASELINE_URL)
#     files = response.text.splitlines()
#     xml_files = [line.split()[-1] for line in files if line.endswith('.gz')]

#     # Open CSV file for writing
#     with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
#         csvwriter = csv.DictWriter(csvfile, fieldnames=["PMID", "Title", "Abstract"])
#         csvwriter.writeheader()

#         # Download, extract, and process each file
#         for xml_file in xml_files:
#             try:
#                 print(f"Processing file: {xml_file}")
#                 xml_path = download_and_extract_file(BASELINE_URL + xml_file, output_dir)
#                 process_xml_file(xml_path, csvwriter)
#                 os.remove(xml_path)  # Remove the decompressed XML file to save space
#             except Exception as e:
#                 print(f"Error processing file {xml_file}: {e}")

#     print("Processing complete! Articles saved in 'ftp_pubmed_articles.csv'.")

# # Run the main processing function
# download_and_process_baseline_files()


import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL of the page containing the links
url = 'https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/'

# Destination folder to save the downloaded files
destination_folder = 'medline_data'

# Create the folder if it doesn't exist
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Send a GET request to the URL
response = requests.get(url)
response.raise_for_status()  # Raise an error for bad status codes

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Find all <a> tags
links = soup.find_all('a')

# Download each XML link
for link in links:
    href = link.get('href')
    if href and (href.endswith('.xml') or 'xml' in href):
        full_url = urljoin(url, href)  # Handle relative URLs
        file_name = os.path.join(destination_folder, os.path.basename(full_url))
        print(f'Downloading {full_url} to {file_name}')
        try:
            file_response = requests.get(full_url)
            file_response.raise_for_status()
            with open(file_name, 'wb') as file:
                file.write(file_response.content)
            print(f'Successfully downloaded {file_name}')
        except requests.exceptions.RequestException as e:
            print(f'Failed to download {full_url}: {e}')

import requests
from bs4 import BeautifulSoup

# Define the base URL for the MeSH ASCII data
MESH_ASCII_BASE_URL = "https://www.nlm.nih.gov/databases/download/mesh.html"

# Send a request to the MeSH ASCII data page
response = requests.get(MESH_ASCII_BASE_URL)
response.raise_for_status()  # Raise an error if the request failed

# Parse the response HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Find the link to the MeSH ASCII data
ascii_link = soup.find("a", string="MeSH ASCII")
if ascii_link:
    ascii_url = ascii_link.get("href")
    print(f"Downloading MeSH ASCII data from: {ascii_url}")

    # Now you can download the ASCII data using the obtained URL
    # Add your code here to download and process the data
else:
    print("MeSH ASCII data link not found on the page.")

# Add your code to process the downloaded ASCII data (e.g., extract symptoms)
# ...

# Example: Print the first 10 lines of the downloaded data
# with open("mesh_ascii_data.txt", "r") as mesh_file:
#     for line in mesh_file.readlines()[:10]:
#         print(line.strip())


# Read the MeSH data from the ASCII file (replace with actual file path)
with open("mesh_ascii_data.txt", "r") as mesh_file:
    mesh_terms = [line.strip() for line in mesh_file.readlines()]

# Filter symptom-related terms
symptom_related_terms = []
for term in mesh_terms:
    # Example: Check if the term contains "symptom" or "sign"
    if "symptom" in term.lower() or "sign" in term.lower():
        symptom_related_terms.append(term)

# Print the symptom-related terms
print("Symptom-related MeSH terms:")
for term in symptom_related_terms:
    print(term)

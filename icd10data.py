import xml.etree.ElementTree as ET
import json

# Parse the XML file
tree = ET.parse('C:/Users/kumar/Downloads/icd10cm_tabular_2021.xml')
root = tree.getroot()

# Function to recursively convert XML to a dictionary
def xml_to_dict(element):
    node = {}
    if list(element):  # if the element has children
        for child in element:
            child_data = xml_to_dict(child)
            if child.tag in node:
                if isinstance(node[child.tag], list):
                    node[child.tag].append(child_data)
                else:
                    node[child.tag] = [node[child.tag], child_data]
            else:
                node[child.tag] = child_data
    else:
        node = element.text.strip() if element.text else None
    return node

# Convert the entire XML structure to a dictionary
xml_dict = xml_to_dict(root)

# Save the dictionary as a formatted JSON file
with open('icd10.json', 'w', encoding='utf-8') as json_file:
    json.dump(xml_dict, json_file, ensure_ascii=False, indent=4)

print("JSON file has been created successfully.")

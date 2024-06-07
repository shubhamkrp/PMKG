# # import networkx as nx
# # import matplotlib.pyplot as plt

# # # Read the data from the txt file
# # with open('icd10cm_codes.txt', 'r') as file:
# #     lines = file.readlines()

# # # Create a directed graph
# # G = nx.DiGraph()

# # # Function to add nodes and edges to the graph
# # def add_nodes_edges(G, lines):
# #     for line in lines:
# #         code, description = line.split(maxsplit=1)
# #         G.add_node(code, label=description.strip())
        
# #         # Establish hierarchy based on the first letter (for simplicity)
# #         parent_code = code[0]
# #         if parent_code != code:
# #             G.add_edge(parent_code, code)

# # # Add nodes and edges
# # add_nodes_edges(G, lines)

# # # Draw the graph
# # pos = nx.spring_layout(G)  # Layout for visualization
# # labels = nx.get_node_attributes(G, 'label')

# # plt.figure(figsize=(12, 8))
# # nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold', arrows=True)
# # plt.title("ICD10 Hierarchical Tree")
# # plt.show()




# import networkx as nx
# import matplotlib.pyplot as plt


# # Read data from the text file
# with open('icd10cm_codes.txt', 'r') as file:
#     data = file.read()

# # Parse the data into a dictionary
# lines = data.split('\n')
# diseases = {}
# for line in lines:
#     if line.strip():  # Skip any empty lines
#         parts = line.split(maxsplit=1)
#         diseases[parts[0]] = parts[1]

# # Function to create a hierarchical tree
# def create_hierarchical_tree(diseases):
#     G = nx.DiGraph()
    
#     # Add the root node
#     root = "Root"
#     G.add_node(root, label=root)
    
#     # Function to add edges based on hierarchical levels
#     def add_edges():
#         for code, name in diseases.items():
#             level1 = code[0]  # First letter
#             level2 = code[:3]  # First letter + two digits
            
#             # Add level 1 nodes
#             if not G.has_node(level1):
#                 G.add_node(level1, label=level1)
#                 G.add_edge(root, level1)
            
#             # Add level 2 nodes
#             if not G.has_node(level2):
#                 G.add_node(level2, label=level2)
#                 G.add_edge(level1, level2)
            
#             # Add leaf nodes
#             G.add_node(code, label=f"{code}\n{name}")
#             G.add_edge(level2, code)
    
#     # Build the hierarchical tree
#     add_edges()
    
#     return G

# # Create the graph
# G = create_hierarchical_tree(diseases)

# # Draw the graph
# pos = nx.spring_layout(G, seed=42)  # Fixed layout for consistency
# labels = nx.get_node_attributes(G, 'label')
# nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000, node_color='lightblue', font_size=8, font_color='black', font_weight='bold')
# plt.show()



# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import json
# import time

# def scrape_icd10_data(driver):
#     # Wait for the side panel to load
#     # WebDriverWait(driver, 10).until(
#     #     EC.presence_of_element_located((By.CSS_SELECTOR, ".treenode"))
#     # )

#     # Click to expand all nodes (if necessary)
#     expand_buttons = driver.find_elements(By.CSS_SELECTOR, ".expandcollapse")
#     for button in expand_buttons:
#         driver.execute_script("arguments[0].click();", button)
#         time.sleep(1)  # Wait for the UI to update

#     # Get the side panel content
#     side_panel = driver.find_element(By.ID, "ygtv1")
#     soup = BeautifulSoup(side_panel.get_attribute('innerHTML'), 'html.parser')

#     return soup

# def parse_icd10_node(node):
#     code = node.find('span', class_='code').text.strip()
#     description = node.find('span', class_='description').text.strip()
#     children = []

#     child_nodes = node.find_next_sibling('ul')
#     if child_nodes:
#         for child in child_nodes.find_all('li', recursive=False):
#             children.append(parse_icd10_node(child))

#     return {
#         'code': code,
#         'description': description,
#         'children': children
#     }

# def build_icd10_tree(soup):
#     root_nodes = soup.find_all('li', class_='treenode')
#     tree = []

#     for root in root_nodes:
#         tree.append(parse_icd10_node(root))

#     return tree

# def save_tree_to_json(tree, filename='icd10_tree.json'):
#     with open(filename, 'w', encoding='utf-8') as f:
#         json.dump(tree, f, indent=4, ensure_ascii=False)

# # Setup WebDriver
# driver = webdriver.Chrome()  # Ensure chromedriver is in your PATH
# driver.get("https://icd.who.int/browse10/2019/en")

# # Example usage
# soup = scrape_icd10_data(driver)
# icd10_tree = build_icd10_tree(soup)
# save_tree_to_json(icd10_tree)

# # Close the WebDriver
# driver.quit()


import simple_icd_10 as icd
from icdcodex import hierarchy
icd_10_cm_hierarchy, icd_10_cm_codes = hierarchy.icd10cm("2020")

print(icd_10_cm_hierarchy)

import networkx as nx
from networkx.algorithms.traversal.breadth_first_search import bfs_tree
import matplotlib.pyplot as plt

G = nx.relabel_nodes(icd_10_cm_hierarchy, {"root": "ICD-10-CM"})
# G_chapters = bfs_tree(G, "Certain infectious and parasitic diseases (A00-B99)", depth_limit=2)
# print(icd.get_description("C44.1"))
# plt.figure(figsize=(8,8))
# nx.draw(G_chapters, with_labels=True)
# plt.show()


# Step 2: Identify the root node
# A root node in a digraph can be a node with in-degree 0
root_nodes = [n for n in G.nodes if G.in_degree(n) == 0]

# Assuming the first root node found as the root
root = root_nodes[0] if root_nodes else None

if root is None:
    raise ValueError("No root node found (no node with in-degree 0).")

# Step 3: Create a hierarchical tree using BFS
T = nx.bfs_tree(G, root)

# Step 4: Visualize the hierarchical tree

def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    """
    If the graph is a tree, this function will return the positions to plot this in a
    hierarchical layout.
    """
    pos = _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
    return pos

def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=[]):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    children = list(G.neighbors(root))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        children.remove(parent)  
    if len(children) != 0:
        dx = width / len(children) 
        nextx = xcenter - width/2 - dx/2
        for child in children:
            nextx += dx
            pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, parent=root, parsed=parsed)
    return pos

# Generate positions
pos = hierarchy_pos(T, root)

# Draw the graph
plt.figure(figsize=(12, 12))
nx.draw(T, pos=pos, with_labels=True, node_size=50, font_size=10, arrows=False)
plt.show()




# from urllib.request import Request, urlopen
# from bs4 import BeautifulSoup as soup
# url = 'https://icd.who.int/browse10/2019/en#/I'
# req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})

# webpage = urlopen(req).read()
# page_soup = soup(webpage, "html.parser")
# # print(page_soup.prettify())
# # import requests
# # from bs4 import BeautifulSoup

# # url = "https://icd.who.int/browse10/2019/en"

# # response = requests.get(url)
# # parsed_rsponse = BeautifulSoup(response.text, "html.parser")
# # print(parsed_rsponse.prettify())

# with open('html_response.txt', 'w') as file:
#     data = file.write(page_soup.prettify())
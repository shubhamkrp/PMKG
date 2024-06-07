import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file with the specified delimiter
df = pd.read_csv('OUTPUT/sym_terms.csv', delimiter='|')

# Create an empty directed graph
G = nx.DiGraph()

# Add nodes and edges to the graph
for index, row in df.iterrows():
    child_id = row['ids'].strip()
    child_name = row['symptom_name'].strip()
    parent_id = row['connected_id'].strip()
    parent_name = row['connected_name'].strip()

    # Add parent node with name attribute
    if not G.has_node(parent_id):
        G.add_node(parent_id, id=parent_id, name=parent_name)
    
    # Add child node with name attribute
    if not G.has_node(child_id):
        G.add_node(child_id, id=child_id, name=child_name)
    
    # Add edge from parent to child
    G.add_edge(parent_id, child_id)

# # Optionally, display the graph's nodes and their attributes
# for node, data in G.nodes(data=True):
#     print(f"Node: {node}, Data: {data}")

# Function to generate tree layout positions
def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    """
    If the graph is a tree, this will return the positions to plot this in a
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

# Find the root node (assuming there's a single root)
root = [node for node, degree in G.in_degree() if degree == 0][0]

# Generate tree layout positions
pos = hierarchy_pos(G, root)

# Draw the graph as a tree
plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=False, arrows=True, node_size=700, node_color='skyblue')

# Draw node labels with names
node_labels = {node:f"{data['id']}\n{data['name']}" for node, data in G.nodes(data=True)}
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10)

# Display the tree
plt.title('Symptom Ontology Tree')
plt.show()


print("Total number of nodes in symptom ontology = ", len(G.nodes()))
leaf_nodes=[node for node in G.nodes() if G.in_degree(node)!=0 and G.out_degree(node)==0]
print("Number of leaf nodes = ", len(leaf_nodes))
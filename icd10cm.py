import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Function to load the graph from CSV
def load_graph_from_csv(csv_file):
    df = pd.read_csv(csv_file, delimiter='|')
    G = nx.DiGraph()

    for index, row in df.iterrows():
        parent_id = row['parent_id'].strip()
        child_info = row['child_id'].strip().split(';')
        child_id = child_info[0]
        child_description = child_info[1] if len(child_info) > 1 else ''
        
        if not G.has_node(parent_id):
            G.add_node(parent_id, id=parent_id, description='')
        
        if not G.has_node(child_id):
            G.add_node(child_id, id=child_id, description=child_description)
        
        G.add_edge(parent_id, child_id)
    
    return G

# Function to create hierarchical layout
def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    if root is None:
        root = next(iter(nx.topological_sort(G)))
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
        nextx = xcenter - width / 2 - dx / 2
        for child in children:
            nextx += dx
            pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, vert_loc=vert_loc-vert_gap,
                                 xcenter=nextx, pos=pos, parent=root, parsed=parsed)
    return pos

# Function to visualize the tree
def draw_hierarchical_tree(G, root):
    pos = hierarchy_pos(G, root)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=False, arrows=True, node_size=700, node_color='skyblue')

    node_labels = {node: f"{data['id']}\n{data['description']}" for node, data in G.nodes(data=True)}
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)

    plt.title('Hierarchical Tree of Disease Ontology')
    plt.show()

# Load the graph from CSV
graph = load_graph_from_csv('icd10_hierarchy.csv')

# Draw the hierarchical tree with the root being 'ICD10CM'
draw_hierarchical_tree(graph, 'ICD10CM')

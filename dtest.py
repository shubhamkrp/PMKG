import simple_icd_10_cm as cm
import networkx as nx
from networkx.algorithms.traversal.depth_first_search import dfs_tree
import matplotlib.pyplot as plt
from icdcodex import hierarchy
icd_10_cm_hierarchy, icd_10_cm_codes = hierarchy.icd10cm("2020")

G = nx.relabel_nodes(icd_10_cm_hierarchy, {"root": "ICD-10-CM"})
G_chapters = dfs_tree(G, "J45", depth_limit=2)
plt.figure(figsize=(8,8))
nx.draw(G_chapters, with_labels=True)
plt.show()

# parent, = G.predecessors("0010")
# print(f"parent: {parent}, siblings: {G[parent]}")

def get_siblings(code):
    siblings=cm.get_children(cm.get_parent(code))
    if len(siblings)==0:
        return "No Siblings"
    return siblings

def get_match(term):
    for i in range(len(all_codes)):
        match = cm.get_description(all_codes[i])
        if(match.strip().lower()==input_text.strip().lower()):
            print("name: ", match)
            print("code: ", all_codes[i])
            print(cm.get_ancestors(all_codes[i], prioritize_blocks=True))
            print(cm.get_parent(all_codes[i], prioritize_blocks=True))
            print(cm.get_children(all_codes[i]))
            # print(cm.get_full_data(all_codes[i]))
            print(cm.get_children(cm.get_parent(all_codes[i])))
            print(get_siblings(all_codes[i]))
            break

# print(cm.get_all_codes()[:5])
all_codes=cm.get_all_codes()
print(cm.get_description("A000"))
input_text=cm.get_description("A000")
for i in range(len(all_codes)):
    match = cm.get_description(all_codes[i])
    if(match.strip().lower()==input_text.strip().lower()):
        print("name: ", match)
        print("code: ", all_codes[i])
        print(cm.get_ancestors(all_codes[i], prioritize_blocks=True))
        print(cm.get_parent(all_codes[i], prioritize_blocks=True))
        print(cm.get_children(all_codes[i]))
        # print(cm.get_full_data(all_codes[i]))
        print(cm.get_children(cm.get_parent(all_codes[i])))
        print(get_siblings(all_codes[i]))
        break

print("last:", match)

# f = open("demofile2.txt", "a")
# f.write(str(all_codes))
# f.close()
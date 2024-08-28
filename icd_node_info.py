import simple_icd_10_cm as cm
# import networkx as nx
# from networkx.algorithms.traversal.depth_first_search import dfs_tree
# import matplotlib.pyplot as plt
# from icdcodex import hierarchy
# icd_10_cm_hierarchy, icd_10_cm_codes = hierarchy.icd10cm("2020")

# G = nx.relabel_nodes(icd_10_cm_hierarchy, {"root": "ICD-10-CM"})
# G_chapters = dfs_tree(G, "J45", depth_limit=2)
# plt.figure(figsize=(8,8))
# nx.draw(G_chapters, with_labels=True)
# plt.show()

# parent, = G.predecessors("0010")
# print(f"parent: {parent}, siblings: {G[parent]}")

def get_siblings(code):
    siblings=cm.get_children(cm.get_parent(code))
    if len(siblings)==0:
        return "No Siblings"
    return siblings

def get_match(term):
    f=0
    all_codes=cm.get_all_codes()
    for i in range(len(all_codes)):
        match = cm.get_description(all_codes[i])
        if(match.strip().lower()==term.strip().lower()):
            f=1
            print("name: ", match)
            print("code: ", all_codes[i])
            ancestors = cm.get_ancestors(all_codes[i], prioritize_blocks=True)
            print("Ancestors_id: ", ancestors)
            if len(ancestors)>0:
                ancestors_list=[]
                for a in ancestors:
                    ancestors_list.append(cm.get_description(a))
                print("Ancestors_name: ",ancestors_list)
            parent=cm.get_parent(all_codes[i], prioritize_blocks=True)
            print("Parent: ", parent, cm.get_description(parent))
            children=cm.get_children(all_codes[i])
            print("Children_id: ", children)
            if len(children)>0:
                children_list=[]
                for a in children:
                    children_list.append(cm.get_description(a))
                print("Children_name: ",children_list)
            # print(cm.get_full_data(all_codes[i]))
            siblings=get_siblings(all_codes[i])
            print("Siblings_id: ", siblings)
            if len(siblings)>0:
                siblings_list=[]
                for a in siblings:
                    siblings_list.append(cm.get_description(a))
                print("Siblings_name: ",siblings_list)
            break
    if f==0:
        print("Not found")

get_match("asthma")

# f = open("demofile2.txt", "a")
# f.write(str(all_codes))
# f.close()
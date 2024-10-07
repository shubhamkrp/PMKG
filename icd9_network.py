
from icd9 import ICD9

tree = ICD9('codes.json')

# list of top level codes (e.g., '001-139', ...)
toplevelnodes = tree.children
toplevelcodes = [node.code for node in toplevelnodes]
print('\t'.join(toplevelcodes))

# find all sub-nodes whose codes contain '001'
print(tree.search('001'))

# find sub-node with code '001.0'. Returns None if code is not found
print(tree.find('001.0'))

# get node's ICD9 code
print(tree.find('001.1').code)

# prints '001'
tree.find('001.1').parent.code

# prints '001'
tree.find('001').code

# get english description of ICD9 code
# prints: 'Cholera due to vibrio cholerae el tor'
tree.find('001.1').description

# prints: 'ROOT'
tree.description

# prints: 'Cholera'
tree.find('001.1').parent.description

# also prints: 'Cholera'
tree.find('001').description

# get node's children
tree.children

# search for '001.0' in root's first child
tree.children[0].search('001.0')

# get 001.0 node's parent.  None if node is a root
tree.find('001.0').parent

# get 001.0 node's parent path from the root.  Root node is the first element
tree.find('001.0').parents

# get all leaf nodes under root's first child
tree.children[0].leaves

# get all of 001.0 node's siblings that share the same parent
tree.find('001.0').siblings
import nltk

# Download the necessary NLTK resources
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

# Define the phrase
phrase = "Salmonella sepsis"

# Tokenize the phrase
tokens = nltk.word_tokenize(phrase)

# Perform POS tagging
tagged_tokens = nltk.pos_tag(tokens)

# Extract nouns from the tagged tokens
nouns = [word for word, pos in tagged_tokens if pos in ['NN']] #['NN', 'NNS', 'NNP', 'NNPS']]

print("Tagged Tokens:", tagged_tokens)
print("Nouns:", nouns)
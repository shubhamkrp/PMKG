from difflib import SequenceMatcher

def similar(a, b):
    similarity = SequenceMatcher(None, a, b).ratio()
    # print(f"Similarity ratio between '{a}' and '{b}': {similarity:.2f}")
    return similarity>=0.71


# import math
# import re
# from collections import Counter

# def get_cosine(vec1, vec2):
#     intersection = set(vec1.keys()) & set(vec2.keys())
#     numerator = sum([vec1[x] * vec2[x] for x in intersection])
#     sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
#     sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
#     denominator = math.sqrt(sum1) * math.sqrt(sum2)
#     if not denominator:
#         return 0.0
#     else:
#         return float(numerator) / denominator

# def text_to_vector(text):
#     words = re.findall(r"\w+", text.lower())
#     return Counter(words)

# def similar(d1,d2):
#     vector1 = text_to_vector(d1)
#     vector2 = text_to_vector(d2)

#     cosine_similarity = get_cosine(vector1, vector2)
#     print(f"Cosine similarity between '{d1}' and '{d2}': {cosine_similarity:.2f}")

###############ClinicalBertSimilarity###############
# from semantic_text_similarity.models import ClinicalBertSimilarity
# def similar(t1,t2):
#     model=ClinicalBertSimilarity(device="cpu")
#     # t1="sars-cov-2"
#     # t2="covid 19"
#     similarityScore=model.predict([(t1,t2)])
#     print(f"{similarityScore[0]:.4f}")
#     return similarityScore[0]>0.3

##################bio-bert#####################
# import torch
# from transformers import AutoTokenizer, AutoModel

# # Load the tokenizer and model
# tokenizer = AutoTokenizer.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
# model = AutoModel.from_pretrained("dmis-lab/biobert-base-cased-v1.1")

# def get_embedding(text, tokenizer, model):
#     # Tokenize input text
#     inputs = tokenizer(text, return_tensors="pt")
#     # Get the embeddings from the model
#     with torch.no_grad():
#         outputs = model(**inputs)
#     # Mean pooling to get a single vector representation of the text
#     embeddings = outputs.last_hidden_state.mean(dim=1)
#     return embeddings

# def cosine_similarity(vec1, vec2):
#     # Compute the cosine similarity between two vectors
#     return torch.nn.functional.cosine_similarity(vec1, vec2)

# def are_terms_similar(term1, term2, tokenizer, model, threshold=0.7):
#     # Get embeddings for both terms
#     embedding1 = get_embedding(term1, tokenizer, model)
#     embedding2 = get_embedding(term2, tokenizer, model)
#     # Compute similarity
#     similarity = cosine_similarity(embedding1, embedding2).item()
#     # Check if similarity is above the threshold
#     return similarity >= threshold, similarity

# def similar(t1,t2):
#     # similar, score = are_terms_similar(term1, term2, tokenizer, model)
#     # print(f"Are the terms '{term1}' and '{term2}' similar? {similar} (Score: {score:.2f})")
#     return are_terms_similar(t1,t2,tokenizer,model)[0]



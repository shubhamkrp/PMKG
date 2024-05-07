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

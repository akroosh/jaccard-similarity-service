from typing import List, Dict

from nltk.tokenize import RegexpTokenizer


def compute_jaccard_similarity(query_string: str, data: List[Dict]):
    query_string = RegexpTokenizer(r'\w+').tokenize(query_string)
    all_data = [set(RegexpTokenizer(r'\w+').tokenize(item["description"])) for item in data]

    similarities = []
    for item_set, item in zip(all_data, data):
        intersection = len(set(query_string).intersection(set(item_set)))
        union = len(set(query_string).union(set(item_set)))
        similarity = intersection / union
        similarities.append((item["id"], similarity))
    return similarities

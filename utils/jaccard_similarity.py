from typing import Dict, List

from nltk.tokenize import RegexpTokenizer


def tokenize_string(input_string: str) -> List[str]:
    """
    Tokenizes the input string by splitting it into individual words.

    Args:
        input_string (str): The input string to be tokenized.

    Returns:
        List[str]: A list of individual word tokens.
    """
    tokenizer = RegexpTokenizer(r"\w+")
    return tokenizer.tokenize(input_string)


def compute_jaccard_similarity(first_tokens_list: List[str], second_tokens_list: List[str]) -> float:
    """
    Computes the Jaccard similarity between two lists of tokens.

    Args:
        first_tokens_list (List[str]): The tokens of the first item.
        second_tokens_list (List[str]): The tokens of the second item.

    Returns:
        float: The Jaccard similarity score between the two token lists.
    """
    common_tokens = set(first_tokens_list).intersection(second_tokens_list)
    total_tokens = set(first_tokens_list).union(second_tokens_list)
    similarity = len(common_tokens) / len(total_tokens)
    return similarity


def compute_similarity_for_all_items(query_string: str, data: List[Dict]) -> List[tuple]:
    """
    Computes the Jaccard similarity between a query string and a list of data items.

    Args:
        query_string (str): The query string to compare against.
        data (List[Dict]): A list of data items, each containing a "description" field.

    Returns:
        List[tuple]: A list of tuples containing the item ID and its similarity score.
    """
    query_tokens = tokenize_string(query_string)
    data_tokens = [set(tokenize_string(item["description"])) for item in data]

    similarities = []
    for item_tokens, item in zip(data_tokens, data):
        similarity = compute_jaccard_similarity(query_tokens, item_tokens)
        similarities.append((item["id"], similarity))
    return similarities

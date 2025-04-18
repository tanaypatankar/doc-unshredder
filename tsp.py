import numpy as np
from PIL import Image
from functools import lru_cache
from matplotlib import pyplot as plt


def calculate_strip_similarity(strip1, strip2):
    """
    Calculate the similarity between two image strips.
    
    :param strip1: First image strip (PIL.Image)
    :param strip2: Second image strip (PIL.Image)
    :return: A similarity score (higher means more similar)
    """
    # Convert strips to numpy arrays for computation
    arr1 = np.array(strip1)
    arr2 = np.array(strip2)

    height = min(arr1.shape[0], arr2.shape[0])
    width = min(arr1.shape[1], arr2.shape[1])

    # w = np.zeros(width)
    # for i in range(width):
    #     if i < width // 2:
    #         w[i] = width // 2 - i
    #     else:
    #         w[i] = i - width // 2
    # w1 = 0
    # w2 = 0
    # for h in range(height):
    #     w1 += arr1[h, :, 0] * w + arr1[h, :, 1] * w + arr1[h, :, 2] * w
    #     w2 += arr2[h, :, 0] * w + arr2[h, :, 1] * w + arr2[h, :, 2] * w
        
    # w1 = np.sum(w1)
    # w2 = np.sum(w2)

    # # lesser is more similar
    # similarity = np.abs(w1 - w2) / (np.sqrt(np.sum(w1 ** 2)) + np.sqrt(np.sum(w2 ** 2)) + 1e-10)

    # Calculate the absolute difference between the two strips
    edge_a = arr1[:, -1]  # (height, 3)
    edge_b = arr2[:, 0]   # (height, 3)

    # Sum absolute channel differences over all pixels
    diff = np.abs(edge_b.astype(np.int16) - edge_a.astype(np.int16))  # (height, 3)
    # print(diff)
    score = np.sum(diff)  # scalar

    return score

def create_similarity_matrix(strips):
    """
    Create a similarity matrix from the list of image strips.

    :param strips: List of image strips (PIL.Image)
    :param calculate_strip_similarity: Function to compute similarity between two strips
    :return: A 2D list (matrix) where matrix[i][j] = similarity between strip i and strip j
    """
    n = len(strips)
    
    # Initialize matrix with zeros and +1 for padding the first row/column
    similarity_matrix = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(0, n):
        for j in range(0, n):  # fill lower triangle, skip first column
            sim = calculate_strip_similarity(strips[i], strips[j])
            similarity_matrix[i][j] = int(sim)
            # similarity_matrix[j][i] = int(sim)  # Optional: fill symmetrically
        # print(similarity_matrix[i])
        # input()
    return similarity_matrix

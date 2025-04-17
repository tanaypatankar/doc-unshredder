import numpy as np
from PIL import Image
import itertools
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

    w = np.zeros(width)
    for i in range(width):
        if i < width // 2:
            w[i] = width // 2 - i
        else:
            w[i] = i - width // 2
    w1 = 0
    w2 = 0
    for h in range(height):
        w1 += arr1[h, :, 0] * w + arr1[h, :, 1] * w + arr1[h, :, 2] * w
        w2 += arr2[h, :, 0] * w + arr2[h, :, 1] * w + arr2[h, :, 2] * w
        
    w1 = np.sum(w1)
    w2 = np.sum(w2)

    # lesser is more similar
    similarity = np.abs(w1 - w2) / (np.sqrt(np.sum(w1 ** 2)) + np.sqrt(np.sum(w2 ** 2)) + 1e-10)
    
    return similarity


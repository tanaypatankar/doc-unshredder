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

def create_graph(strips):
    """
    Create a graph of the strips based on their similarity.
    
    :param strips: List of image strips (PIL.Image)
    :return: A graph represented as a dictionary where keys are strip indices and values are lists of tuples (index, similarity)
    """
    graph = {i: [] for i in range(len(strips))}
    # Store calculated similarities to avoid redundant calculations
    # calculated_similarities = {}
    
    for i in range(len(strips)):
        for j in range(i+1, len(strips)):  # Only calculate for i < j
            # Calculate similarity only once
            similarity = calculate_strip_similarity(strips[i], strips[j])
            # Store the similarity in both directions
            graph[i].append((j, similarity))
            graph[j].append((i, similarity))
            # Store in our lookup dictionary
            # calculated_similarities[(i, j)] = similarity÷
            print(graph)



    return graph

def solve_tsp(graph):
    """
    Solve the Traveling Salesman Problem (TSP) using a brute-force approach.
    
    :param graph: A graph represented as a dictionary where keys are strip indices and values are lists of tuples (index, similarity)
    :return: The best path and its total similarity score
    """
    n = len(graph)
    best_path = None
    min_similarity = float('inf')

    # Generate all permutations of the strip indices
    for perm in itertools.permutations(range(n)):
        # Calculate the total similarity for this permutation
        total_similarity = 0
        for i in range(n-1):
            # Get the similarity between consecutive strips in the path
            current = perm[i]
            next_strip = perm[i+1]
            
            # Find the similarity between current and next strip
            # We need to search through the adjacency list
            for adj_idx, sim in graph[current]:
                if adj_idx == next_strip:
                    total_similarity += sim
                    break

        # Update best path if this one is better
        if total_similarity < min_similarity:
            min_similarity = total_similarity
            best_path = perm

    return best_path, min_similarity

def display_best_path(strips, best_path):
    """
    Display the best path of strips using matplotlib.
    
    :param strips: List of image strips (PIL.Image)
    :param best_path: The best path as a tuple of strip indices
    """
    # Create a figure to display the strips in the best path
    fig, axes = plt.subplots(1, len(best_path), figsize=(len(best_path) * 0.7, 2.5))

    # Ensure axes is iterable even if there is only one strip
    if len(best_path) == 1:
        axes = [axes]

    # Display each strip in its corresponding axis
    for ax, index in zip(axes, best_path):
        ax.imshow(strips[index])
        ax.axis('off')

    plt.show()
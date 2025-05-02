import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

def extract_edges(strips):
    """
    Precompute left and right edges as NumPy arrays (dtype int16 for subtraction).
    """
    left_edges = []
    right_edges = []
    for strip in strips:
        arr = np.array(strip).astype(np.int16)  # Convert once
        left_edges.append(arr[:, 0])            # Left edge (height, 3)
        right_edges.append(arr[:, -1])          # Right edge (height, 3)
    return left_edges, right_edges

def fast_strip_similarity(right_a, left_b):
    """
    Fast similarity based on pre-extracted edge arrays.
    """
    diff = np.abs(right_a - left_b)
    return int(np.sum(diff))

def create_similarity_matrix(strips):
    n = len(strips)
    similarity_matrix = [[0 for _ in range(n)] for _ in range(n)]

    left_edges, right_edges = extract_edges(strips)

    for i in tqdm(range(n), desc="Creating fast similarity matrix"):
        for j in range(n):
            if i == j:
                continue
            score = fast_strip_similarity(right_edges[i], left_edges[j])
            similarity_matrix[i][j] = score
    # subtract mac
    return similarity_matrix

def find_min_pair(matrix):
    min_value = float('inf')
    min_i = min_j = -1
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i != j and matrix[i][j] > 0 and matrix[i][j] < min_value:
                min_value = matrix[i][j]
                min_i, min_j = i, j
    return min_i, min_j, min_value

def find_best_right(matrix, left_index, used):
    min_value = float('inf')
    min_j = -1
    for j in range(len(matrix)):
        if j not in used and matrix[left_index][j] > 0 and matrix[left_index][j] < min_value:
            min_value = matrix[left_index][j]
            min_j = j
    return min_j, min_value

def find_best_left(matrix, right_index, used):
    min_value = float('inf')
    min_i = -1
    for i in range(len(matrix)):
        if i not in used and matrix[i][right_index] > 0 and matrix[i][right_index] < min_value:
            min_value = matrix[i][right_index]
            min_i = i
    return min_i, min_value

def reconstruct_strips(shreds, similarity_matrix):
    # Make a copy of the similarity matrix to avoid modifying the original
    sim_matrix = [row[:] for row in similarity_matrix]
    reconstructed = []

    # Step 1: Get initial best pair
    left_idx, right_idx, _ = find_min_pair(sim_matrix)
    
    if left_idx == -1 or right_idx == -1:
        return shreds  # No valid pairs found
        
    reconstructed = [shreds[left_idx], shreds[right_idx]]
    used = {left_idx, right_idx}

    for _ in tqdm(range(len(shreds) - 2), desc="Reconstructing image", mininterval=0.1):
        # Find the best strip to add to the left
        leftmost_idx = left_idx
        next_left_idx, left_val = find_best_left(sim_matrix, leftmost_idx, used)
        
        # Find the best strip to add to the right
        rightmost_idx = right_idx
        next_right_idx, right_val = find_best_right(sim_matrix, rightmost_idx, used)

        # If no valid extensions, break
        if next_left_idx == -1 and next_right_idx == -1:
            break

        # Choose the better of the two
        if next_left_idx != -1 and (next_right_idx == -1 or left_val <= right_val):
            # Prepend to the left
            reconstructed.insert(0, shreds[next_left_idx])
            used.add(next_left_idx)
            left_idx = next_left_idx
        elif next_right_idx != -1:
            # Append to the right
            reconstructed.append(shreds[next_right_idx])
            used.add(next_right_idx)
            right_idx = next_right_idx
    
    # If we haven't used all shreds, add them at the end (this is optional)
    remaining = [shreds[i] for i in range(len(shreds)) if i not in used]
    reconstructed.extend(remaining)
    
    return reconstructed


def reconstructed_image(strips, vertical=True):
    """
    Concatenate and display the list of image strips.
    :param strips: List of PIL.Image strips
    """
    if not strips:
        print("No strips to display")
        return
        
    # Ensure all strips have the same mode
    mode = strips[0].mode
    strips = [strip.convert(mode) if strip.mode != mode else strip for strip in strips]
    
    # Convert all strips to numpy arrays
    arrays = [np.array(strip) for strip in strips]

    # Concatenate along width (axis=1)
    full_image = np.concatenate(arrays, axis=1)

    if not vertical:
        # Rotate back to original orientation if needed
        full_image = np.rot90(full_image, k=3)

    return full_image

def show_reconstructed_image(image):
    """
    Display the reconstructed image.
    :param image: Reconstructed image as a NumPy array
    """
    plt.imshow(image)
    plt.axis('off')
    plt.show()
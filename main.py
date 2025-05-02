import os
import shredder
import tsp
import matplotlib.pyplot as plt
import numpy as np
from tsp_solver.greedy import solve_tsp


DEBUG = 0
IS_TSP = 1
IS_VERTICAL = 1

def calculate_accuracy(original, reconstructed):
    """
    Calculate accuracy of the reconstructed image against the original.
    Tries both direct and reversed reconstructed order.

    :param original: List of original (unshuffled) strips
    :param reconstructed: List of reconstructed strips
    :return: (accuracy %, best reconstructed order)
    """
    def count_correct_matches(orig, recon):
        count = 0
        for i in range(len(orig)):
            if i >= len(recon):
                break
            if np.array_equal(np.array(orig[i]), np.array(recon[i])):
                count += 1
        return count

    if len(original) != len(reconstructed):
        print(f"Warning: Length mismatch ({len(original)} vs {len(reconstructed)})")
        return 0.0, reconstructed

    correct_normal = count_correct_matches(original, reconstructed)
    reconstructed_reversed = list(reversed(reconstructed))
    correct_reversed = count_correct_matches(original, reconstructed_reversed)

    if correct_reversed > correct_normal:
        return (correct_reversed / len(original)) * 100.0, reconstructed_reversed
    else:
        return (correct_normal / len(original)) * 100.0, reconstructed

def display_shreds(shreds, isVertical):
    """
    Displays the shredded strips of an image using matplotlib.

    :param shreds: List of PIL.Image strips (shredded portions of the image).
    :param isVertical: Boolean flag indicating if the strips are vertical (True) or horizontal (False).
    """
    # Choose display layout based on vertical flag: 1 row for vertical strips, 1 column for horizontal strips
    if isVertical:
        fig, axes = plt.subplots(1, len(shreds), figsize=(len(shreds) * 0.7, 2.5))
    else:
        fig, axes = plt.subplots(len(shreds), 1, figsize=(6, len(shreds) * 0.3))

    # Ensure axes is iterable even if there is only one strip
    if len(shreds) == 1:
        axes = [axes]

    # Display each strip in its corresponding axis
    for ax, strip in zip(axes, shreds):
        ax.imshow(strip)
        ax.axis('off')

    plt.show()

def process_images(image_path, vertical=True, shuffle=True):
    """
    Shreds a single image and displays the shredded strips using matplotlib.

    :param image_path: Full path to the image file.
    :param vertical: Boolean flag indicating whether to create vertical strips (True) or horizontal strips (False).
    """
    # Shred the image into strips (vertical or horizontal)
    strips = shredder.shred_image(image_path, strip_size=1, vertical=vertical, shuffle=shuffle)
    
    if DEBUG:
        display_shreds(strips, vertical)

    return strips

def reconstruct_image_tsp(shreds):
    # 2. Find the best path using TSP solver
    best_path = solve_tsp(tsp_graph)
    if len(strips) in best_path:
        best_path.remove(len(strips))
    ordered_shreds = [strips[i] for i in best_path]
    return ordered_shreds

def reconstruct_image_heuristic(strips, tsp_graph):
    # 2. Use heurestic greedy algorithm to find the best path
    ordered_shreds = tsp.reconstruct_strips(strips, tsp_graph)
    return ordered_shreds

if __name__ == "__main__":
    # Input folder path containing the images to be processed
    input_folder = "./Input" 
    # Output folder path to save the reconstructed images
    output_folder = "./Output"

    # Process all .jpg files in the folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".jpg"):
            print(f"Processing {filename}...")
            image_path = os.path.join(input_folder, filename)  
            original_strips = process_images(image_path, vertical=IS_VERTICAL, shuffle=False)
            strips = process_images(image_path, vertical=IS_VERTICAL) 
            shredded_image = tsp.reconstructed_image(strips, vertical=IS_VERTICAL)
            if IS_VERTICAL:
                plt.imsave(os.path.join(output_folder, "Shredded_Vertical_" + filename), shredded_image)
            else:
                plt.imsave(os.path.join(output_folder, "Shredded_Horizontal_" + filename), shredded_image)
            # 1. Create a similarity matrix for the strips
            tsp_graph = tsp.create_similarity_matrix(strips)
            # Solve with TSP
            if IS_TSP:
                ordered_shreds = reconstruct_image_tsp(strips)
            else:
                ordered_shreds = reconstruct_image_heuristic(strips, tsp_graph)
            # 3. Calculate accuracy
            accuracy, reconstructed_strips = calculate_accuracy(original_strips, ordered_shreds)
            print(f"Accuracy: {accuracy:.2f}%")
            # Save the reconstructed image
            finalimage = tsp.reconstructed_image(reconstructed_strips, vertical=IS_VERTICAL)
            if IS_VERTICAL:
                plt.imsave(os.path.join(output_folder, "Reconstructed_Vertical_" + filename), finalimage)
            else:
                plt.imsave(os.path.join(output_folder, "Reconstructed_Horizontal_" + filename), finalimage)
            


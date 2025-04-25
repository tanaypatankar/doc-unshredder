import os
import shredder
import tsp
import matplotlib.pyplot as plt
from tsp_solver.greedy import solve_tsp


DEBUG = 0

def calculate_accuracy(original, reconstructed):
    """
    Calculate the accuracy of the reconstructed image compared to the original image.

    :param original: List of original unshuffled strips
    :param reconstructed: List of reconstructed strips
    :return: Accuracy as a percentage.
    """
    # Check that the lists have the same length
    if len(original) != len(reconstructed):
        print(f"Warning: Original ({len(original)} strips) and reconstructed ({len(reconstructed)} strips) have different lengths")
        return 0.0
    
    # Calculate the number of strips that are in the correct position
    correct_strips = 0
    total_strips = len(original)
    
    # Compare each strip using numpy arrays for precision
    for i in range(total_strips):
        orig_arr = np.array(original[i])
        
        # Find if this strip appears in the reconstructed image
        for j in range(total_strips):
            recon_arr = np.array(reconstructed[j])
            
            # Check if strips have the same shape
            if orig_arr.shape != recon_arr.shape:
                continue
                
            # Check if the strips are identical
            if np.array_equal(orig_arr, recon_arr) and i == j:
                correct_strips += 1
                break
    
    # Calculate accuracy percentage
    accuracy = (correct_strips / total_strips) * 100.0
    return accuracy

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

def process_images(image_path, vertical=True):
    """
    Shreds a single image and displays the shredded strips using matplotlib.

    :param image_path: Full path to the image file.
    :param vertical: Boolean flag indicating whether to create vertical strips (True) or horizontal strips (False).
    """
    # Shred the image into strips (vertical or horizontal)
    strips = shredder.shred_image(image_path, strip_size=1, vertical=vertical)
    
    if DEBUG:
        display_shreds(strips, vertical)

    # 1. Create a similarity matrix for the strips
    tsp_graph = tsp.create_similarity_matrix(strips)

    # 2. Find the best path using TSP solver
    best_path = solve_tsp(tsp_graph)
    if len(strips) in best_path:
        best_path.remove(len(strips))
    ordered_shreds = [strips[i] for i in best_path]
    display_shreds(ordered_shreds, vertical)

    #     OR

    # # 2. Use heurestic greedy algorithm to find the best path
    # result = tsp.reconstruct_strips(strips, tsp_graph)

if __name__ == "__main__":
    # Input folder path containing the images to be processed
    input_folder = "./Input" 

    # Process all .jpg files in the folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".jpg"):
            image_path = os.path.join(input_folder, filename)  
            process_images(image_path, vertical=True) 

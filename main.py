import os
import shredder
import tsp
import matplotlib.pyplot as plt
from tsp_solver.greedy import solve_tsp


DEBUG = 0

def display_ordered_shreds(shreds, order, isVertical):
    """
    Displays the shreds in a specific order.

    :param shreds: List of PIL.Image shreds.
    :param order: List of indices specifying the order in which to display the shreds.
    :param isVertical: Boolean indicating vertical (True) or horizontal (False) shreds.
    """
    ordered_shreds = [shreds[i] for i in order]

    # Choose display layout
    if isVertical:
        fig, axes = plt.subplots(1, len(ordered_shreds), figsize=(len(ordered_shreds) * 0.7, 2.5))
    else:
        fig, axes = plt.subplots(len(ordered_shreds), 1, figsize=(6, len(ordered_shreds) * 0.3))

    # Make sure axes is always iterable
    if len(ordered_shreds) == 1:
        axes = [axes]

    for ax, strip in zip(axes, ordered_shreds):
        ax.imshow(strip)
        ax.axis('off')

    plt.tight_layout()
    plt.show()


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
    display_ordered_shreds(strips, best_path, vertical)

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

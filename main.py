import os
import shredder
import tsp
import matplotlib.pyplot as plt
# import fast_tsp
from tsp_solver.greedy import solve_tsp


DEBUG = 1

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

    # plt.show()

    tsp_graph = tsp.create_similarity_matrix(shreds)
    # print(f"Similarity matrix: {tsp_graph}")

    # print minimum non-zero value and the row/column it belongs to
                # reconstructed = []
                # min_value = float('inf')
                # min_left = -1
                # min_right = -1
                # min_i = -1
                # min_j = -1
                # for i in range(len(tsp_graph)):
                #     for j in range(len(tsp_graph)):
                #         if tsp_graph[i][j] > 0 and tsp_graph[i][j] < min_value:
                #             min_value = tsp_graph[i][j]
                #             min_i = i
                #             min_j = j
                # print(f"Minimum non-zero value: {min_value} at index {min_i}, jindex {min_j}")
                # print(tsp_graph[min_j][min_i])
                # input()
                # tsp_graph[min_i][min_j] = 0
                # reconstructed.append([shreds[min_i], shreds[min_j]])
                # print(f"Reconstructed: {reconstructed}")

    # for leftvals in range(len(tsp_graph)):
    #     if leftvals != min_i and leftvals != min_j:

    best_path = solve_tsp(tsp_graph)
    print(f"Best path: {best_path}")
    if len(shreds) in best_path:
        best_path.remove(len(shreds))
    display_ordered_shreds(shreds, best_path, isVertical)

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

if __name__ == "__main__":
    # Input folder path containing the images to be processed
    input_folder = "./Input" 

    # Process all .jpg files in the folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".jpg"):
            image_path = os.path.join(input_folder, filename)  
            process_images(image_path, vertical=True) 

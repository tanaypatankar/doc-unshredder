import os
from matplotlib import pyplot as plt
import shredder

DEBUG = 1
from tsp import calculate_strip_similarity

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
    strips = shredder.shred_image(image_path, strip_size=9, vertical=vertical)
    
    if DEBUG:
        display_shreds(strips, vertical)

if __name__ == "__main__":
    # Input folder path containing the images to be processed
    input_folder = "./Input-Img" 

    # Process all .jpg files in the folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".jpg"):
            image_path = os.path.join(input_folder, filename)  
            process_images(image_path, vertical=False) 

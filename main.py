import os
from matplotlib import pyplot as plt
from shredder import shred_image

def process_and_display_shreds(input_folder, image_name):
    """
    Reads an image from the input folder, shreds it, and displays the shreds using matplotlib.
    
    :param input_folder: Path to the folder containing the input image.
    :param image_name: Name of the image file to process.
    """
    image_path = os.path.join(input_folder, image_name)
    strips = shred_image(image_path)

    # Display the strips using matplotlib
    fig, axes = plt.subplots(1, len(strips), figsize=(15, 5))
    for ax, strip in zip(axes, strips):
        ax.imshow(strip)
        ax.axis('off')
    plt.show()

if __name__ == "__main__":
    input_folder = "./Input"  # Replace with your input folder path
    image_name = "image01.jpg"  # Replace with your image file name
    process_and_display_shreds(input_folder, image_name)
import os
from matplotlib import pyplot as plt
from shredder import shred_image

def process_and_display_shreds(image_path):
    """
    Shreds a single image and displays the shreds using matplotlib.

    :param image_path: Full path to the image file.
    """
    strips = shred_image(image_path)

    # Display the strips using matplotlib
    fig, axes = plt.subplots(1, len(strips), figsize=(15, 5))
    for ax, strip in zip(axes, strips):
        ax.imshow(strip)
        ax.axis('off')
    plt.suptitle(os.path.basename(image_path))  # Optional: show image name
    plt.show()

if __name__ == "__main__":
    input_folder = "./Input-Img"  # Replace with your input folder path

    # Process all .jpg files in the folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".jpg"):
            image_path = os.path.join(input_folder, filename)
            process_and_display_shreds(image_path)

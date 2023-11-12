import cv2

def check_resolution(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Get the resolution
    height, width, _ = image.shape

    return width, height

# Example usage:
width, height = check_resolution('D:\\vscode_stuff\\Programming\\Python\\Steganography\\02\\image.png')
print(f'The resolution of the image is {width}x{height}')
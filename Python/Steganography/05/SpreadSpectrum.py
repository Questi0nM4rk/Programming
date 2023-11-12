import cv2
import numpy as np


def text_to_bits(text):
    return ''.join(format(ord(char), '08b') for char in text)


def encode(image_path, text, output_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the text to bits
    bits = text_to_bits(text)

    # Append the special sequence of bits to the end of our message
    bits += '0' * 64

    # Ensure the image is large enough to encode the text
    if len(bits) > image.size:
        raise ValueError('The image is not large enough to encode the text.')

    # Spread the bits across the image
    bit_index = 0
    for i in np.ndindex(image.shape):
        if bit_index < len(bits):
            # Modify the pixel value to encode the bit
            if image[i] % 2 == int(bits[bit_index]):
                pass
            elif image[i] % 2 == 1 and image[i] != 255:
                image[i] += 1
            elif image[i] % 2 == 1 and image[i] == 255:
                image[i] -= 1
            elif image[i] % 2 == 0 and image[i] != 0:
                image[i] -= 1
            elif image[i] % 2 == 0 and image[i] == 0:
                image[i] += 1
            bit_index += 1

    # Save the encoded image
    cv2.imwrite(output_path, image)

def decode(encoded_path):
    # Load the encoded image
    encoded_image = cv2.imread(encoded_path)

    # Extract the least significant bit of each pixel
    decoded_bits = (encoded_image & 0b00000001).flatten()

    # Convert the bits to text
    decoded_text = ''
    for i in range(0, len(decoded_bits), 8):
        byte = ''.join(map(str, decoded_bits[i:i+8]))
        if byte == '00000000':
            break
        decoded_text += chr(int(byte, 2))

    return decoded_text


# Specify the paths to the images
image_path = 'image.png'
encoded_path = 'encoded.png'

# Specify the text to encode
text = 'Hello, world!'

# Encode the text into the image
encode(image_path, text, encoded_path)

# Decode the text from the encoded image
decoded_text = decode(encoded_path)

print('Decoded text:', decoded_text)
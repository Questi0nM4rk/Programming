import cv2
import numpy as np


def select_pixel_pair(image, given_key, bit_index):
    # Convert the key to a number by summing up the ASCII values of its characters
    key_number = sum(ord(char) for char in given_key)

    # Add the bit index to the key number
    key_number += bit_index

    # Use the key number to select a pair of pixels
    height, width, _ = image.shape
    x1 = key_number % width
    y1 = (key_number // width) % height
    x2 = (key_number // (width * height)) % width
    y2 = ((key_number // (width * height)) // width) % height

    return image[y1, x1], image[y2, x2]


def text_to_bits(text):
    return ''.join(format(byte, '08b') for byte in text.encode('utf-8'))

def bits_to_text(bits):
    # Join the bits into a single string
    bits_string = ''.join(bits)

    # Split the bits string into 8-bit chunks
    byte_strings = [bits_string[i:i+8] for i in range(0, len(bits_string), 8)]

    # Pad the last chunk with zeros on the left if it's less than 8 bits long
    byte_strings[-1] = byte_strings[-1].zfill(8)

    # Convert each 8-bit chunk to a character
    bytes = [int(byte_string, 2) for byte_string in byte_strings]

    # Convert the bytes to text using 'utf-8'
    text = bytearray(bytes).decode('utf-8')

    return text


def patchwork_encode(image_path, text, output_path, given_key):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the text to bits
    bits = text_to_bits(text)

    # Encode the bits into the pixel values
    for bit_index, bit in enumerate(bits):
        pixel1, _ = select_pixel_pair(image, given_key, bit_index)
        pixel1[0] = (pixel1[0] & 0xFE) | int(bit)

    # Save the encoded image
    cv2.imwrite(output_path, image)


def patchwork_decode(image_path, given_key, length):
    # Load the image
    image = cv2.imread(image_path)

    length *= 8
    
    # Decode the bits from the pixel values
    bits = []
    for bit_index in range(length):
        pixel1, _ = select_pixel_pair(image, given_key, bit_index)
        bits.append(str(pixel1[0] & 1))

    # Convert the bits to text
    text = bits_to_text(bits)

    return text


# Specify the paths to the images
name = '9rH2U2cm6L'
next = 'Ah3rIZDqZw'

image_path = 'image.png'
encoded_path = f'{name}.png'

# Specify the text to encode
text = 'Vážení vojáci, musíme vás varovat, že máme podezření, že někdo sleduje a čte naše rozkazy. Z tohoto důvodu buďte extrémně opatrní a mějte ostražitý pohled na vaše okolí. Vaše bezpečnost a bezpečnost informací jsou v tomto okamžiku klíčové. Další rozkazy jsou v alg05. Další kód: ' + next

# Encode the text into the image
patchwork_encode(image_path, text, encoded_path, "LosKarlos")

# Decode the text from the encoded image
decoded_text = patchwork_decode(encoded_path, "LosKarlos", len(text.encode('utf-8')))

print('Decoded text:', decoded_text)
import cv2
import numpy as np



class Alg01:

    @staticmethod
    def encode(output_name, image_path, text):
        # Load the image
        img = cv2.imread(image_path)

        # Convert text to binary
        binary = text_to_bits(text)

        for i in range(len(binary)):
            # Find the pixel to modify
            x = i // img.shape[1]
            y = i % img.shape[1]

            # Embed the bit into the pixel if it's different from the LSB
            if str(img[x, y, 0] & 0x1) != binary[i]:
                img[x, y, 0] ^= 0x1

        # Save the stego image
        cv2.imwrite(f'{output_name}', img)

    @staticmethod
    def decode(image_path, text_length):
        # Load the image
        img = cv2.imread(image_path)

        # Extract the bits
        bits = ""
        for i in range(text_length * 8):
            # Find the pixel
            x = i // img.shape[1]
            y = i % img.shape[1]

            # Extract the least significant bit of the pixel's blue color
            bits += str(img[x, y, 0] & 0x1)

        # Convert the bits to text
        return bits_to_text(bits)



class Alg02:
    @staticmethod
    def encode(image_path, message_path, output_path):
        # Load the images
        image = cv2.imread(image_path)
        message = cv2.imread(message_path, cv2.IMREAD_GRAYSCALE)

        # Ensure the images are the same size
        image = cv2.resize(image, (message.shape[1], message.shape[0]))

        # Make red channel even where message is white
        image[(message == 255) & (image[..., 2] % 2 != 0), 2] += 1

        # Make red channel odd where message is black
        image[(message == 0) & (image[..., 2] % 2 == 0), 2] += 1

        # Save the encoded image
        cv2.imwrite(output_path, image)

    @staticmethod
    def decode(encoded_path, output_path):
        # Load the encoded image
        encoded = cv2.imread(encoded_path)

        # Create an empty array for the decoded message
        decoded = np.zeros((encoded.shape[0], encoded.shape[1]), dtype=np.uint8)

        # Set white where red channel is even
        decoded[encoded[..., 2] % 2 == 0] = 255

        # Save the decoded image
        cv2.imwrite(output_path, decoded)



class Alg03:
    @staticmethod
    def encode(image_path, message_path, output_path):
        # Load the images
        image = cv2.imread(image_path)
        message = cv2.imread(message_path)

        # Ensure the images are the same size
        image = cv2.resize(image, (message.shape[1], message.shape[0]))

        # Convert the images to 8-bit unsigned integers
        image = np.uint8(image)
        message = np.uint8(message)

        # Shift the message image bits to the right
        message = message >> 7

        # Clear the least significant bit of the image
        image = image & 0b11111110

        # Combine the images
        encoded_image = image | message

        # Save the encoded image
        cv2.imwrite(output_path, encoded_image)

    @staticmethod
    def decode(encoded_path, output_path):
        # Load the encoded image
        encoded_image = cv2.imread(encoded_path)

        # Extract the least significant bit of each pixel
        decoded_image = encoded_image & 0b00000001

        # Shift the bits to the left to make the message visible
        decoded_image = decoded_image << 7

        # Save the decoded image
        cv2.imwrite(output_path, decoded_image)
        


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



class Alg04:
    @staticmethod
    def encode(image_path, text, output_path, given_key):
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

    @staticmethod
    def decode(image_path, given_key, length):
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
    


class Alg05:
    @staticmethod
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

    @staticmethod
    def decode(encoded_path):
        # Load the encoded image
        encoded_image = cv2.imread(encoded_path)

        # Extract the least significant bit of each pixel
        decoded_bits = (encoded_image & 0b00000001).flatten()

        # Convert the bits to bytes
        decoded_bytes = []
        for i in range(0, len(decoded_bits), 8):
            byte = ''.join(map(str, decoded_bits[i:i+8]))
            if byte == '00000000':
                break
            decoded_bytes.append(int(byte, 2))

        # Convert the bytes to text using 'utf-8'
        decoded_text = bytearray(decoded_bytes).decode('utf-8')

        return decoded_text


""" original image => Alg03 -> image => Alg04(Stejne heslo jako naposledy) -> code to next image => Alg02 -> image with code to next image -> image => Alg05 -> lastCode -> lastImage
originalImage = "uWukiLW032.png" # Original image
# Alg03 image
imageEncodedInImage = "imageEncodedInImage.png"
# Alg04 code to next image
codeToNext = "wpwpGGs180noscope"
# Alg02 image with code to next image
imageToUse02On = "wpwpGGs180noscope.png" # Image to use Alg02 on
# output image:
imageWithCodeToNextImage = "imageWithCodeToNextImage.png" # Black and white code
codeToNext2 = "Y0urM0mL1k3sM1Lk" # Code on the imageWithCodeToNextImage
theNextImage = "Y0urM0mL1k3sM1Lk.png" # The next image
# Alg05 image
lastCode = "v55c9sbOAD"
# Last funny image
lastImage = "v55c9sbOAD.png"


05.encode(theNextImage, lastCode) -> encode last code into the next image
02.encode(imageToUse02On, imageWithCodeToNextImage) -> encode imageWithCodeToNextImage into imageToUse02On
04.encode(codeToNext, imageEncodedInImage) -> encode codeToNext into imageEncodedInImage
03.encode(originalImage, imageEncodedInImage) -> encode imageEncodedInImage into originalImage
"""

key = "LosKarlos"


# The next image
theNextImage = "Y0urM0mL1k3sM1Lk.png"

# Alg05 image
lastCode = "Vojáci, je to špatné, dostali jsme totálně na zadek. Karlík a jeho skupina nás přepadli a zničili všechny naše útočné pozice. Konverze na light mode a modernizace jejich zařízení se konat nebude. Bohužel, nám dokázali, že dark mode a Linux jsou prostě lepší. Každý sám za sebe, zavolejte si Uber nebo tak něco. Sbohem. Žádné další rozkazy nebudou. Poslední heslo: v55c9sbOAD"
print(len(lastCode.encode("utf-8")))
Alg05.encode("theNextImage.png", lastCode, theNextImage)

# Alg02 image with code to next image
ImageToUse02On = "wpwpGGs180noscope.png"
imageWithCodeToNextImage = "imageWithCodeToNextImage.png"
Alg02.encode("ImageToUse02On.png", imageWithCodeToNextImage, ImageToUse02On)

# Alg04 code to next image
codeToNext = "Vojáci, nalézáme se v kritické situaci. Nepřítel pod vedením nebezpečného Karlika zasáhl naše zadní linie ze zálohy a způsobil nám značné ztráty. Zřejmě se jim opravdu nelíbí light mode ani naše iphony. V této chvíli je naší prioritou zajistit taktický ústup a připravit se na další možný odpor. Další kód je podle předchozích instrukcí 02. Kód na další obrázek: wpwpGGs180noscope"
print(len(codeToNext.encode("utf-8")))

imageInBetween = "ALm0stTh3r3L1ttLe0n3.png"
codeInBetween = "ALm0stTh3r3L1ttLe0n3"
Alg04.encode(imageInBetween, codeToNext, imageInBetween, key)


ImageEncodedInImage = "ImageEncodedInImage.png" # Image with a code in between

# Original image
originalImage = "uWukiLW032.png"
Alg03.encode("originalImage.png", ImageEncodedInImage, originalImage)

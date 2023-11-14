import cv2
import numpy as np

def text_to_bits(text):
    return ''.join(format(byte, '08b') for byte in text.encode('utf-8'))

def bits_to_text(bits):
    # Split the bits into groups of 8
    byte_strings = [bits[i:i+8] for i in range(0, len(bits), 8)]

    # Convert each group of 8 bits to a byte
    bytes = [int(byte_string, 2) for byte_string in byte_strings]

    # Convert the bytes to text using 'utf-8'
    text = bytearray(bytes).decode('utf-8')

    return text

def f3_encode(name, image_path, text):
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
    cv2.imwrite(f'{name}', img)

def f3_decode(image_path, text_length):
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

# Example usage


name = 'Ns1DI4N5U9'
next = 'iHC438uwRv'

text = "Vojáci, vaším úkolem je provést důkladný průzkum okolního terénu. Začněte vyhledávat strategické body, které by mohly posloužit jako potenciální útočiště nebo základny. Při průzkumu dávejte pozor na možné pasti nebo nepřátelské síly. Další rozkazy budou zakódovánz alg02, dostanete z něj obrázek, který dešifrujte alg01. Další kód: " + next

img = cv2.imread('image.png')
print('Total pixels:', img.shape[0] * img.shape[1])
print('Text length in bits:', len(text.encode('utf-8')) * 8)

f3_encode(f"{name}.png", 'image.png', text)
decoded_message = f3_decode(f"{name}.png", len(text.encode('utf-8')))
print(decoded_message)

"""f3_encode("message.png", 'message.png', "Vojáci, naléhavý úkol před námi. Obkličte nepřátelský tábor a vyvíjejte na ně tlak. Snažte se je dostat do defenzivy a vyčkávejte na další pokyny. Buďte obezřetní a využijte každou příležitost k oslabení jejich pozice. Další rozkazy budou zakódovány pomocí alg03. Dostanete obrázek, který dešifrujte pomocí alg01. Další kód: na obrázku")
decoded_message = f3_decode(f"message.png", 40)
print(decoded_message)"""

t = "Vojáci, sjednoťte se a shromážděte u hlavní brány. Máme připraven útok nebo důležitou strategickou akci, kterou je třeba provést společně. Buďte připraveni na soustředěný postup a silný útok. Další rozkazy budou zakódovány pomocí alg04. K tomuto budete potřebovat i klíč, který je jméno našeho velitele(PascalCase). Další kód: v obrázku"
f3_encode("message.png", "message.png", t)
print(f3_decode(f"message.png", len(t.encode('utf-8'))))
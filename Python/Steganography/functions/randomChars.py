import random
import string

random_chars = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
print(random_chars)
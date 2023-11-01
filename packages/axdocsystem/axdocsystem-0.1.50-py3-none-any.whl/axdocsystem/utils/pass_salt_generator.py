import random
import string

def generate_pass_salt(size=4) -> str:
    return ''.join(random.choices(string.printable, k=size))


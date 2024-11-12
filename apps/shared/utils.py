from string import ascii_lowercase, digits
import random


def get_random_text(length: int = 30):
    string = ""
    for _ in range(1, length):
        string += random.choice([i for i in ascii_lowercase + digits])
    return string

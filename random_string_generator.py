import random

class RandomStringGenerator:
    @staticmethod
    def generate_random_string():
        dictionary = [
            "apple", "banana", "orange", "grape", "pear",
            "dog", "cat", "rabbit", "hamster", "bird",
            "house", "car", "bicycle", "boat", "plane"
        ]
        num_words = random.randint(5, 10)
        random_words = random.choices(dictionary, k=num_words)
        random_string = ' '.join(random_words)
        return random_string
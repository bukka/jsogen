import random

class Template:
    """Template for generating JSON"""

    def __init__(self, path, output, seed=None):
        self.seed = seed or random.randint(1, 1000)
        self.path = path
        self.output = output

    def generate(self):
        print("path: %s, output: %s, seed: %d" % (self.path, self.output, self.seed))


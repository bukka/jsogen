
class Expression:
    """Expression class"""

    def __init__(self, es, output):
        # Expression string
        self.es = es
        # output
        self.output = output

    def run(self):
        self.output.write(self.es)

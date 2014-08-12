import json
import random
import sys


class Template:
    """Template for generating JSON"""

    def __init__(self, path, output, seed=None, quiet=False):
        self.seed = seed or random.randint(1, 1000)
        self.path = path
        self.output = output
        self.quiet = quiet

    def _debug(self, message):
        if not self.quiet:
            print(message)

    def _print(self, content):
        self.ohandle.write(str(content))

    def _parse(self, data):
        self._print(data)
        pass

    def generate(self):
        self.ihandle = open(self.path, "r")
        self.ohandle = open(self.output, "w") if self.output else sys.stdout

        self._debug("Template (path: %s, output: %s, seed: %d)" %
                    (self.path, self.output, self.seed))
        try:
            self._parse(json.load(self.ihandle))
        finally:
            self.ihandle.close()
            if self.ohandle is not sys.stdout:
                self.ohandle.close()


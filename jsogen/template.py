import json
import random
import sys
from pip._vendor.pkg_resources import basestring


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

    def _parse_array(self, dl):
        self._print('[')
        for val in dl:
            self._parse(val)
            self._print(',')
        self._print(']')

    def _parse_object(self, dd):
        self._print('{')
        for key, val in dd.items():
            self._print('"%s":' % key)
            self._parse(val)
            self._print(',')
        self._print('}')

    def _parse_string(self, ds):
        self._print('"%s"' % ds)

    def _parse(self, data):
        if isinstance(data, list):
            self._parse_array(data)
        elif isinstance(data, dict):
            self._parse_object(data)
        elif isinstance(data, basestring):
            self._parse_string(data)
        else:
            self._print(data)

    def generate(self):
        self.ihandle = open(self.path, "r")
        self.ohandle = open(self.output, "w") if self.output else sys.stdout

        self._debug("Template (path: %s, output: %s, seed: %d)" %
                    (self.path, self.output if self.output else "STDOUT", self.seed))
        try:
            self._parse(json.load(self.ihandle))
        finally:
            self.ihandle.close()
            if self.ohandle is sys.stdout:
                self._print("\n")
            else:
                self.ohandle.close()


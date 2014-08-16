import json
import random
import sys
from pip._vendor.pkg_resources import basestring


class Template:
    """Template for generating JSON"""

    def __init__(self, path, output, seed=None, quiet=False):
        self.path = path
        self.output = output
        self.quiet = quiet
        self.seed = seed or random.randint(1, 1000)
        random.seed(seed)

    def _debug(self, message):
        if not self.quiet:
            print(message)

    def _make_command(self, ds):
        s = ds.strip()
        if not s.startswith('{{') or not s.endswith('}}'):
            return None
        return TemplateCommand(s[2:-2])

    def _print(self, content):
        self.ohandle.write(str(content))

    def _parse_array(self, dl):
        self._print('[')
        if len(dl):
            self._parse(dl[0])
            for val in dl[1:]:
                self._print(',')
                self._parse(val)
        self._print(']')

    def _parse_object(self, dd):
        self._print('{')
        dd_len = len(dd) - 1;
        for key, val in dd.items():
            self._print('"%s":' % key)
            self._parse(val)
            if dd_len > 0:
                self._print(',')
                dd_len -= 1
        self._print('}')

    def _parse_string(self, ds):
        cmd = self._make_command(ds)
        if cmd:
            cmd.run(self.ohandle)
        else:
            self._print('"%s"' % str)

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


class TemplateCommand:
    """Template command executer"""

    def __init__(self, cmd):
        self.cmd = cmd

    def run(self, output):
        output.write(self.cmd)

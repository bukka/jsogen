import json
import random
import sys
import re
import io
from .expression import Expression

# compat with python 2
if sys.version >= '3':
    basestring = str
    StringIO = io.StringIO
    b = lambda x : x
else:
    StringIO = io.BytesIO
    b = bytes

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

    def _print(self, content):
        self.ohandle.write(str(content))

    def _get_repeat(self, val):
        if (isinstance(val, TemplateString) and
                val.expression and val.expression.function and
                val.expression.function.repeat is not None):
            return val.expression.function.repeat
        else:
            return None

    def _parse_array(self, dl):
        self._print('[')
        if len(dl):
            val = self._parse(dl[0])
            repeat = self._get_repeat(val)
            if repeat is None:
                repeat = 1
                is_first = False
            else:
                is_first = True
            while repeat > 0:
                for val in dl[1:]:
                    if is_first:
                        is_first = False
                    else:
                        self._print(',')
                    self._parse(val)
                repeat -= 1
        self._print(']')

    def _parse_object_pass1(self, dd):
        ndd = {}
        repeat = None
        for key, val in dd.items():
            sio = StringIO()
            ts = TemplateString(sio)
            ts.run(key)
            key_repeat = self._get_repeat(ts)
            if key_repeat is None:
                ndd[sio.getvalue()] = val
            else:
                repeat = key_repeat
        return (ndd, repeat)

    def _parse_object(self, dd):
        self._print('{')
        (dd, repeat) = self._parse_object_pass1(dd)
        max_range = 2 if repeat is None else repeat + 1
        for i in range(1, max_range):
            dd_len = len(dd) - 1;
            key_suffix = None if repeat is None else "_%d" % i
            for key, val in dd.items():
                key_name = key if key_suffix is None else key[0:-1] + key_suffix + '"'
                self._print('%s:' % key_name)
                self._parse(val)
                if dd_len > 0:
                    self._print(',')
                    dd_len -= 1
            if i < max_range - 1:
                self._print(',')
        self._print('}')

    def _parse_string(self, ds):
        ts = TemplateString(self.ohandle)
        ts.run(ds)
        return ts

    def _parse(self, data):
        if isinstance(data, list):
            self._parse_array(data)
        elif isinstance(data, dict):
            self._parse_object(data)
        elif isinstance(data, basestring):
            return self._parse_string(data)
        else:
            self._print(data)
        return True

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


class TemplateString:
    """Template string converter"""

    pattern = re.compile(r"{{\s*(.*?)\s*}}")

    def __init__(self, output):
        self.output = output
        self.expression = None

    def _match(self, match):
        self.expression = Expression(match.group(1), output=self.output)
        self.expression.run()

    def run(self, data):
        self.expression = None
        self.__class__.pattern.sub(self._match, data)
        if self.expression is None:
            self.output.write('"' + b(data) + '"')

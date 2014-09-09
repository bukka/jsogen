import random
import string

class Function:
    """Template Function"""
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.repeat = False

    def dump(self, os):
        os.write("%s[%s]" % (self.name, ', '.join(self.args)))

    def run(self, os):
        self.os = os
        if self.name == 'repeat':
            self.f_repeat(*self.args)
        elif self.name == 'boolean':
            self.f_boolean(*self.args)
        elif self.name == 'integer':
            self.f_integer(*self.args)
        elif self.name == 'float':
            self.f_float(*self.args)
        elif self.name == 'number':
            self.f_number(*self.args)
        elif self.name == 'string':
            self.f_string(*self.args)
        else:
            self.dump(os)

    def _write(self, msg):
        self.os.write(str(msg))

    def f_repeat(self, count1, count2=None):
        self.repeat = random.randint(int(count1), int(count2)) if count2 else int(count1)

    def f_boolean(self):
        self._write(random.choice(["true", "false"]))

    def f_integer(self, len1, len2):
        self._write(random.randint(int(len1), int(len2)))

    def f_float(self, len1, len2):
        self._write(random.uniform(float(len1), float(len2)))

    def f_number(self, len1, len2, kind='integer'):
        if type == 'float':
            self.f_float(len1, len2)
        else:
            self.f_integer(len1, len2)

    def f_string(self, len1, len2=None, kind='basic'):
        if not len2:
            len2 = len1
            len1 = 0
        if kind == 'basic':
            # just simplified set of english letters
            seq = string.ascii_letters + string.digits + '    _()'
        if kind == 'printable':
            seq = string.printable
        if kind == 'ascii':
            seq = string.ascii_letters
        if kind == 'digit':
            seq = string.digits
        slen = random.randint(int(len1), int(len2))
        self._write('"' + ''.join([random.choice(seq) for _ in range(slen)]) + '"')

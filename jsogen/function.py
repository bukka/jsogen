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

    def _char_range(self, start, end):
        return [ chr(x) for x in range(start, end) ]

    def f_string(self, len1, len2=None, kind='basic'):
        if not len2:
            len2 = len1
            len1 = 0
        seq = False
        if kind == 'basic':
            # just simplified set of english letters
            seq = string.ascii_letters + string.digits + '    _()'
        elif kind == 'ascii':
            seq = string.ascii_letters
        elif kind == 'digit':
            seq = string.digits
        elif kind == 'printable':
            seq = string.printable
        elif kind.startswith('utf8'):
            utf8_1 = [0x000020, 0x00007f]
            utf8_2 = [0x000080, 0x0007ff]
            utf8_3 = [0x001000, 0x00ffff]
            utf8_4 = [0x010000, 0x10ffff]
            if kind == 'utf8':
                seq_1 = self._char_range(*utf8_1)
                seq_2 = self._char_range(*utf8_2)
                seq_3 = self._char_range(*utf8_3)
                seq_4 = self._char_range(*utf8_4)
                seq = seq_1 + seq_2 + seq_3 + seq_4
            if kind == 'utf8_1':
                seq = self._char_range(*utf8_1)
            elif kind == 'utf8_2':
                seq = self._char_range(*utf8_2)
            elif kind == 'utf8_3':
                seq = self._char_range(*utf8_3)
            elif kind == 'utf8_4':
                seq = self._char_range(*utf8_4)
        if not seq:
            raise FunctionException("Invalid string kind")
        slen = random.randint(int(len1), int(len2))
        self._write('"' + ''.join([random.choice(seq) for _ in range(slen)]) + '"')

class FunctionException(Exception):
    pass

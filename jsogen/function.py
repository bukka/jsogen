import random
import string
import sys

class Function:
    """Template Function"""
    def __init__(self, name, args, nargs):
        self.name = name
        self.args = args
        self.nargs = nargs
        self.repeat = False

    def dump(self, os):
        os.write("%s[%s]" % (self.name, ', '.join(self.args)))

    def run(self, os):
        self.os = os
        cb_name = "f_" + self.name
        if hasattr(self, cb_name):
            cb = getattr(self, "f_" + self.name)
            cb(*self.args, **self.nargs)
        else:
            self.dump(os)


    def _write(self, msg):
        self.os.write(str(msg))

    def f_repeat(self, count1, count2=None):
        if count2 is None:
            self.repeat = int(count1)
        else:
            self.repeat = random.randint(int(count1), int(count2))

    def f_boolean(self):
        self._write(random.choice(["true", "false"]))

    def f_integer(self, len1, len2=None):
        if len2 is None:
            len2 = len1
            len1 = 0
        self._write(random.randint(int(len1), int(len2)))

    def f_float(self, len1, len2=None, precision=10, exponent=False):
        if len2 is None:
            len2 = len1
            len1 = 0.
        value = random.uniform(float(len1), float(len2))
        flag = 'e' if exponent else 'f'
        format = "%." + str(precision) + flag
        self._write(format % value)

    def f_number(self, len1, len2, kind='integer'):
        if type == 'float':
            self.f_float(len1, len2)
        else:
            self.f_integer(len1, len2)

    def f_string(self, *args, **nargs):
        FunctionString(self.os).run(*args, **nargs)

# compat with python 2
if sys.version >= '3':
    unichr = chr


class FunctionString:

    def __init__(self, os):
        self.os = os

    def _choice_mix(self, choice1, seq1, choice2, seq2, ratio):
        return choice2(seq2) if random.random() > ratio else choice1(seq1)

    def _choose_utf_code(self, code_range):
        code = random.randint(code_range[0], code_range[1])
        # shift for surrogate character codes
        if code > 0xd7ff:
            code += 0x800
        return code

    def _choice_utf(self, code_range):
        code = self._choose_utf_code(code_range)
        # do not return back slash or double quote
        if code == ord('\\') or code == ord('"'):
            return ''
        if code >= 0x10000 and sys.version < '3':
            s = "\\U%08x" % code
            return s.decode('unicode-escape')
        else:
            return unichr(code)

    def _choice_utf_esc(self, code_range):
        code = self._choose_utf_code(code_range)
        if code > 0x010000:
            high = 0xD800 + (code >> 10)
            low = 0xDC00 + (code & 0x3ff)
            return self._utf_code_to_esc(high) + self._utf_code_to_esc(low)
        else:
            return self._utf_code_to_esc(code)

    def _utf_code_to_esc(self, code):
        return "\\u{:04X}".format(code)

    def _kind_utf(self, kind):
        kind = kind.replace('escape_utf', 'utf8')
        if kind == 'utf8' or kind == 'utf8_14':
            return (0x000020, 0x10f7ff)
        if kind == 'utf8_1':
            return (0x000020, 0x00007f)
        if kind == 'utf8_2':
            return (0x000080, 0x0007ff)
        if kind == 'utf8_3':
            return (0x001000, 0x00f7ff)
        if kind == 'utf8_4':
            return (0x00f800, 0x10f7ff)
        if kind == 'utf8_12':
            return (0x000020, 0x0007ff)
        if kind == 'utf8_13':
            return (0x000020, 0x00f7ff)
        if kind == 'utf8_23':
            return (0x000080, 0x00f7ff)
        if kind == 'utf8_24':
            return (0x000080, 0x10f7ff)
        return None

    def _kind(self, kind):
        # default choice function for selecting random item from seq
        choice = lambda x: random.choice(x)
        # sequence string or range tuple for utf
        seq = False
        if kind == 'basic':
            # spaces have higher probabality of selection
            spaces = ' ' * 10
            # just simplified set of english letters + spaces
            seq = string.ascii_letters + string.digits + spaces
        elif kind == 'ascii_letters':
            seq = string.ascii_letters
        elif kind == 'digit':
            seq = string.digits
        elif kind == 'printable':
            # punctuation that does not contain back slash and double quote
            punctuation = "!#$%&'()*+,-./:;<=>?@[]^_`{|}~"
            seq = string.ascii_letters + string.digits + string.whitespace + punctuation
        elif kind == 'escape':
            seq = ['\\n', '\\t', '\\r', '\\f', '\\b', '\\\\', '\\/']
        elif kind.startswith('escape_utf'):
            choice = self._choice_utf_esc
            seq = self._kind_utf(kind)
        elif kind.startswith('utf8'):
            choice = self._choice_utf
            seq = self._kind_utf(kind)
        if not seq:
            raise FunctionException("Invalid string kind")
        # return tuple with choice function and seq / range tuple
        return (choice, seq)

    def run(self, len1, len2=None, kind='basic', kind2=None, ratio=None):
        # string length
        if not len2:
            slen = len2 = len1
        else:
            slen = random.randint(int(len1), int(len2))

        # default values for escape mode (prevents all escapes by default)
        if kind.startswith('escape'):
            kind2 = kind2 or 'basic'
            ratio = ratio or 0.5 if kind.startswith('escape_utf') else 0.1

        (choice, seq) = self._kind(kind)
        if kind2:
            (choice2, seq2) = self._kind(kind2)
            arg = (choice, seq, choice2, seq2, ratio)
            choice = self._choice_mix
        else:
            arg = (seq,)

        # generate string array
        sarr = []
        while slen > 0:
            c = choice(*arg)
            slen -= len(c)
            sarr.append(c)
        # write string
        self.os.write('"' + ''.join(sarr) + '"')


class FunctionException(Exception):
    pass

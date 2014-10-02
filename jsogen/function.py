import random
import string
import sys

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
            FunctionString(os).run(*self.args)
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


class FunctionString:

    def __init__(self, os):
        self.os = os
        if sys.version < '3':
            self.chr = unichr
            self.uesc = lambda x : unichr(x).encode('unicode_escape')
        else:
            self.chr = chr
            self.uesc = lambda x : chr(x).encode('unicode_escape').decode('utf8')

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
        return self.chr(code)



    def _choice_utf_esc(self, code_range):
        code = self._choose_utf_code(code_range)
        if code > 0x010000:
            pass
        else:
            return self.uesc(code)


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
        # default choic function for selecting random item from seq
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
            choice = self._choice_esc_utf
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
            ratio = ratio or 0.1

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

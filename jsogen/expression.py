import string

class Expression:
    """Expression class"""

    def __init__(self, es, output):
        # Expression string
        self.es = es
        # output
        self.output = output

    def run(self):
        self.output.write(self.es)


class Token:
    """Tokens"""

    t_empty = 1
    t_int = 2
    t_float = 3
    t_string = 4


class Scanner:
    """Expression Scanner"""

    def __init__(self, es):
        self.es = es
        self.start = 0
        self.pos = 0
        self.value = None
        self.token = None

    def scan(self):
        es = self.es
        if (es[self.start] in string.whitespace):
            self.start += 1
        p = self.start
        in_string = False
        token = Token.t_empty
        while p < es.len:
            if not in_string and es[p] in string.whitespace:
                return token


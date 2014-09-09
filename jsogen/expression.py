import string
from function import Function

class Expression:
    """Expression class"""

    def __init__(self, es, output):
        # parser
        self.parser = Parser(es)
        # output
        self.output = output
        # function object
        self.function = None

    def run(self):
        fce = self.parser.parse()
        fce.run(self.output)
        self.function = fce



class Token:
    """Tokens"""

    t_empty = 0
    t_int = 1
    t_float = 2
    t_string = 3
    t_comma = 4
    t_ident = 5
    t_rpar = 6
    t_lpar = 7
    t_rpar = 8
    t_eq = 9
    t_end = 10

class Parser:
    """Parser"""

    def __init__(self, es):
        self.scanner = Scanner(es)

    def _assert(self, expected_token, token=False):
        if not token:
            token = self.scanner.scan()
        if expected_token != token:
            raise ParserException("Expected %d token, provided %d" % (expected_token, token))
        return self.scanner.value

    def _assert_arg(self, token=False):
        if not token:
            token = self.scanner.scan()
        if token not in [Token.t_int, Token.t_float, Token.t_string]:
            raise ParserException("Invalid argument token")
        return self.scanner.value

    def parse(self):
        fce = self._function()
        self._assert(Token.t_end)
        return fce

    def _function(self):
        name = self._assert(Token.t_ident)
        self._assert(Token.t_lpar)
        args = self._args()
        return Function(name, args)

    def _args(self):
        args = []
        token = self.scanner.scan()
        if token == Token.t_rpar:
            return args
        args.append(self._assert_arg(token))
        return self._args_cont(args)

    def _args_cont(self, args):
        token = self.scanner.scan()
        if token == Token.t_rpar:
            return args
        self._assert(Token.t_comma, token)
        args.append(self._assert_arg())
        return self._args_cont(args)


class ParserException(Exception):
    """Parser exception"""
    pass


class Scanner:
    """Expression Scanner"""

    def __init__(self, es):
        self.es = es
        self.start = 0
        self.pos = 0
        self.value = None
        self.token = None

    def result(self, token, p, is_string=False, char_term=False):
        val_start = self.start + 1 if is_string else self.start
        val_end = p - 1 if is_string else p
        self.value = self.es[val_start:val_end]
        self.start = p if char_term else p + 1
        return token

    def result_char(self, token, char_token, p):
        if token == Token.t_empty:
            self.start = p + 1
            self.value = None
            return char_token
        else:
            return self.result(token, p, char_term=True)

    def scan(self):
        es = self.es
        if len(es) <= self.start:
            return Token.t_end
        if es[self.start] in string.whitespace:
            self.start += 1
        p = self.start
        token = Token.t_empty
        while p < len(es):
            c = es[p]
            if token == Token.t_string:
                if c == "'":
                    return self.result(token, p, is_string=True)
            elif c == ',':
                return self.result_char(token, Token.t_comma, p);
            elif c == '(':
                return self.result_char(token, Token.t_lpar, p);
            elif c == ')':
                return self.result_char(token, Token.t_rpar, p);
            elif c == '=':
                return self.result_char(token, Token.t_eq, p);
            elif c in string.whitespace:
                self.start = p
                return token
            elif c == "'":
                if not token:
                    raise ScannerException("single quote beginning of string")
                token = Token.t_string
            elif c in string.digits:
                if not token:
                    token = Token.t_int
            elif c == '.':
                if token == Token.t_float:
                    raise ScannerException("double floating point")
                token = Token.t_float
            elif c in string.ascii_letters:
                if token not in (Token.t_empty, Token.t_ident):
                    raise ScannerException("letter")
                token = Token.t_ident
            else:
                raise ScannerException("invalid character")
            p += 1
        if token == Token.t_string:
            raise ScannerException("unclosed string")
        return Token.t_end


class ScannerException(Exception):
    """Scanner exception"""
    pass

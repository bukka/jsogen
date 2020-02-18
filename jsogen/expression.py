import string
from .function import Function

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
    t_minus = 10
    t_plus = 11
    t_bool = 12
    t_none = 13
    t_end = 14


class Parser:
    """Parser
    
    Grammar (BNF):
    
        <parse>     ::= <fce>
        <fce>       ::= <IDENT> "(" <arg>
        <arg>       ::= value <arg-cont> | narg | ")"
        <arg-cont>  ::= "," <arg> | ")"
        <narg>      ::= <IDENT> "=" value <narg_cont> | ")"
        <narg-cont> ::= "," <narg> | ")"
        <value>     ::= <STRING> | <BOOL> | <NONE> | <number>
        <number>    ::= "-" <unumber> | "+" <unumber> | <unumber>
        <unumber>   ::= <INT> | <FLOAT>
    
    """

    def __init__(self, es):
        self.scanner = Scanner(es)

    def _scan_value(self):
        return self.scanner.value

    def _scan_token(self):
        return self.scanner.token

    def _scan_next(self):
        return self.scanner.scan()

    def _assert(self, expected_tokens, token=False):
        if not isinstance(expected_tokens, list):
            expected_tokens = [expected_tokens]
        if not token:
            token = self._scan_next()
        if not token in expected_tokens:
            raise ParserException("Expected %s token, provided %d" % (' or '.join(map(str, expected_tokens)), token))
        return self._scan_value()

    def parse(self):
        fce = self._function()
        self._assert(Token.t_end)
        return fce

    def _function(self):
        name = self._assert(Token.t_ident)
        self._assert(Token.t_lpar)
        args = []
        nargs = {}
        self._arg(args, nargs)
        return Function(name, args, nargs)

    def _arg(self, args, nargs):
        token = self._scan_next()
        if token in (Token.t_ident, Token.t_end, Token.t_rpar):
            self._narg(nargs)
        else:
            args.append(self._value(token))
            self._arg_cont(args, nargs)

    def _arg_cont(self, args, nargs):
        self._assert([Token.t_comma, Token.t_rpar])
        self._arg(args, nargs)

    def _narg(self, nargs):
        token = self._scan_token()
        if token == Token.t_rpar:
            return
        name = self._scan_value()
        self._assert(Token.t_eq)
        nargs[name] = self._value()
        self._narg_cont(nargs)

    def _narg_cont(self, nargs):
        self._assert([Token.t_comma, Token.t_rpar])
        self._scan_next()
        self._narg(nargs)

    def _value(self, token=False):
        if not token:
            token = self._scan_next()
        value = self._scan_value()
        if token in (Token.t_string, Token.t_bool, Token.t_none):
            return value
        else:
            return self._number(token, value)

    def _number(self, token, value):
        if token in (Token.t_minus, Token.t_plus):
            minus = token == Token.t_minus
            self._scan_next()
            token = self._scan_token()
            value = self._scan_value()
        else:
            minus = False
        unumber = self._unumber(token, value)
        return -1 * unumber if minus else unumber

    def _unumber(self, token, value):
        if token == Token.t_int:
            return int(value)
        if token == Token.t_float:
            return float(value)
        # invalid argument
        raise ParserException("Invalid argument token %d" % token)


class ParserException(Exception):
    """Parser exception"""
    pass


class Scanner:
    """Expression Scanner"""

    ident_letters = string.ascii_letters + '_'

    def __init__(self, es):
        self.es = es
        self.start = 0
        self.pos = 0
        self.value = None
        self.token = None

    def result(self, token, p, is_string=False, char_term=False):
        val_start = self.start + 1 if is_string else self.start
        val_end = p
        self.value = self.es[val_start:val_end]
        self.start = p if char_term else p + 1
        if token == Token.t_ident:
            # ident is case insensitive
            self.value = self.value.lower()
            if self.value == 'true':
                token = Token.t_bool
                self.value = True
            elif self.value == 'false':
                token = Token.t_bool
                self.value = False
            elif self.value == 'none':
                token = Token.t_none
                self.value = None
        self.token = token
        return token

    def result_char(self, token, char_token, p):
        if token == Token.t_empty:
            self.start = p + 1
            self.value = None
            self.token = char_token
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
            elif c == '-':
                return self.result_char(token, Token.t_minus, p);
            elif c == '+':
                return self.result_char(token, Token.t_plus, p);
            elif c in string.whitespace:
                return self.result(token, p)
            elif c == "'":
                if token:
                    raise ScannerException("single quote beginning of string")
                token = Token.t_string
            elif c in string.digits:
                if not token:
                    token = Token.t_int
            elif c == '.':
                if token == Token.t_float:
                    raise ScannerException("double floating point")
                token = Token.t_float
            elif c in Scanner.ident_letters:
                if token not in (Token.t_empty, Token.t_ident):
                    raise ScannerException("letter")
                token = Token.t_ident
            else:
                print(c)
                raise ScannerException("invalid character")
            p += 1
        if token == Token.t_string:
            raise ScannerException("unclosed string")
        self.token = Token.t_end
        return self.token


class ScannerException(Exception):
    """Scanner exception"""
    pass

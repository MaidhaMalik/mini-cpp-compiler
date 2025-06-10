class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', None)

    def match(self, expected_type):
        if self.current()[0] == expected_type:
            self.pos += 1
        else:
            raise SyntaxError(f"Expected {expected_type}, got {self.current()}")

    def parse(self):
        ast = []
        while self.current()[0] != 'EOF':
            ast.append(self.statement())
        return ast

    def statement(self):
        if self.current()[0] == 'TYPE':
            return self.declaration()
        else:
            raise SyntaxError(f"Invalid statement start: {self.current()}")

    def declaration(self):
        self.match('TYPE')
        var_name = self.current()[1]
        self.match('ID')
        self.match('ASSIGN')
        expr = self.expression()
        self.match('SEMI')
        return ('declare', var_name, expr)

    def expression(self):
        left = self.term()
        while self.current()[0] == 'OP' and self.current()[1] in ('+', '-'):
            op = self.current()[1]
            self.match('OP')
            right = self.term()
            left = ('binop', op, left, right)
        return left

    def term(self):
        left = self.factor()
        while self.current()[0] == 'OP' and self.current()[1] in ('*', '/'):
            op = self.current()[1]
            self.match('OP')
            right = self.factor()
            left = ('binop', op, left, right)
        return left

    def factor(self):
        if self.current()[0] == 'NUMBER':
            val = self.current()[1]
            self.match('NUMBER')
            return ('num', val)
        elif self.current()[0] == 'ID':
            name = self.current()[1]
            self.match('ID')
            return ('var', name)
        elif self.current()[0] == 'LPAREN':
            self.match('LPAREN')
            expr = self.expression()
            self.match('RPAREN')
            return expr
        else:
            raise SyntaxError(f"Unexpected token: {self.current()}")

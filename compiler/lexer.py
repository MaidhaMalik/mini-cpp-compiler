import re

token_specification = [
    ('NUMBER',   r'\d+'),
    ('ID',       r'[A-Za-z_]\w*'),
    ('ASSIGN',   r'='),
    ('SEMI',     r';'),
    ('OP',       r'[+\-*/]'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('TYPE',     r'\bint\b|\bfloat\b'),
    ('SKIP',     r'[ \t]+'),
    ('NEWLINE',  r'\n'),
    ('MISMATCH', r'.'),
]

token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
keywords = {"int", "float"}

def tokenize(code):
    tokens = []
    for mo in re.finditer(token_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            value = int(value)
        elif kind == 'ID' and value in keywords:
            kind = 'TYPE'
        elif kind in ['SKIP', 'NEWLINE']:
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character {value!r}')
        tokens.append((kind, value))
    tokens.append(('EOF', None))
    return tokens

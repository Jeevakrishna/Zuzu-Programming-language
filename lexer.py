
import re

TOKEN_REGEX = [
    ('NUMBER', r'\d+(\.\d+)?'),
    ('STRING', r'\".*?\"'),
    ('SAY', r'say|yell'),
    ('PLANT', r'plant|keep'),
    ('IF', r'check'),
    ('ELSE', r'flip'),
    ('HOP', r'hop'),
    ('MAGIC', r'magic'),
    ('CAST', r'cast'),
    ('RETURN', r'return'),
    ('END', r'end'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MULT', r'\*'),
    ('DIV', r'/'),
    ('MOD', r'%'),
    ('EQ', r'=='),
    ('NE', r'!='),
    ('GT', r'>'),
    ('LT', r'<'),
    ('GE', r'>='),
    ('LE', r'<='),
    ('EQUALS', r'='),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('COLON', r':'),
    ('NAME', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
]

def tokenize(code):
    tokens = []
    while code:
        match = None
        for tok_type, regex in TOKEN_REGEX:
            pattern = re.compile(regex)
            match = pattern.match(code)
            if match:
                value = match.group(0)
                if tok_type != 'SKIP':
                    tokens.append((tok_type, value))
                code = code[len(value):]
                break
        if not match:
            raise SyntaxError(f'Unknown token: {code}')
    return tokens

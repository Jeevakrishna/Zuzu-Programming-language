
from lexer import tokenize

class Node: pass
class ExpressionNode(Node): pass

class NumberNode(ExpressionNode): 
    def __init__(self, value): self.value = float(value)
class StringNode(ExpressionNode): 
    def __init__(self, value): self.value = value.strip('"')
class VarNode(ExpressionNode): 
    def __init__(self, name): self.name = name
class BinOpNode(ExpressionNode):
    def __init__(self, left, op, right): self.left = left; self.op = op; self.right = right

class SayNode(Node): 
    def __init__(self, expr): self.expr = expr
class PlantNode(Node): 
    def __init__(self, name, expr): self.name = name; self.expr = expr
class AssignNode(Node): 
    def __init__(self, name, expr): self.name = name; self.expr = expr
class IfNode(Node): 
    def __init__(self, cond, body, else_body=None): self.cond = cond; self.body = body; self.else_body = else_body
class WhileNode(Node): 
    def __init__(self, cond, body): self.cond = cond; self.body = body
class FunctionDef(Node):
    def __init__(self, name, body): self.name = name; self.body = body
class FunctionCall(Node): 
    def __init__(self, name): self.name = name
class ReturnNode(Node):
    def __init__(self, expr): self.expr = expr

def parse(tokens):
    pos = 0
    ast = []

    def current(): return tokens[pos] if pos < len(tokens) else ('EOF', '')
    def advance(): nonlocal pos; pos += 1; return current()

    def parse_expr():
        left = parse_term()
        while current()[0] in ('PLUS', 'MINUS', 'EQ', 'NE', 'GT', 'LT', 'GE', 'LE'):
            op = current()[1]; advance()
            right = parse_term()
            left = BinOpNode(left, op, right)
        return left

    def parse_term():
        left = parse_factor()
        while current()[0] in ('MULT', 'DIV', 'MOD'):
            op = current()[1]; advance()
            right = parse_factor()
            left = BinOpNode(left, op, right)
        return left

    def parse_factor():
        tok_type, tok_val = current()
        if tok_type == 'NUMBER':
            advance(); return NumberNode(tok_val)
        elif tok_type == 'STRING':
            advance(); return StringNode(tok_val)
        elif tok_type == 'NAME':
            advance(); return VarNode(tok_val)
        return None

    def parse_block():
        block = []
        while current()[0] not in ('END', 'ELSE', 'EOF'):
            block.append(parse_stmt())
        return block

    def parse_stmt():
        tok_type, tok_val = current()

        if tok_type == 'SAY':
            advance()
            return SayNode(parse_expr())

        if tok_type == 'PLANT':
            advance()
            name = current()[1]; advance()
            if current()[0] == 'EQUALS':
                advance()
                return PlantNode(name, parse_expr())

        if tok_type == 'NAME' and tokens[pos+1][0] == 'EQUALS':
            name = tok_val; advance(); advance()
            return AssignNode(name, parse_expr())

        if tok_type == 'IF':
            advance()
            cond = parse_expr()
            if current()[0] == 'COLON': advance()
            body = parse_block()
            else_body = None
            if current()[0] == 'ELSE':
                advance()
                if current()[0] == 'COLON': advance()
                else_body = parse_block()
            return IfNode(cond, body, else_body)

        if tok_type == 'HOP':
            advance()
            cond = parse_expr()
            if current()[0] == 'COLON': advance()
            body = parse_block()
            return WhileNode(cond, body)

        if tok_type == 'MAGIC':
            advance()
            name = current()[1]; advance()
            if current()[0] == 'COLON': advance()
            body = parse_block()
            if current()[0] == 'END': advance()
            return FunctionDef(name, body)

        if tok_type == 'CAST':
            advance()
            name = current()[1]; advance()
            return FunctionCall(name)

        if tok_type == 'RETURN':
            advance()
            return ReturnNode(parse_expr())

        advance()  # skip unknown
        return None

    while current()[0] != 'EOF':
        stmt = parse_stmt()
        if stmt: ast.append(stmt)

    return ast

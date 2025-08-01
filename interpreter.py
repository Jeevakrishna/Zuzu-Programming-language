
from lexer import tokenize
from parser import parse, SayNode, PlantNode, AssignNode, VarNode, NumberNode, StringNode, BinOpNode,     IfNode, WhileNode, FunctionDef, FunctionCall, ReturnNode

class Env:
    def __init__(self):
        self.vars = {}
        self.funcs = {}
        self.ret_val = None

    def run(self, code):
        tokens = tokenize(code)
        ast = parse(tokens)
        for node in ast:
            self.eval(node)

    def eval(self, node):
        if isinstance(node, SayNode):
            print(self.eval_expr(node.expr))
        elif isinstance(node, PlantNode):
            self.vars[node.name] = self.eval_expr(node.expr)
        elif isinstance(node, AssignNode):
            self.vars[node.name] = self.eval_expr(node.expr)
        elif isinstance(node, IfNode):
            if self.eval_expr(node.cond):
                for stmt in node.body:
                    self.eval(stmt)
            elif node.else_body:
                for stmt in node.else_body:
                    self.eval(stmt)
        elif isinstance(node, WhileNode):
            while self.eval_expr(node.cond):
                for stmt in node.body:
                    self.eval(stmt)
        elif isinstance(node, FunctionDef):
            self.funcs[node.name] = node
        elif isinstance(node, FunctionCall):
            func = self.funcs.get(node.name)
            if func:
                for stmt in func.body:
                    self.eval(stmt)
                    if self.ret_val is not None:
                        val = self.ret_val
                        self.ret_val = None
                        return val
        elif isinstance(node, ReturnNode):
            self.ret_val = self.eval_expr(node.expr)

    def eval_expr(self, expr):
        if isinstance(expr, NumberNode): return expr.value
        elif isinstance(expr, StringNode): return expr.value
        elif isinstance(expr, VarNode): return self.vars.get(expr.name, 0)
        elif isinstance(expr, BinOpNode):
            left = self.eval_expr(expr.left)
            right = self.eval_expr(expr.right)
            if expr.op == '+': return left + right
            if expr.op == '-': return left - right
            if expr.op == '*': return left * right
            if expr.op == '/': return left / right
            if expr.op == '%': return left % right
            if expr.op == '==': return left == right
            if expr.op == '!=': return left != right
            if expr.op == '>': return left > right
            if expr.op == '<': return left < right
            if expr.op == '>=': return left >= right
            if expr.op == '<=': return left <= right
        return 0

if __name__ == "__main__":
    code = """
plant name = \"Zuzu\"
say \"Hello, \" + name

plant x = 5
hop x > 0:
    say x
    x = x - 1

magic greet:
    say \"Hi from function\"
end

cast greet
"""
    Env().run(code)

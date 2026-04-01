import ast
import operator

class Calculator:
    operators = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
                 ast.Div: operator.truediv, ast.Pow: operator.pow, ast.BitXor: operator.xor,
                 ast.USub: operator.neg}

    def evaluate(self, expression: str) -> str:
        try:
            return str(self._eval_node(ast.parse(expression, mode='eval').body))
        except Exception as e:
            return f"Error computing '{expression}': {str(e)}"

    def _eval_node(self, node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return self.operators[type(node.op)](self._eval_node(node.left), self._eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):
            return self.operators[type(node.op)](self._eval_node(node.operand))
        else:
            raise TypeError(node)

if __name__ == "__main__":
    calc = Calculator()
    print(calc.evaluate("5 * (3 + 2)"))
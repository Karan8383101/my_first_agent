import ast
import operator

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def evaluate_expression(expr):
    """Evaluate a safe arithmetic expression string."""
    node = ast.parse(expr, mode="eval")
    return _eval_node(node.body)


def _eval_node(node):
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in OPERATORS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        return OPERATORS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return OPERATORS[op_type](operand)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed")
    raise ValueError(f"Unsupported expression: {type(node).__name__}")


def print_help():
    print("Calculator App")
    print("Enter arithmetic expressions like: 2 + 3 * 4")
    print("Supported operators: +, -, *, /, **")
    print("Type 'exit' or 'quit' to leave.")


def main():
    print_help()
    while True:
        try:
            expression = input("calc> ").strip()
            if not expression:
                continue
            if expression.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break
            result = evaluate_expression(expression.replace("^", "**"))
            print(result)
        except Exception as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()

"""
Safe scientific expression evaluator.
Provides evaluate(expr: str) -> float which supports math functions and operators.
Uses ast to restrict allowed operations.
"""
import ast
import operator as op
import math

# Supported binary operators
BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
}

# Supported unary operators
UNARY_OPS = {
    ast.UAdd: lambda x: x,
    ast.USub: op.neg,
}

# Allowed names mapped to math functions/constants
ALLOWED_NAMES = {
    name: getattr(math, name)
    for name in (
        'sin','cos','tan','asin','acos','atan',
        'sinh','cosh','tanh','asinh','acosh','atanh',
        'radians','degrees','log','log10','exp','sqrt','pow','fabs','factorial'
    )
    if hasattr(math, name)
}
# Add constants
ALLOWED_NAMES.update({'pi': math.pi, 'e': math.e})

# Add some aliases
ALLOWED_NAMES.update({'ln': math.log, 'log2': getattr(math, 'log2', None)})
ALLOWED_NAMES = {k: v for k, v in ALLOWED_NAMES.items() if v is not None}


class EvalError(Exception):
    pass


def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Constant):
        return node.value

    # for Python <3.8 compatibility, Num
    if isinstance(node, ast.Num):
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in BIN_OPS:
            try:
                return BIN_OPS[op_type](left, right)
            except Exception as e:
                raise EvalError(str(e))
        raise EvalError(f"Unsupported binary operator: {op_type}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in UNARY_OPS:
            return UNARY_OPS[op_type](operand)
        raise EvalError(f"Unsupported unary operator: {op_type}")

    if isinstance(node, ast.Call):
        # Only allow simple function call names
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in ALLOWED_NAMES:
                func = ALLOWED_NAMES[func_name]
                args = [_eval_node(a) for a in node.args]
                try:
                    return func(*args)
                except Exception as e:
                    raise EvalError(str(e))
            raise EvalError(f"Use of function '{func_name}' is not allowed")
        raise EvalError("Only simple function calls allowed")

    if isinstance(node, ast.Name):
        if node.id in ALLOWED_NAMES:
            return ALLOWED_NAMES[node.id]
        raise EvalError(f"Use of name '{node.id}' is not allowed")

    if isinstance(node, ast.Tuple):
        return tuple(_eval_node(elt) for elt in node.elts)

    raise EvalError(f"Unsupported expression: {ast.dump(node)}")


def evaluate(expr: str):
    """Evaluate a math expression safely.

    Supported: numbers, + - * / // % **, unary +/-, calls to allowed math functions,
    and constants pi, e.

    Raises EvalError on invalid input.
    """
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise EvalError(f"Syntax error: {e}")

    # Walk AST and ensure it contains only allowed node types
    for node in ast.walk(parsed):
        if not isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
                                 ast.Call, ast.Name, ast.Load, ast.Pow, ast.Add, ast.Sub,
                                 ast.Mult, ast.Div, ast.Mod, ast.FloorDiv, ast.USub, ast.UAdd,
                                 ast.Tuple)):
            raise EvalError(f"Disallowed expression or node: {type(node).__name__}")

    return _eval_node(parsed)


if __name__ == '__main__':
    while True:
        try:
            s = input('expr> ')
            if not s:
                continue
            print(evaluate(s))
        except (EOFError, KeyboardInterrupt):
            break
        except EvalError as e:
            print('Error:', e)
        except Exception as e:
            print('Unexpected error:', e)

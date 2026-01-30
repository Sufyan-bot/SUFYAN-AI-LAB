# Scientific Calculator (Tkinter)

A small safe scientific calculator implemented in Python using a restricted AST-based evaluator and a Tkinter GUI.

Files
- `calculator.py` - Safe expression evaluator using Python's `ast` and `math` functions. Use `evaluate(expr: str)` to evaluate expressions.
- `main.py` - Tkinter GUI application. Run this to open the calculator window.
- `test_calculator.py` - Small unit tests for core functionality.

Requirements
- Pure Python standard library. Tkinter is used for the GUI (usually bundled with the system Python). No external packages required.

How to run (Windows PowerShell)

Run the GUI:

```powershell
python "f:\lab ai\main.py"
```

Run the tests:

```powershell
python "f:\lab ai\test_calculator.py"
```

Usage notes
- The evaluator accepts numeric expressions using +, -, *, /, //, %, ** and unary +/-. 
- Scientific functions available: sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, asinh, acosh, atanh, radians, degrees, log (natural log), log10, log2 (if available), exp, sqrt, pow, fabs, factorial, and constants `pi` and `e`.
- Use function calls like `sin(pi/2)`, `sqrt(16)`, or `ln(e)` (alias for natural log).

Security
- The evaluator uses Python's `ast` to whitelist nodes and function names. Arbitrary code execution is disallowed.

License
- Public domain / MIT-style (use as you wish).

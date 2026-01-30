"""
Tkinter-based scientific calculator GUI.
Depends on `calculator.evaluate` for expression evaluation.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from calculator import evaluate, EvalError


class SciCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Scientific Calculator')
        self.resizable(False, False)
        self._create_widgets()

    def _create_widgets(self):
        self.expr_var = tk.StringVar()

        entry = ttk.Entry(self, textvariable=self.expr_var, font=('Consolas', 16), width=26)
        entry.grid(row=0, column=0, columnspan=6, padx=6, pady=6)
        entry.focus()

        btns = [
            ('7', '8', '9', '/', 'sqrt', '(',),
            ('4', '5', '6', '*', 'pow', ')',),
            ('1', '2', '3', '-', 'log', 'ln',),
            ('0', '.', '%', '+', 'sin', 'cos',),
            ('tan', 'pi', 'e', 'exp', 'CLEAR', 'DEL'),
            ('ANS', '=', '', '', '', ''),
        ]

        for r, row in enumerate(btns, start=1):
            for c, label in enumerate(row):
                if not label:
                    continue
                btn = ttk.Button(self, text=label, command=lambda l=label: self._on_button(l))
                btn.grid(row=r, column=c, sticky='nsew', padx=3, pady=3)

        for c in range(6):
            self.grid_columnconfigure(c, weight=1)

    def _on_button(self, label):
        if label == 'CLEAR':
            self.expr_var.set('')
            return
        if label == 'DEL':
            self.expr_var.set(self.expr_var.get()[:-1])
            return
        if label == '=':
            self._evaluate()
            return
        if label == 'ANS':
            # Not implementing memory; paste last result if available
            try:
                with open('.last_ans', 'r') as f:
                    ans = f.read().strip()
                self.expr_var.set(self.expr_var.get() + ans)
            except Exception:
                pass
            return
        if label == 'pi':
            self.expr_var.set(self.expr_var.get() + 'pi')
            return
        if label == 'e':
            self.expr_var.set(self.expr_var.get() + 'e')
            return
        if label in ('sqrt', 'sin', 'cos', 'tan', 'log', 'ln', 'exp', 'pow'):
            if label == 'ln':
                label = 'ln'
            self.expr_var.set(self.expr_var.get() + f"{label}(")
            return
        if label == '%':
            self.expr_var.set(self.expr_var.get() + '%')
            return

        self.expr_var.set(self.expr_var.get() + label)

    def _evaluate(self):
        expr = self.expr_var.get()
        try:
            result = evaluate(expr)
            self.expr_var.set(str(result))
            # Save last answer
            try:
                with open('.last_ans', 'w') as f:
                    f.write(str(result))
            except Exception:
                pass
        except EvalError as e:
            messagebox.showerror('Evaluation error', str(e))
        except Exception as e:
            messagebox.showerror('Error', str(e))


if __name__ == '__main__':
    app = SciCalculator()
    app.mainloop()

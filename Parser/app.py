from flask import Flask, render_template, request
import re

app = Flask(__name__)

expressions = []
ERROR_EMPTY_EXPRESSION = "Expression can't be empty."
ERROR_MISMATCHED_PARENTHESES = "Mismatched parentheses."
ERROR_INVALID_OPERATOR = "Invalid operator: {}"
ERROR_INVALID_STRUCTURE = "Invalid expression structure."
ERROR_DIVISION_BY_ZERO = "Division by zero is not allowed."

class InvalidExpressionException(Exception):
    pass

def evaluate_expression(expression):
    expression = re.sub(r'//.*?//', '', expression).strip()

    if not expression:
        raise InvalidExpressionException(ERROR_EMPTY_EXPRESSION)

    def precedence(op):
        if op in ('+', '-'):
            return 1
        if op in ('*', '/'):
            return 2
        return 0

    def apply_operator(o, v):
        if len(v) < 2:
            raise InvalidExpressionException(ERROR_INVALID_STRUCTURE)
        operator = o.pop()
        right = v.pop()
        left = v.pop()
        if operator == '+':
            v.append(left + right)
        elif operator == '-':
            v.append(left - right)
        elif operator == '*':
            v.append(left * right)
        elif operator == '/':
            if right == 0:
                raise InvalidExpressionException(ERROR_DIVISION_BY_ZERO)
            v.append(left / right)

    values = []
    operators = []
    i = 0

    while i < len(expression):
        char = expression[i]

        if char.isspace():
            i += 1
            continue

        if char.isdigit():
            num = 0
            while i < len(expression) and expression[i].isdigit():
                num = num * 10 + int(expression[i])
                i += 1
            values.append(num)
            i -= 1

        elif char == '(':
            operators.append(char)

        elif char == ')':
            while operators and operators[-1] != '(':
                apply_operator(operators, values)
            if not operators or operators[-1] != '(':
                raise InvalidExpressionException(ERROR_MISMATCHED_PARENTHESES)
            operators.pop()

        elif char in '+-*/':
            while (operators and operators[-1] != '(' and
                   precedence(operators[-1]) >= precedence(char)):
                apply_operator(operators, values)
            operators.append(char)

        else:
            raise InvalidExpressionException(ERROR_INVALID_OPERATOR.format(char))

        i += 1

    while operators:
        if operators[-1] == '(':
            raise InvalidExpressionException(ERROR_MISMATCHED_PARENTHESES)
        apply_operator(operators, values)

    if len(values) != 1:
        raise InvalidExpressionException(ERROR_INVALID_STRUCTURE)

    return values[0]



@app.route('/', methods=['GET', 'POST'])
def index():
    global expressions
    solved_expression = None
    result = None

    if request.method == 'POST':
        action = request.form.get('action')
        idx = request.form.get('index')

        try:
            if action == 'add':
                new_expression = request.form.get('expression')
                if not new_expression.strip():
                    raise InvalidExpressionException(ERROR_EMPTY_EXPRESSION)
                expressions.append(new_expression)
            elif action == 'delete' and idx is not None:
                idx = int(idx)
                if 0 <= idx < len(expressions):
                    del expressions[idx]
            elif action == 'solve' and idx is not None:
                idx = int(idx)
                if 0 <= idx < len(expressions):
                    solved_expression = expressions[idx]
                    result = evaluate_expression(solved_expression)
        except InvalidExpressionException as e:
            result = str(e)

    return render_template(
        'index.html',
        expressions=expressions,
        solved_expression=solved_expression,
        result=result,
    )


if __name__ == '__main__':
    app.run(debug=True)

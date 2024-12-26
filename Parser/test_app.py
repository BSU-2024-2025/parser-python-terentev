
import pytest
from app import (
    process_expression,
    ExpressionError,
    ERROR_EMPTY_INPUT,
    ERROR_UNBALANCED_PARENTHESES,
    ERROR_INVALID_OPERATOR,
    ERROR_SYNTAX_ERROR,
    ERROR_DIVIDE_BY_ZERO,
)

@pytest.mark.parametrize(
    "expression, expected_result",
    [
        ("8 + 2", 10),
        ("15 - 5", 10),
        ("3 * 7", 21),
        ("24 / 3", 8.0),
        ("6 + 2 * 3", 12),
        ("(4 + 3) * 2", 14),
        ("// ignored // 4 + 4", 8),
        ("9 // note // - 4", 5),
        ("(5 + 2) // extra comment // * 3", 21),
    ]
)
def test_valid_cases(expression, expected_result):
    assert process_expression(expression) == expected_result

@pytest.mark.parametrize(
    "expression, expected_exception, error_message",
    [
        ("8 +", ExpressionError, ERROR_SYNTAX_ERROR),
        ("(8", ExpressionError, ERROR_UNBALANCED_PARENTHESES),
        ("8)", ExpressionError, ERROR_UNBALANCED_PARENTHESES),
        ("24 / 0", ExpressionError, ERROR_DIVIDE_BY_ZERO),
        ("3 + 7 & 1", ExpressionError, ERROR_INVALID_OPERATOR.format("&")),
        ("// no expression //", ExpressionError, ERROR_EMPTY_INPUT),
        ("", ExpressionError, ERROR_EMPTY_INPUT),
    ]
)
def test_invalid_cases(expression, expected_exception, error_message):
    with pytest.raises(expected_exception) as exception:
        process_expression(expression)
    assert str(exception.value) == error_message
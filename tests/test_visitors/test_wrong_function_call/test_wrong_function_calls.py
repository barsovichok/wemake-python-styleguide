# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.wrong_function_call import (
    BAD_FUNCTIONS,
    WrongFunctionCallViolation,
    WrongFunctionCallVisitor,
)

regular_call = """
{0}(*args, **kwargs)
"""

assignment_call = """
test_result = {0}(*args, **kwargs)
"""

nested_function_call = """
def proxy(*args, **kwargs):
    return {0}(*args, **kwargs)
"""


@pytest.mark.parametrize('bad_function', BAD_FUNCTIONS)
@pytest.mark.parametrize('code', [
    regular_call,
    assignment_call,
    nested_function_call,
])
def test_wrong_function_called(
    assert_errors, parse_ast_tree, bad_function, code,
):
    """Testing that some built-in functions are restricted."""
    tree = parse_ast_tree(code.format(bad_function))

    visiter = WrongFunctionCallVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [WrongFunctionCallViolation])


@pytest.mark.parametrize('good_function', ['len', 'abs', 'max', 'custom'])
@pytest.mark.parametrize('code', [
    regular_call,
    assignment_call,
    nested_function_call,
])
def test_regular_function_called(
    assert_errors, parse_ast_tree, good_function, code,
):
    """Testing that other functions are not restricted."""
    tree = parse_ast_tree(code.format(good_function))

    visiter = WrongFunctionCallVisitor()
    visiter.visit(tree)

    assert_errors(visiter, [])

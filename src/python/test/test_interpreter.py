import pytest
from source.interpreter import Interpreter


def test_print_12():
    i = Interpreter()
    code = 'print("12")'
    return_values = i.executeString(code)
    expected = [
        {
            'begin': 0,
            'end': 1,
            'error_string': '',
            'output_string': '12',
            'return_value': ''
        }
    ]
    assert return_values == expected


def test_1_plus_12():
    i = Interpreter()
    code = '1 + 12'
    return_values = i.executeString(code)
    expected = [
        {
            'begin': 0,
            'end': 1,
            'error_string': '',
            'output_string': '',
            'return_value': '13'
        }
    ]
    assert return_values == expected


def test_1_plus_12_syntax_error():
    i = Interpreter()
    code = '1  12'
    return_values = i.executeString(code)
    expected = [
        {
            'begin': 0,
            'end': 1,
            'error_string': 'invalid syntax (<unknown>, line 1)',
            'output_string': '',
            'return_value': ''
        }
    ]
    assert return_values == expected


def test_def_hello():
    code = """def hello():
        return 'hello'"""
    i = Interpreter()
    return_values = i.executeString(code)
    expected = [
        {
            'begin': 0,
            'end': 2,
            'error_string': '',
            'output_string': '',
            'return_value': ''
        }
    ]
    assert return_values == expected


def test_def_and_call_hello():
    code = """def hello():
    return 'hello'

hello()
    """  # noqa
    i = Interpreter()
    return_values = i.executeString(code)
    expected = [
        {
            'begin': 0,
            'end': 2,
            'error_string': '',
            'output_string': '',
            'return_value': ''
        },
        {
            'begin': 3,
            'end': 4,
            'error_string': '',
            'output_string': '',
            'return_value': 'hello'
        }
    ]
    assert return_values == expected


def test_long_line_with_break():
    code = """0 + 1 + 2 + 3 + 4 + 5 + 6 + 7 +\
        8 + 9"""
    i = Interpreter()
    return_values = i.executeString(code)
    expected = [
       {
            'begin': 0,
            'end': 1,
            'error_string': '',
            'output_string': '',
            'return_value': '45'
        }
    ]
    assert return_values == expected


def test_print_two_times_after_each_other():
    code = """print(12)
print(12)"""
    i = Interpreter()
    return_values = i.executeString(code)
    expected = [
        {
            'begin': 0,
            'end': 1,
            'error_string': '',
            'output_string': '12',
            'return_value': ''
        },
        {
            'begin': 1,
            'end': 2,
            'error_string': '',
            'output_string': '12',
            'return_value': ''
        }
    ]
    assert return_values == expected


def test_import():
    code = "import math"
    i = Interpreter()
    return_values = i.executeString(code)
    expected = [
        {
            'begin': 0,
            'end': 1,
            'error_string': '',
            'output_string': '',
            'return_value': ''
        }
    ]
    assert return_values == expected


def test_import_and_use():
    code = """import math
math.e"""
    i = Interpreter()
    return_values = i.executeString(code)
    expected = [
        {
            'begin': 0,
            'end': 1,
            'error_string': '',
            'output_string': '',
            'return_value': ''
        },
        {
            'begin': 1,
            'end': 2,
            'error_string': '',
            'output_string': '',
            'return_value': '2.718281828459045'
        }
    ]
    assert return_values == expected


def test_import_and_use_in_function():
    code = """import math

def math_e():
        return math.e

math_e()"""
    i = Interpreter()
    return_values = i.executeString(code)
    expected = [
        {
            'begin': 0,
            'end': 1,
            'error_string': '',
            'output_string': '',
            'return_value': ''
        },
        {
            'begin': 2,
            'end': 4,
            'error_string': '',
            'output_string': '',
            'return_value': ''
        },
        {
            'begin': 5,
            'end': 6,
            'error_string': '',
            'output_string': '',
            'return_value': '2.718281828459045'
        }
    ]
    assert return_values == expected


def test_from_import():
    code = "from math import cos"
    i = Interpreter()
    return_values = i.executeString(code)
    expected = [
        {
            'begin': 0,
            'end': 1,
            'error_string': '',
            'output_string': '',
            'return_value': ''
        }
    ]
    assert return_values == expected


def test_from_import_and_use():
    code = """from math import cos

cos(0.5)"""
    i = Interpreter()
    return_values = i.executeString(code)
    expected = [
        {
            'begin': 0,
            'end': 1,
            'error_string': '',
            'output_string': '',
            'return_value': ''
        },
        {
            'begin': 2,
            'end': 3,
            'error_string': '',
            'output_string': '',
            'return_value': '0.8775825618903728'
        }
    ]
    assert return_values == expected


def test_from_import_and_use_in_function():
    code = """from math import cos

def math_cos(t):
        return cos(t)

math_cos(0.5)"""
    i = Interpreter()
    return_values = i.executeString(code)
    expected = [
        {
            'begin': 0,
            'end': 1,
            'error_string': '',
            'output_string': '',
            'return_value': ''
        },
        {
            'begin': 2,
            'end': 4,
            'error_string': '',
            'output_string': '',
            'return_value': ''
        },
        {
            'begin': 5,
            'end': 6,
            'error_string': '',
            'output_string': '',
            'return_value': '0.8775825618903728'
        }
    ]
    assert return_values == expected


def test_loop():
    code = """for i in range(10):
        print(i)"""
    i = Interpreter()
    return_values = i.executeString(code)
    expected = [
        {
            'begin': 0,
            'end': 2,
            'error_string': '',
            'output_string': '0 1 2 3 4 5 6 7 8 9',
            'return_value': ''
        }
    ]
    assert return_values == expected


def test_loop_return_string():
    code = """for i in range(10):
        i
    """
    i = Interpreter()
    return_values = i.executeString(code)
    expected = [
        {
            'begin': 0,
            'end': 2,
            'error_string': '',
            'output_string': '',
            'return_value': ''
        }
    ]
    assert return_values == expected


def test_np_random_random_sample():
    code = """import numpy as np
    
np.random.seed(1)
np.random.random_sample((5))
"""  # noqa
    i = Interpreter()
    return_values = i.executeString(code)
    expected = [
        {
            'begin': 0,
            'end': 1,
            'error_string': '',
            'output_string': '',
            'return_value': ''
        },
        {
            'begin': 2,
            'end': 3,
            'error_string': '',
            'output_string': '',
            'return_value': ''
        },
        {
            'begin': 3,
            'end': 4,
            'error_string': '',
            'output_string': '',
            'return_value': "[  4.17022005e-01   7.20324493e-01   1.14374817e-04   3.02332573e-01    1.46755891e-01]"  # noqa
        }
    ]
    assert return_values == expected


def test_long_example():
    code = """print('hello')

a = 12 + 11

def henk(piet):
    return 'henk en {}.'.format(piet)

henk('piet')

[(i,j) for j in range(2)
       for i in range(2)]

def long(alf, trump):
    assert(alf != trump)
    a = len(alf) - len(trump)
    if a == 0:
        return 'peanuts'
    elif a > 0:
        return 'alf is the real Trump'
    return 'Trump is the biggest alien'

a
"""  # noqa
    i = Interpreter()
    return_values = i.executeString(code)
    expected = [
        {
            'begin': 0,
            'end': 1,
            'error_string': '',
            'output_string': 'hello',
            'return_value': ''
        },
        {
            'begin': 2,
            'end': 3,
            'error_string': '',
            'output_string': '',
            'return_value': ''
        },
        {
            'begin': 4,
            'end': 6,
            'error_string': '',
            'output_string': '',
            'return_value': ''
        },
        {
            'begin': 7,
            'end': 8,
            'error_string': '',
            'output_string': '',
            'return_value': 'henk en piet.'
        },
        {
            'begin': 9,
            'end': 11,
            'error_string': '',
            'output_string': '',
            'return_value': '[(0, 0), (1, 0), (0, 1), (1, 1)]'
        },
        {
            'begin': 12,
            'end': 20,
            'error_string': '',
            'output_string': '',
            'return_value': ''
        },
        {
            'begin': 21,
            'end': 22,
            'error_string': '',
            'output_string': '',
            'return_value': '23'
        },
    ]
    assert return_values == expected


def test_array_over_two_lines():
    code = """[(i,j) for j in range(2)
        for i in range(2)]
    """  # noqa
    i = Interpreter()
    return_values = i.executeString(code)
    expected = [
        {
            'begin': 0,
            'end': 2,
            'error_string': '',
            'output_string': '',
            'return_value': '[(0, 0), (1, 0), (0, 1), (1, 1)]'
        },
    ]
    assert return_values == expected


def test_max_runtime_exceeded():
    code = """while True:
    123*66666
"""  # noqa
    i = Interpreter()
    return_values = i.executeString(code)
    expected = [
        {
            'begin': 0,
            'end': 2,
            'error_string': 'Timed out!',
            'output_string': '',
            'return_value': ''
        },
    ]
    assert return_values == expected


def test_result_is_False():
    code = "False"  # noqa
    i = Interpreter()
    return_values = i.executeString(code)
    expected = [
        {
            'begin': 0,
            'end': 1,
            'error_string': '',
            'output_string': '',
            'return_value': 'False'
        },
    ]
    assert return_values == expected


def test_result_is_None():
    code = "None"  # noqa
    i = Interpreter()
    return_values = i.executeString(code)
    expected = [
        {
            'begin': 0,
            'end': 1,
            'error_string': '',
            'output_string': '',
            'return_value': ''
        },
    ]
    assert return_values == expected


def test_result_is_Multilinestring():
    code = """\"\"\"Barry

Beaver"\"\""""
    i = Interpreter()
    return_values = i.executeString(code)
    expected = [
        {
            'begin': 0,
            'end': 3,
            'error_string': '',
            'output_string': '',
            'return_value': 'Barry  Beaver'
        },
    ]
    assert return_values == expected

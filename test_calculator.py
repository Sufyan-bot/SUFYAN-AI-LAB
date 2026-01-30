import math
from calculator import evaluate, EvalError


def test_basic():
    assert evaluate('1+2*3') == 7
    assert evaluate('2**3') == 8


def test_trig_and_constants():
    assert abs(evaluate('sin(pi/2)') - 1.0) < 1e-9
    assert abs(evaluate('cos(0)') - 1.0) < 1e-9


def test_sqrt_log():
    assert evaluate('sqrt(16)') == 4
    # natural log of e is 1
    assert abs(evaluate('ln(e)') - 1.0) < 1e-9


def test_error():
    try:
        evaluate('__import__("os").system("rm -rf /")')
    except EvalError:
        pass
    else:
        raise AssertionError('Unsafe expression should raise EvalError')


if __name__ == '__main__':
    test_basic()
    test_trig_and_constants()
    test_sqrt_log()
    test_error()
    print('All tests passed')

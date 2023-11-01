import os
import sys
import unittest
import random as ran
from decimal import Decimal
from os.path import abspath, dirname
from subprocess import CompletedProcess
from typing import Generator
from unittest.mock import MagicMock, call, patch

MFROOT = str(dirname(abspath(__file__)))
sys.path.append(MFROOT)

from myfuncs import (
    ALPHANUMERIC_CHARS,
    default_repr,
    get_terminal_width,
    is_jwt_str,
    nlprint,
    objinfo,
    print_columns,
    print_middle,
    ranstr,
    runcmd,
    typed_evar,
)

_valid_jwtstr = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZXN0IjoidGVzdCJ9.MZZ7UbJRJH9hFRdBUQHpMjU4TK4XRrYP5UxcAkEHvxE'


class TestRunCmd(unittest.TestCase):
    def test_runcmd_with_output(self):
        # Mock the subprocess.run() function to return a CompletedProcess object
        with patch(
            'subprocess.run',
            return_value=CompletedProcess(
                args=['echo', 'Hello, World!'],
                returncode=0,
                stdout='Hello, World!',
                stderr='',
            ),
        ):
            result = runcmd('echo Hello, World!', output=True)
        self.assertEqual(result, ['Hello, World!'])

    def test_runcmd_without_output(self):
        # Mock the subprocess.run() function to return None
        with patch('subprocess.run'):
            result = runcmd('echo Hello, World!', output=False)

        self.assertIsNone(result)


class TestPrintMiddle(unittest.TestCase):
    @patch("myfuncs.main.get_terminal_width", return_value=50)
    def test_print_middle_no_print(self, *args):
        tstr = '012345678901'
        clen = (50 - len(f' {tstr} ')) // 2
        with patch('builtins.print') as mock_print:
            result = print_middle(tstr, noprint=True)
        self.assertEqual(result, f'{clen * "="} {tstr} {clen * "="}')
        mock_print.assert_not_called()


class TestGetTerminalWidth(unittest.TestCase):
    def test_default_terminal_width(self):
        # When there's an OSError exception
        with patch('os.get_terminal_size', side_effect=OSError):
            result = get_terminal_width()
        self.assertEqual(result, 80)

    def test_actual_terminal_width(self):
        with patch(
            'os.get_terminal_size', return_value=os.terminal_size((100, 24))
        ):
            result = get_terminal_width()
        self.assertEqual(result, 100)


class TestPrintColumns(unittest.TestCase):
    teststrs = ['a' * i for i in range(1, 20)]

    def print_columns(self):
        result = print_columns(self.teststrs, terminal_width=80)
        ran.shuffle(self.teststrs)
        ranresult = print_columns(self.teststrs, terminal_width=80)

        for r in [result, ranresult]:
            self.assertEqual(len(r), 4)
            self.assertTrue(max(len(s) for s in r) == min(len(s) for s in r))


class TestRanStr(unittest.TestCase):
    def test_string_length(self):
        result = ranstr(5, 10)
        self.assertTrue(5 <= len(result) <= 10)

    def test_string_characters(self):
        chars = 'abcd'
        result = ranstr(5, 10, chars=chars)
        for char in result:
            self.assertIn(char, chars)

    def test_return_generator(self):
        result = ranstr(5, 10, as_generator=True)
        self.assertIsInstance(result, Generator)
        generated_string = ''.join(result)
        self.assertTrue(5 <= len(generated_string) <= 10)

    def test_return_string(self):
        result = ranstr(5, 10)
        self.assertIsInstance(result, str)
        self.assertTrue(5 <= len(result) <= 10)


class TestCustomReprFunction(unittest.TestCase):
    class MyClass:
        def __init__(self, a, b):
            self.a = a
            self.b = b

        def method(self):
            pass

    class AnotherClass:
        c = "class attribute"

        def __init__(self, x):
            self.x = x

    def test_simple_class(self):
        instance = self.MyClass(1, "test")
        representation = default_repr(instance)
        expected_repr = "MyClass(a=1, b='test')"
        self.assertEqual(representation, expected_repr)

    def test_class_with_class_attribute(self):
        instance = self.AnotherClass(5)
        representation = default_repr(instance)
        expected_repr = "AnotherClass(x=5)"
        self.assertEqual(representation, expected_repr)

    def test_builtin_type_without_dict(self):
        value = 123
        representation = default_repr(value)
        expected_repr = "int(123)"
        self.assertEqual(representation, expected_repr)

    def test_list(self):
        lst = [1, 2, 3]
        representation = default_repr(lst)
        expected_repr = "[1, 2, 3]"
        self.assertEqual(representation, expected_repr)

    def test_set(self):
        st = {1, 2, 3}
        representation = default_repr(st)
        expected_repr = "set({1, 2, 3})"
        self.assertEqual(representation, expected_repr)

    def test_float(self):
        value = 123.45
        representation = default_repr(value)
        expected_repr = "float(123.45)"
        self.assertEqual(representation, expected_repr)

    def test_tuple(self):
        tpl = (1, 2, 3)
        representation = default_repr(tpl)
        expected_repr = "(1, 2, 3)"
        self.assertEqual(representation, expected_repr)

    def test_dict(self):
        d = {'a': 1, 'b': 2}
        representation = default_repr(d)
        expected_repr = "{'a': 1, 'b': 2}"
        self.assertEqual(representation, expected_repr)

    def test_with_private_attribute(self):
        class WithPrivate:
            def __init__(self, x):
                self._x = x

        instance = WithPrivate(5)
        representation = default_repr(instance)
        expected_repr = "WithPrivate()"
        self.assertEqual(representation, expected_repr)


class TestTypedEvar(unittest.TestCase):
    def setUp(self):
        if 'TEST_VAR' in os.environ:
            del os.environ['TEST_VAR']

    # Tests for absence of the environment variable
    def test_no_default_and_no_value(self):
        self.assertIsNone(typed_evar('TEST_VAR'))

    def test_with_default_and_no_value(self):
        self.assertEqual(typed_evar('TEST_VAR', default=42), 42)

    # Tests for booleans
    def test_default_bool_with_true_value(self):
        os.environ['TEST_VAR'] = 'true'
        self.assertEqual(typed_evar('TEST_VAR', default=False), True)

    def test_default_bool_with_false_value(self):
        os.environ['TEST_VAR'] = 'false'
        self.assertEqual(typed_evar('TEST_VAR', default=True), False)

    def test_default_bool_with_invalid_value(self):
        os.environ['TEST_VAR'] = 'invalid_bool'
        with self.assertRaises(ValueError):
            typed_evar('TEST_VAR', default=False)

    def test_infer_bool_true(self):
        os.environ['TEST_VAR'] = 'true'
        self.assertEqual(typed_evar('TEST_VAR'), True)

    def test_infer_bool_false(self):
        os.environ['TEST_VAR'] = 'false'
        self.assertEqual(typed_evar('TEST_VAR'), False)

    # Tests for the behavior of 'true'/'false' values
    def test_default_bool_with_1_value(self):
        os.environ['TEST_VAR'] = '1'
        self.assertEqual(typed_evar('TEST_VAR', default=False), True)

    def test_default_bool_with_0_value(self):
        os.environ['TEST_VAR'] = '0'
        self.assertEqual(typed_evar('TEST_VAR', default=True), False)

    # Tests for numbers
    def test_infer_int(self):
        os.environ['TEST_VAR'] = '123'
        self.assertEqual(typed_evar('TEST_VAR'), 123)

    def test_infer_float(self):
        os.environ['TEST_VAR'] = '123.456'
        self.assertEqual(typed_evar('TEST_VAR'), 123.456)

    # Tests for strings
    def test_infer_str(self):
        os.environ['TEST_VAR'] = 'Hello World'
        self.assertEqual(typed_evar('TEST_VAR'), 'Hello World')

    # Tests for custom type (Decimal)
    def test_default_decimal_with_value(self):
        os.environ['TEST_VAR'] = '123.456'
        self.assertEqual(
            typed_evar('TEST_VAR', default=Decimal('0.0')), Decimal('123.456')
        )

    # Tests for bool as int inference
    def test_infer_bool_as_int_1(self):
        os.environ['TEST_VAR'] = '1'
        self.assertEqual(typed_evar('TEST_VAR', default=True), True)

    def test_infer_bool_as_int_0(self):
        os.environ['TEST_VAR'] = '0'
        self.assertEqual(typed_evar('TEST_VAR', default=True), False)

    def test_infer_bool_as_int_neg1(self):
        os.environ['TEST_VAR'] = '-1'
        self.assertEqual(typed_evar('TEST_VAR', default=True), False)

    # regression test for is_jwt_str() import
    def test_is_jwt_str_legacy(self):
        from .test_myfuncs import is_jwt_str

        self.assertTrue(is_jwt_str(_valid_jwtstr))


if __name__ == '__main__':
    unittest.main()

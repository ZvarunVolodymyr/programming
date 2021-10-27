import functools, unittest
from unittest import TestCase
from unit_test.help_function import false, true

import vaccine_class
import vaccine_validation
from validation import *


class TestValidation(TestCase):
    def test_is_float_number(self):
        false_ = functools.partial(false, obj=self, func=is_float_number)
        true_ = functools.partial(true, obj=self, func=is_float_number)
        false_('asd')
        false_('_1')
        false_('-1-1')
        true_('-1.52')

    def test_is_int_number(self):
        false_ = functools.partial(false, obj=self, func=is_int_number)
        true_ = functools.partial(true, obj=self, func=is_int_number)
        false_('asd')
        false_('_1-1')
        false_('-1.1')
        true_('-1')

    def test_is_natural_number(self):
        false_ = functools.partial(false, obj=self, func=is_natural_number)
        true_ = functools.partial(true, obj=self, func=is_natural_number)
        false_('asd')
        false_('_1-1')
        false_('-1.1')
        false_('-1')
        false_('0')
        true_('1')

    def test_is_menu(self):
        false_ = functools.partial(false, obj=self, func=is_menu)
        true_ = functools.partial(true, obj=self, func=is_menu)
        false_('on', ['one', 'two', 'three'])
        true_('one', ['one', 'two', 'three'])

    def test_is_in_list(self):
        false_ = functools.partial(false, obj=self, func=is_in_list)
        true_ = functools.partial(true, obj=self, func=is_in_list)
        false_('on', ['one', 'two', 'three'])
        true_('one', ['one', 'two', 'three'])

    def test_is_attribute(self):
        false_ = functools.partial(false, obj=self, func=is_attribute)
        true_ = functools.partial(true, obj=self, func=is_attribute)
        class A:
            b = 1
        false_(A(), 'B')
        true_(A(), 'b')

    def test_has_attribute(self):
        false_ = functools.partial(false, obj=self, func=has_attribute)
        true_ = functools.partial(true, obj=self, func=has_attribute)
        class A:
            b = 1
        false_('B', A())
        true_('b', A())

    def test_is_valid_array(self):
        false_ = functools.partial(false, obj=self, func=is_valid_array)
        true_ = functools.partial(true, obj=self, func=is_valid_array)
        false_('1 2 3 4 -5.1', is_int_number)
        false_('1 2 3 4 5', is_int_number, 4)
        true_('1,2,3,5', is_natural_number, 4, ',')

    def test_is_file(self):
        false_ = functools.partial(false, obj=self, func=is_file)
        true_ = functools.partial(true, obj=self, func=is_file)
        false_('input')
        true_('input.txt')

    def test_is_vaccine_filed(self):
        false_ = functools.partial(false, obj=self, func=is_vaccine_filed)
        true_ = functools.partial(true, obj=self, func=is_vaccine_filed)
        false_(-1, vaccine_class.COVID_CERTIFICATE().is_valid, 'id')
        false_('moderna', vaccine_class.COVID_CERTIFICATE().is_valid, 'vac')
        true_('pfizer', vaccine_class.COVID_CERTIFICATE().is_valid, 'vaccine')


if __name__ == '__main__':
    unittest.main()

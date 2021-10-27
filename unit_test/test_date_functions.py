import functools, unittest
from unittest import TestCase
from date_functions import *
from help_function import false, true


class TestDateFunctions(TestCase):
    def test_get_max_day_in_month(self):
        false_ = functools.partial(false, obj=self, func=get_max_day_in_month)
        true_ = functools.partial(true, obj=self, func=get_max_day_in_month)
        false_(-1, 0)
        self.assertEqual(true_(2, 2016), 29)
        self.assertEqual(true_(1, 2016), 31)
        self.assertEqual(true_(4, 2016), 30)

    def test_is_month_day(self):
        false_ = functools.partial(false, obj=self, func=is_month_day)
        true_ = functools.partial(true, obj=self, func=is_month_day)
        true_(1, 1, 1970)
        false_(30, 2, 2000)
        true_(31, 1, 1970)
        false_(31, 4, 1940)

    def test_is_date_term(self):
        false_ = functools.partial(false, obj=self, func=is_date_term)
        true_ = functools.partial(true, obj=self, func=is_date_term)
        false_('-1.0.0')
        false_('0.-1.-1')
        true_('100.0.10')

    def test_date_plus_date(self):
        false_ = functools.partial(false, obj=self, func=date_plus_date)
        true_ = functools.partial(true, obj=self, func=date_plus_date)
        false_('-1.-1.-1', '-1.0.10')
        self.assertEqual(true_('40.1.0', '41.1.1'), '21.4.1')
        self.assertEqual(true_('10.2.12', '21.2.12'), '2.5.24')
        self.assertEqual(true_('10.4.12', '21.4.12'), '1.9.24')

    def test_comparison(self):
        false_ = functools.partial(false, obj=self, func=comparison)
        true_ = functools.partial(true, obj=self, func=comparison)

        false_('1.-1.10', '1.1.1')
        self.assertEqual(true_('1.1.10', '1.2.12'), True)
        self.assertEqual(true_('2.1.10', '1.1.10'), False)

    def test_is_date(self):
        false_ = functools.partial(false, obj=self, func=is_date)
        true_ = functools.partial(true, obj=self, func=is_date)
        false_('1.12.-2001')
        false_('1.13.2001')
        false_('29.2.2013')
        true_('29.2.2012')
        true_('31.1.2003')

    def test_is_date_after_term(self):
        false_ = functools.partial(false, obj=self, func=is_date_after_term)
        true_ = functools.partial(true, obj=self, func=is_date_after_term)
        false_('1.10.1', '30.1.1', '0.8.0')
        false_('1.10.1', '1.1.1', '100.0.0')
        false_('29.2.2013', '1.1.1', '0.0.0')

        true_('1.10.1', '1.1.1', '500.0.0')
        true_('1.10.1', '30.1.1', '0.9.0')

    def test_is_date_between(self):
        false_ = functools.partial(false, obj=self, func=is_date_between)
        true_ = functools.partial(true, obj=self, func=is_date_between)
        false_('1.10.1', '30.1.1', '1.1.0', '1.8.0')
        false_('1.10.1', '1.1.1', '600.0.0', '50.0.0')
        false_('29.2.2013', '1.1.1', '0.0.0')

        true_('1.10.1', '1.1.1', '50.0.0', '600.0.0')
        true_('1.10.1', '30.1.1', '1.1.0', '1.9.0')

    def test_is_date_in_range(self):
        false_ = functools.partial(false, obj=self, func=is_date_in_range)
        true_ = functools.partial(true, obj=self, func=is_date_in_range)
        false_('1.10.1', '1.11.0', '1.2.2')
        false_('1.10.1', '1.11.2', '1.1.1')
        false_('1.10.1', '1.11.2', '1.1.0')

        true_('1.10.1', '1.1.1', '1.2.20')
        true_('1.3.2012', '28.2.2012', '2.3.2012')


if __name__ == '__main__':
    unittest.main()
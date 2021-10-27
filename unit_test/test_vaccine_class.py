from unittest import TestCase
import vaccine_class, unittest, functools
from unit_test.help_function import false, true


def correct_1():
    obj = vaccine_class.COVID_CERTIFICATE(5, 'Ab', '1.1.2000', '1.1.2001', '5.1.2001', 'moderna', 'aa000000')
    return obj


def correct_2():
    obj = vaccine_class.COVID_CERTIFICATE(1, 'a', '1.1.2000', '1.1.2011', '5.1.2011', 'moderna', 'aa000000')
    return obj


class TestCOVID_CERTIFICATE(TestCase):
    def test_has_value(self):
        obj = correct_1()
        self.assertEqual(obj.has_value(5), True)
        self.assertEqual(obj.has_value('2000'), False)
        self.assertEqual(obj.has_value('ab'), False)
        self.assertEqual(obj.has_value('Ab'), True)

    def test_is_valid(self):
        obj = correct_1()
        func = functools.partial(obj.is_valid, is_input=True)
        false_ = functools.partial(false, obj=self, func=func)
        true_ = functools.partial(true, obj=self, func=func)

        false_('id', -3)
        false_('username', 'asd1')
        false_('birth_date', '1.1.1900')
        false_('start_date', '30.2.2010')
        false_('end_date', '31.4.2002')
        false_('vaccine', 'mode')
        false_('international_passport', 'aa21')

        true_('id', 1)
        true_('username', 'asd')
        true_('birth_date', '1.1.1950')
        true_('start_date', '20.2.2010')
        true_('end_date', '6.1.2001')
        true_('vaccine', 'moderna')
        true_('international_passport', 'aa123456')

    def test_part_str(self):
        obj = correct_1()
        text = '5, Ab, 1.1.2000, 1.1.2001, 5.1.2001, moderna, aa000000'
        self.assertEqual(text, obj.part_str())

    def test_setattr(self):
        obj = correct_1()
        obj.setattr('id', 1)
        obj.setattr('id', -1)
        obj.setattr('username', 'a')
        obj.setattr('username', 'asd1')
        obj.setattr('start_date', '1.1.2011')
        obj.setattr('end_date', '5.1.2011')
        self.assertEqual(obj, correct_2())

    def test_getattr(self):
        obj = correct_1()
        false_ = functools.partial(false, obj=self, func=obj.getattr)
        true_ = functools.partial(true, obj=self, func=obj.getattr)
        false_('error')
        self.assertEqual(5, true_('id'))
        self.assertEqual('Ab', true_('username'))

    def test_get_attr_str(self):
        obj = correct_1()
        func = functools.partial(obj.get_attr_str, function='valid')
        false_ = functools.partial(false, obj=self, func=func)
        true_ = functools.partial(true, obj=self, func=func)
        false_('error')
        self.assertEqual('5', true_('id'))
        self.assertFalse(5 == true_('id'))
        self.assertEqual('Ab', true_('username'))


if __name__ == '__main__':
    unittest.main()
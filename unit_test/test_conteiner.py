from unittest import TestCase
import unittest
from unit_test.help_function import false, true
import functools
import conteiner
import vaccine_class


def correct_0():
    obj = conteiner.CertificateConteiner()
    return obj


def correct_1():
    obj = conteiner.CertificateConteiner()
    obj.append(vaccine_class.COVID_CERTIFICATE(5, 'Ab', '1.1.2000', '1.1.2001', '5.1.2001', 'moderna', 'aa000000'))
    obj.append(vaccine_class.COVID_CERTIFICATE(7, 'Cab', '1.1.2000', '1.1.2001', '5.1.2001', 'pfizer', 'aa000001'))
    return obj


def correct_2():
    obj = conteiner.CertificateConteiner()
    obj.append(vaccine_class.COVID_CERTIFICATE(5, 'Ab', '1.1.2000', '1.1.2001', '5.1.2001', 'moderna', 'aa000000'))
    obj.append(vaccine_class.COVID_CERTIFICATE(7, 'Cab', '1.1.2000', '1.1.2001', '5.1.2001', 'pfizer', 'aa000001'))
    obj.append(vaccine_class.COVID_CERTIFICATE(1, 'z', '1.1.2000', '1.1.2001', '5.1.2001', 'pfizer', 'aa000001'))
    return obj


def correct_3():
    obj = conteiner.CertificateConteiner()
    obj.append(vaccine_class.COVID_CERTIFICATE(1, 'z', '1.1.2000', '1.1.2001', '5.1.2001', 'pfizer', 'aa000001'))
    obj.append(vaccine_class.COVID_CERTIFICATE(5, 'Ab', '1.1.2000', '1.1.2001', '5.1.2001', 'moderna', 'aa000000'))
    obj.append(vaccine_class.COVID_CERTIFICATE(7, 'Cab', '1.1.2000', '1.1.2001', '5.1.2001', 'pfizer', 'aa000001'))
    return obj


def correct_4():
    obj = conteiner.CertificateConteiner()
    obj.append(vaccine_class.COVID_CERTIFICATE(5, 'Ab', '1.1.2000', '1.1.2001', '5.1.2001', 'moderna', 'aa000000'))
    obj.append(vaccine_class.COVID_CERTIFICATE(7, 'Cab', '1.1.2000', '1.1.2001', '5.1.2001', 'pfizer', 'aa000001'))
    obj.append(vaccine_class.COVID_CERTIFICATE(1, 'z', '1.1.2000', '1.1.2001', '5.1.2001', 'pfizer', 'aa000001'))
    return obj


def correct_5():
    obj = conteiner.CertificateConteiner()
    obj.append(vaccine_class.COVID_CERTIFICATE(5, 'Ab', '1.1.2000', '1.1.2001', '5.1.2001', 'moderna', 'aa000000'))
    obj.append(vaccine_class.COVID_CERTIFICATE(1, 'z', '1.1.2000', '1.1.2001', '5.1.2001', 'pfizer', 'aa000001'))
    return obj


class TestCertificateConteiner(TestCase):
    def test_input_from_file(self):
        obj = conteiner.CertificateConteiner()
        false_ = functools.partial(false, obj=self, func=obj.input_from_file)
        true_ = functools.partial(true, obj=self, func=obj.input_from_file)
        false_('error')
        true_('input.txt')
        self.assertEqual(obj, correct_1())

    def test_append(self):
        obj = conteiner.CertificateConteiner()
        false_ = functools.partial(false, obj=self, func=obj.append)
        true_ = functools.partial(true, obj=self, func=obj.append)
        true_(vaccine_class.COVID_CERTIFICATE(5, 'Ab', '1.1.2000', '1.1.2001', '5.1.2001', 'moderna', 'aa000000'))
        false_(4)
        true_(vaccine_class.COVID_CERTIFICATE(7, 'Cab', '1.1.2000', '1.1.2001', '5.1.2001', 'pfizer', 'aa000001'))
        self.assertEqual(obj, correct_1())

    def test_part_str(self):
        obj = correct_1()
        text = '5, Ab, 1.1.2000, 1.1.2001, 5.1.2001, moderna, aa000000|7, Cab, 1.1.2000, 1.1.2001, 5.1.2001, pfizer, aa000001|'
        self.assertEqual(obj.part_str(), text)

    def test_find_part(self):
        obj = correct_1()
        self.assertEqual([], obj.find_part('abc'))
        self.assertEqual([5], obj.find_part('na'))
        self.assertEqual([5, 7], obj.find_part('001'))
        self.assertEqual([7], obj.find_part('0001'))

    def test_find(self):
        obj = correct_1()
        class_1 = vaccine_class.COVID_CERTIFICATE(5, 'Ab', '1.1.2000', '1.1.2001', '5.1.2001', 'moderna', 'aa000000')
        class_2 = vaccine_class.COVID_CERTIFICATE(7, 'Cab', '1.1.2000', '1.1.2001', '5.1.2001', 'pfizer', 'aa000001')
        self.assertEqual([], obj.find('abc', field_name='username'))
        self.assertEqual([], obj.find('moderna', field_name='id'))
        self.assertEqual([class_1], obj.find('moderna', field_name='vaccine'))
        self.assertEqual([], obj.find('5', field_name='some_id'))
        self.assertEqual([class_1, class_2], obj.find('1.1.2000', field_name='birth_date'))

    def test_sort(self):
        obj = correct_2()
        true_ = functools.partial(true, obj=self, func=obj.sort)
        false_ = functools.partial(false, obj=self, func=obj.sort)
        true_('id')
        self.assertEqual(str(obj), str(correct_3()))
        true_('username')
        self.assertEqual(str(obj), str(correct_4()))
        false_('error')

    def test_remove(self):
        obj = correct_2()
        obj.remove(1)
        self.assertEqual(obj, correct_1())
        obj = correct_2()
        obj.remove(8)
        obj.remove(3, 'error')
        self.assertEqual(obj, correct_2())
        obj.remove('z', 'username')
        self.assertEqual(obj, correct_1())

    def test_change_by_id(self):
        obj = correct_5()
        obj.change_by_id(12)
        obj.change_by_id(1, ['id=asd', 'id=7', 'usernam=asd', 'username=Cab'])
        self.assertEqual(obj, correct_1())

    def test_clear(self):
        obj = correct_4()
        obj.clear()
        self.assertEqual(obj, correct_0())


if __name__ == '__main__':
    unittest.main()
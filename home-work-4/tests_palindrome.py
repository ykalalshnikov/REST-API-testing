import unittest
import palindrome


class PalindromeTests(unittest.TestCase):

    def test_palindrome(self):
        """ Checks word is palindrome, word consist of upper and lower register letters,
         register ignored . """

        palindrome_res = palindrome.is_palindrome(word='MaDam')
        self.assertTrue(palindrome_res, 'word is not palindrome')

    def test_not_palindrome(self):
        """ Checks word is not palindrome, word contains of upper and lower register letters,
                 register ignored . """

        palindrome_res = palindrome.is_palindrome(word='Qwerty')
        self.assertFalse(palindrome_res, 'word is palindrome, when should not')

    def test_palindrome_upper(self):
        """ Checks word is palindrome, word consist of upper register letters,
         register ignored . """

        palindrome_res = palindrome.is_palindrome(word='MADAM')
        self.assertTrue(palindrome_res, 'word is not palindrome')

    def test_not_palindrome_upper(self):
        """ Checks word is not palindrome, word consist of upper register letters,
                 register ignored . """

        palindrome_res = palindrome.is_palindrome(word='QWERTY')
        self.assertFalse(palindrome_res, 'word is palindrome, when should not')

    def test_palindrome_lower(self):
        """ Checks word is palindrome, word consist of lower register letters,
                 register ignored . """

        palindrome_res = palindrome.is_palindrome(word='madam')
        self.assertTrue(palindrome_res, 'word is not palindrome')

    def test_not_palindrome_lower(self):
        """ Checks word is not palindrome, word consist of lower register letters,
                         register ignored . """

        palindrome_res = palindrome.is_palindrome(word='qwerty')
        self.assertFalse(palindrome_res, 'word is palindrome, when should not')

    def test_palindrome_invalid_symbols(self):
        palindrome_res = palindrome.is_palindrome(word='qw()wq')
        self.assertEqual(palindrome_res, 'Word does not consist of letters',
                         'not required error text')

    def test_palindrome_consider_register_lower(self):
        """ Checks word is palindrome, word consist of lower register letters,
                         register not ignored . """

        palindrome_res = palindrome.is_palindrome(word='madam', register=True)
        self.assertTrue(palindrome_res, 'word is not palindrome')

    def test_not_palindrome_consider_register_lower(self):
        """ Checks word is not palindrome, word consist of lower register letters,
                                register not ignored . """

        palindrome_res = palindrome.is_palindrome(word='qwerty', register=True)
        self.assertFalse(palindrome_res, 'word is palindrome, when should not')

    def test_palindrome_consider_register_upper(self):
        """ Checks word is palindrome, word contains upper register letters,
                                register not ignored . """

        palindrome_res = palindrome.is_palindrome(word='Madam', register=True)
        self.assertFalse(palindrome_res, 'word is palindrome, when should not')

    def test_not_palindrome_consider_register_upper(self):
        """ Checks word is not palindrome, word contains upper register letters,
                                        register not ignored . """

        palindrome_res = palindrome.is_palindrome(word='Madam', register=True)
        self.assertFalse(palindrome_res, 'word is palindrome, when should not')

    def test_palindrome_register_invalid_symbols(self):
        palindrome_res = palindrome.is_palindrome(word='q()Q', register=True)
        self.assertEqual(palindrome_res, 'Word does not consist of letters',
                         'not required error text')

    def test_palindrome_many_letters(self):
        palindrome_res = palindrome.is_palindrome(word='qwewq'*100000, register=True)
        self.assertTrue(palindrome_res, 'word is not palindrome')


if __name__ == '__main__':
    unittest.main()
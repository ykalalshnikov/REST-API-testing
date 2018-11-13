""" This function cheks if the given word is palindrome."""


def is_palindrome(word, register=False):
    if word.isalpha():
        if not register:
            word = str(word).lower()
        else:
            word = str(word)
        reverse_word = word[::-1]
        return True if word == reverse_word else False
    else:
        return 'Word does not consist of letters'





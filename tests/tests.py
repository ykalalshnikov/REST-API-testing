#!/usr/bin/python3
# -*- encoding=utf8 -*-

import pytest

from tests.utils import *


def test_login():
    """ This test checks that login REST API works fine. """

    # Log in with valid credentials:
    data = auth()

    # Verify that server returns some auth cookie:
    assert data['my_cookie'] > '', 'empty auth cookie'


def test_wrong_user():
    """ This test checks that REST API return 401 on wrong login. """

    # Log in with invalid login:
    data = auth(user='qwe')

    # Verify that server returns unauthorized code 401:
    assert data == 401, 'status code is not 401'


def test_wrong_password():
    """ This test checks that REST API return 401 on wrong password. """

    # Log in with invalid password:
    data = auth(password='qwe')

    # Verify that server returns unauthorized code 401:
    assert data == 401, 'status code is not 401'


def test_wrong_credentials():
    """ This test checks that REST API return 401 on wrong credentials. """

    # Log in with invalid credentials:
    data = auth(user='qwe', password='qwe')

    # Verify that server returns unauthorized code 401:
    assert data == 401, 'status code is not 401'


def test_get_list_of_books():
    """ Check that 'get books' method returns correct list of books. """

    # Create three books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    # Get list of all books:
    all_books = get_all_books()

    # Check that every book in the list has all required attributes:
    for book in all_books:
        assert 'title' in book, 'no title of the book'
        assert 'author' in book, 'no book author'
        assert validate_uuid4(book['id']), 'invalid book id'

    # Make sure that the list has at least 3 books:
    assert len(all_books) >= 3, 'less than 3 books in the list'


@pytest.mark.parametrize('title', ['', 'TeSt', u'тест', '*^&%$%#{}[]()',
                                   'a'*1000000])
@pytest.mark.parametrize('author', ['', 'Teodor Drayzer', u'Пушкин',
                                    '*^&%$%#{}[]()', '!'*1000000])
def test_get_book_by_id(title, author):
    """ Check that 'get books by id' method returns correct books. """

    # Create three books, just to make sure books will be correctly
    # added to the list:
    add_three_books()
    book = add_book({'title': title, 'author': author})

    # Get second book id:
    getting_book = get_book(book['id'])

    # Get list of all books:
    all_books = get_all_books()

    # Make sure that
    assert getting_book == book, 'getting book not equals added'
    assert len(all_books) >= 4, 'less than 3 books in the list'


@pytest.mark.parametrize('book_id', ['TeSt', u'тест', '*^&%$%#{}[]()',
                                     'a'*1000000])
def test_get_book_by_nonexistent_id(book_id):
    """ Check that 'get book by id' method returns nothing on nonexistent id. """

    # Create three books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    # Get nonexistent book
    getting_book = get_book(book_id)

    # Get list of all books:
    all_books = get_all_books()

    # Make sure that getting book does not exist
    assert getting_book == {}, 'nonexistent book is exist'
    assert len(all_books) >= 3, 'less than 3 books in the list'


def test_get_sorted_list_of_books():
    """ Check that 'get books' method returns sorted list of books. """

    # Create Three books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    # Set sort filter:
    filters = {'sort': 'by_title'}

    # Get list of all books with filter:
    all_books = get_all_books(filters=filters)

    # Make sure that list is sorted
    assert all_books == sorted(all_books, key=lambda x: x['title']),\
        'list of books not sorted'


@pytest.mark.parametrize('sort', ['test', u'тест', 2])
def test_get_invalid_sorted_list_of_books(sort):
    """ Check that 'get books' method returns unsorted list of books on invalid
        sort param. """

    # Create three books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    # Set invalid sort filter:
    filters = {'sort': sort}

    # Get list of all books with filter:
    all_books = get_all_books(filters=filters)

    # Make sure that list is not sorted
    assert all_books != sorted(all_books, key=lambda x: x['title']),\
        'list of books sorted'


@pytest.mark.parametrize('limit', [1, 2, 3])
def test_get_limited_list_of_books(limit):
    """ Check that 'get books' method returns limited list of books. """

    # Create three books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    # Set limit filter:
    filters = {'limit': limit}

    # Get list of all books with filter:
    all_books = get_all_books(filters=filters)

    # Make sure that list is limited
    assert len(all_books) == limit, 'list of books not limited'


@pytest.mark.parametrize('limit', [0, -1, -2, -44])
def test_get_negative_limited_list_of_books(limit):
    """ Check that 'get books' method returns unlimited list of books
        on invalid limit param. """

    # Create three books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    # Set negative limit filter:
    filters = {'limit': limit}

    # Get list of all books with filter:
    all_books = get_all_books(filters=filters)

    # Make sure that list is not limited
    assert len(all_books) >= 3, 'less than 3 books in the list'


def test_get_more_max_limited_list_of_books():
    """ Check that 'get books' method returns unlimited list of books
        on limit > books. """

    # Create three books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    len_all_books = len(get_all_books())
    len_all_books = len_all_books + 10
    # Set negative limit filter:
    filters = {'limit': len_all_books}

    # Get list of all books with filter:
    all_books = get_all_books(filters=filters)

    # Make sure that list is not limited
    assert all_books != [], 'list of books is empty'
    assert len(all_books) != len_all_books, 'quantity of books equals wrong limit'


def test_get_invalid_limited_list_of_books():
    """ Check that 'get books' method returns correct unlimited list of books
        on invalid limit param. """

    # Create three books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    # Set invalid limit filter:
    filters = {'limit': 'qwe'}

    # Get list of all books with filter:
    all_books = get_all_books(filters=filters)

    # Make sure that list is not limited
    assert len(all_books) >= 3, 'less than 3 books in the list'


def test_get_sorted_and_limited_list_of_books():
    """ Check that 'get books' method returns sorted and limited list of books. """

    # Create two books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    # Set sort and limit filter:
    filters = {'sort': 'by_title', 'limit': 2}

    # Get list of all books with filter:
    all_books = get_all_books(filters=filters)

    # Make sure that list is sorted and limited
    assert all_books == sorted(all_books, key=lambda x: x['title']),\
        'list of books sorted'
    assert len(all_books) == 2, 'list of books not limited'


def test_similar_id_in_list():
    """ Check that there are no similar id in list of books. """

    # Create two books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    # Get list of all books
    all_books = get_all_books()

    # Create empty list
    a = []

    # Append similar ids to the list
    for i in all_books:
        print(i['id'])
        if (i['id']) not in a:
            a.append(i['id'])

    # Make sure that mo similar id in list
    assert len(a) == len(all_books), 'similar id in list of books'


@pytest.mark.parametrize('title', ['', 'TeSt', u'тест', '*^&%$%#{}[]()',
                                   'a'*1000000])
@pytest.mark.parametrize('author', ['', 'Teodor Drayzer', u'Пушкин',
                                    '*^&%$%#{}[]()', '!'*1000000])
def test_add_new_book(title, author):
    """ Check 'create book' method with different values of Title and Author. """

    # Create new book
    book = {'title': title, 'author': author}

    # Get new book
    new_book = add_book(book)

    # Get list of all books
    all_books = get_all_books()

    # Verify that book and params added correctly:
    assert new_book in all_books, 'new book not in list of the books'
    for book in all_books:
        if book['id'] == new_book['id']:
            assert book['title'] == title, 'no title of the book'
            assert book['author'] == author, 'no book author'
            assert validate_uuid4(book['id']), 'invalid book id'


def test_add_several_new_books():
    """ Check 'create book' method for several books. """

    # Create three books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    # Get list of all books
    all_books = get_all_books()

    # Make sure that more than 3 books in list
    assert len(all_books) >= 3, 'less than 3 books in the list'


def test_add_book_with_empty_title():
    """ Check 'create book' method with empty title. """

    # Create new book with empty title
    new_book = add_book({'author': 'Pushkin'})

    # Set empty title for new book
    new_book['title'] = ''

    # Get list of all books
    all_books = get_all_books()

    # Make sure that added book in list
    assert new_book in all_books, 'title of added book not empty'


def test_add_book_with_empty_author():
    """ Check 'create book' method with empty author.
             """
    # Create new book with empty author
    new_book = add_book({'title': 'Qwerty'})

    # Set 'No Name' author for new book
    new_book['author'] = 'No Name'

    # Get list of all books
    all_books = get_all_books()

    # Make sure that added book in list
    assert new_book in all_books, 'author of added book not No Name'


def test_add_book_with_empty_data():
    """ Check 'create book' method with empty title and author. """

    # Create new book with empty author
    new_book = add_book({})
    # Set empty title for new book and 'No Name' author for new book
    new_book['title'] = ''
    new_book['author'] = 'No Name'

    # Get list of all books
    all_books = get_all_books()

    # Make sure that added book in list
    assert new_book in all_books, 'title or author of added book' \
                                  ' is not empty and No Name'


@pytest.mark.parametrize('title', ['', 'TeSt', u'тест', '*^&%$%#{}[]()',
                                   'a'*1000000])
@pytest.mark.parametrize('author', ['', 'Teodor Drayzer', u'Пушкин',
                                    '*^&%$%#{}[]()', '!'*1000000])
def test_update_book(title, author):
    """ Check 'update book' method with different values of Title and Author. """

    # Create new book for update:
    new_book = add_book({'title': '', 'author': ''})
    book_id = new_book['id']

    # Update book attributes:
    update_book(book_id, {'title': title, 'author': author})

    # Get info about this book:
    book = get_book(book_id)

    # Verify that changes were applied correctly:
    assert book['title'] == title
    assert book['author'] == author


@pytest.mark.parametrize('title', ['', 'TeSt', u'тест', '*^&%$%#{}[]()',
                                   'a'*1000000])
@pytest.mark.parametrize('author', ['', 'Teodor Drayzer', u'Пушкин',
                                    '*^&%$%#{}[]()', '!'*1000000])
def  test_update_nonexistent_book(title, author):
    """ Check 'update book' method fro nonexistent book id. """

    # Create new book for update:
    add_book({'title': '', 'author': ''})
    book_id = 'qwe'

    # Update book attributes:
    result = update_book(book_id, {'title': title, 'author': author})

    # Make sure that there is correct error message
    assert result == {"message": "No book with given ID!"},\
        'wrong message of invalid cookie'


def test_delete_book():
    """ Check 'delete book' method. """

    # Create two books, just to make sure books will be correctly
    # added to the list:
    first_book = add_book({'title': 'B', 'author': ''})
    second_book = add_book({'title': '1', 'author': 'Pushkin'})

    # Create new book for delete:
    book = add_book({'title': '1', 'author': '2'})

    # Delete new book:
    deleted_book = delete_book(book['id'])

    # Get list of all books
    all_books = get_all_books()

    # Verify that book is not presented in the list:
    assert book not in all_books, 'added book not deleted'
    assert deleted_book == {"deleted": book['id']},\
        'not returned deleted book id'
    assert (first_book and second_book) in all_books, 'added books not in list'
    assert len(all_books) >= 3, 'less than 3 books in the list'


def test_double_delete_book():
    """ Check twice 'delete book' method. """

    # Create two books, just to make sure books will be correctly
    # added to the list:
    first_book = add_book({'title': 'B', 'author': ''})
    second_book = add_book({'title': '1', 'author': 'Pushkin'})

    # Create new book for delete:
    book = add_book({'title': '1', 'author': '2'})

    # Double delete new book:
    delete_book(book['id'])
    deleted_book = delete_book(book['id'])

    # Get list of all books
    all_books = get_all_books()

    # Verify that book is not presented in the list:
    assert book not in all_books, 'added book not deleted'
    assert deleted_book == {"deleted": book['id']},\
        'not returned deleted book id'
    assert (first_book and second_book) in all_books, 'added books not in list'
    assert len(all_books) >= 3, 'less than 3 books in the list'


@pytest.mark.TOFIX(reason='can not return {,},[,],(,),#,'' ')
@pytest.mark.parametrize('book_id', ['TeSt', u'тест', '*^&%$%',
                                     'a'*1000000])
def test_delete_nonexistent_book(book_id):
    """ Check 'delete book' method for nonexistent book id. """

    # Create three books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    # Delete nonexistent book:
    deleted_book = delete_book(book_id)

    assert deleted_book == {"deleted": book_id}, \
        'not returned deleted book id'

    # Get list of books:
    all_books = get_all_books()

    # TODO
    assert len(all_books) >= 3, 'less than 3 books in the list'

    # Make sure that deleted book no in list
    for book in all_books:
        assert book['id'] != book_id, 'deleted book id in list'


@pytest.mark.parametrize('title', ['', 'TeSt', u'тест', '*^&%$%#{}[]()',
                                   'a'*1000000])
@pytest.mark.parametrize('author', ['', 'Teodor Drayzer', u'Пушкин',
                                    '*^&%$%#{}[]()', '!'*1000000])
def test_full_cycle_of_the_book(title, author):
    """ Check full cycle of life of the book(create-update-delete). """

    # Create new book
    book = {'title': title, 'author': author}

    # Get new book
    new_book = add_book(book)

    # Update new book
    update_book(new_book['id'], {'title': author, 'author': title})

    # Delete new book
    delete_book(new_book['id'])

    # Get list of all books
    all_books = get_all_books()

    # Verify that book is not presented in the list:
    assert book not in all_books, 'added book not deleted'


def test_validate_cookie():
    """ Check auth cookie validation. """

    # Set name of host
    host_name = 'http://0.0.0.0:7000'
    # Set right message of invalid cookie
    right_message = {"message": "No valid auth cookie provided!"}

    url = '{0}/books'.format(host_name)
    result = get(url)
    message = result.json()
    assert message == right_message, 'wrong message of invalid cookie'

    url = '{0}/add_book'.format(host_name)
    result = post(url)
    message = result.json()
    assert message == right_message, 'wrong message of invalid cookie'

    url = '{0}/books/qwe'.format(host_name)
    result = get(url)
    message = result.json()
    assert message == right_message, 'wrong message of invalid cookie'

    url = '{0}/books/qwe'.format(host_name)
    result = delete(url)
    message = result.json()
    assert message == right_message, 'wrong message of invalid cookie'

    url = '{0}/books/qwe'.format(host_name)
    result = put(url)
    message = result.json()
    assert message == right_message, 'wrong message of invalid cookie'

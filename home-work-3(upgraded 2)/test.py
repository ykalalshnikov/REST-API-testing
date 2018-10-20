#!/usr/bin/python3
# -*- encoding=utf8 -*-

import requests
import pytest

from utils import add_book
from utils import get_all_books
from utils import get_book
from utils import update_book
from utils import delete_book
from utils import validate_uuid4
from utils import get_random_pairs
from utils import auth
from utils import get
from utils import put
from utils import post
from utils import delete
from utils import add_three_books


def test_login():
    """ This test checks that login REST API works fine. """

    # Log in with valid credentials:
    data = auth()

    # Verify that server returns some auth cookie:
    assert data['my_cookie'] > '', 'empty auth cookie'


def test_wrong_user():
    """ This test checks that login REST API works fine. """

    # Log in with invalid login:
    data = auth(user='qwe')

    # Verify that server returns unauthorized code 401:
    assert data == 401, 'status code is not 401'


def test_wrong_password():

    # Log in with invalid password:
    data = auth(password='qwe')

    # Verify that server returns unauthorized code 401:
    assert data == 401, 'status code is not 401'


def test_wrong_credentials():

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


def test_get_book_by_id():
    """ Check that 'get books' method returns correct list of books. """

    # Create three books, just to make sure books will be correctly
    # added to the list:
    add_three_books()
    book = add_book({'title': '1', 'author': 'Pushkin'})

    # Get second book id:
    getting_book = get_book(book['id'])

    # Get list of all books:
    all_books = get_all_books()

    # Make sure that
    assert getting_book == book, ''  # TODO error message
    assert len(all_books) >= 4, 'less than 3 books in the list'


def test_get_book_by_nonexistent_id():
    """ Check that 'get books' method returns correct list of books. """

    # Create three books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    # Get nonexistent book
    getting_book = get_book()

    # Get list of all books:
    all_books = get_all_books()

    # TODO comment
    assert getting_book == {}, 'nonexistent book is exist'
    assert len(all_books) >= 3, 'less than 3 books in the list'


def test_get_sorted_list_of_books():
    """ Check that 'get books' method returns correct list of books. """

    # Create Three books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    # Set sort filter:
    filters = {'sort': 'by_title'}

    # Get list of all books with filter:
    all_books = get_all_books(filters=filters)

    # TODO comment
    assert all_books == sorted(all_books, key=lambda x: x['title']), 'list of books not sorted'


@pytest.mark.parametrize('sort', ['test', u'тест', 2])
def test_get_invalid_sorted_list_of_books(sort):
    """ Check that 'get books' method returns correct list of books. """

    # Create three books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    # Set invalid sort filter:
    filters = {'sort': sort}

    # Get list of all books with filter:
    all_books = get_all_books(filters=filters)

    # TODO comment
    assert all_books != sorted(all_books, key=lambda x: x['title']), 'list of books sorted'


@pytest.mark.parametrize('limit', [1, 2, 3])
def test_get_limited_list_of_books(limit):
    """ Check that 'get books' method returns correct list of books. """

    # Create three books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    # Set limit filter:
    filters = {'limit': limit}

    # Get list of all books with filter:
    all_books = get_all_books(filters=filters)

    # TODO comment
    assert len(all_books) == limit, 'list of books not limited'


@pytest.mark.parametrize('limit', [0, -1, -2, -44])
def test_get_negative_limited_list_of_books(limit):
    """ Check that 'get books' method returns correct list of books. """

    # Create three books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    # Set negative limit filter:
    filters = {'limit': limit}

    # Get list of all books with filter:
    all_books = get_all_books(filters=filters)

    # TODO comment
    assert len(all_books) >= 3, 'less than 3 books in the list'


def test_get_invalid_limited_list_of_books():
    """ Check that 'get books' method returns correct list of books. """

    # Create three books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    # Set invalid limit filter:
    filters = {'limit': 'qwe'}

    # Get list of all books with filter:
    all_books = get_all_books(filters=filters)

    # TODO comment
    assert len(all_books) >= 3, 'less than 3 books in the list'


def test_get_sorted_and_limited_list_of_books():
    """ Check that 'get books' method returns correct list of books. """

    # Create two books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    # Set sort and limit filter:
    filters = {'sort': 'by_title', 'limit': 2}

    # Get list of all books with filter:
    all_books = get_all_books(filters=filters)

    # TODO comment
    assert all_books == sorted(all_books, key=lambda x: x['title']), 'list of books sorted'
    assert len(all_books) == 2, 'list of books not limited'


def test_similar_id_in_list():

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

    # TODO comment
    assert len(a) == len(all_books), 'similar id in list of books'


@pytest.mark.parametrize('title', ['', 'test', u'тест', '*^&%$%#{}[]()', 'a'*10])
@pytest.mark.parametrize('author', ['', 'Teodor Drayzer', u'Пушкин', '*^&%$%#{}[]()', '!'*10])
def test_add_new_book(title, author):
    """ Check 'create book' method with different values of
        Title and Author.
    """
    # Create new book
    book = {'title': title, 'author': author}

    # Get new book
    new_book = add_book(book)

    # Get list of all books
    all_books = get_all_books()

    # TODO comment
    assert new_book in all_books, 'new book not in list of the books'


def test_add_several_new_books():

    # Create three books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    # Get list of all books
    all_books = get_all_books()

    # TODO comment
    assert len(all_books) >= 3, 'less than 3 books in the list'


def test_add_book_with_empty_title():


    new_book = add_book({'author': 'Pushkin'})
    new_book['title'] = ''
    all_books = get_all_books()
    assert new_book in all_books, 'title of added book not empty'


def test_add_book_with_empty_author():

    new_book = add_book({'title': 'Qwerty'})
    new_book['author'] = 'No Name'
    print(new_book)
    all_books = get_all_books()
    print(all_books)
    assert new_book in all_books, 'author of added book no No Name'


def test_add_book_with_empty_data():

    new_book = add_book({})
    new_book['title'] = ''
    new_book['author'] = 'No Name'
    all_books = get_all_books()
    assert new_book in all_books, 'title or author of added book nor empty and No Name'


@pytest.mark.parametrize('title', ['', 'test', u'тест', '*^&%$%#', 'a'*10])
@pytest.mark.parametrize('author', ['', 'Teodor Drayzer', u'Пушкин', '#$%$^', '!'*10])
def test_update_book(title, author):
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


@pytest.mark.parametrize('title', ['test'])
@pytest.mark.parametrize('author', ['Teodor Drayzer'])
def test_update_nonexistent_book(title, author):

    # Create new book for update:
    add_book({'title': '', 'author': ''})
    book_id = 'qwe'

    # Update book attributes:
    result = update_book(book_id, {'title': title, 'author': author})

    # TODO comment
    assert result == {"message": "No book with given ID!"}, 'wrong message of invalid cookie'


def test_delete_book():
    # Create three books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    # Create new book for delete:
    book = add_book({'title': '1', 'author': '2'})

    # Delete new book:
    deleted_book = delete_book(book['id'])

    # Get list of all books
    all_books = get_all_books()

    # Verify that book is not presented in the list:
    assert book not in all_books, 'added book not deleted'
    assert deleted_book == {"deleted": book['id']}, 'not returned deleted book id'
    assert len(all_books) >= 3, 'less than 3 books in the list'


def test_delete_nonexistent_book():
    # Create three books, just to make sure books will be correctly
    # added to the list:
    add_three_books()

    # Get list of books:
    all_books = get_all_books()

    # TODO
    assert len(all_books) >= 3, 'less than 3 books in the list'


def test_validate_cookie():

    # Set name of host
    host = 'http://0.0.0.0:7000'
    # Set right message of invalid cookie
    right_message = {"message": "No valid auth cookie provided!"}

    url = '{0}/books'.format(host)
    result = get(url)
    message = result.json()
    assert message == right_message, 'wrong message of invalid cookie'

    url = '{0}/add_book'.format(host)
    result = post(url)
    message = result.json()
    assert message == right_message, 'wrong message of invalid cookie'

    url = '{0}/books/qwe'.format(host)
    result = get(url)
    message = result.json()
    assert message == right_message, 'wrong message of invalid cookie'

    url = '{0}/books/qwe'.format(host)
    result = delete(url)
    message = result.json()
    assert message == right_message, 'wrong message of invalid cookie'

    #TODO
    url = '{0}//books/qwe'.format(host)
    result = put(url)
    print(result)
    message = result.json()
    assert message == right_message, 'wrong message of invalid cookie'

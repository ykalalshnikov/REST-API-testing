import pytest
import requests
from requests.auth import HTTPBasicAuth


user = 'test_user'
wrong_user = 'user'
password = 'test_password'
wrong_password = 'password'
host = 'http://0.0.0.0:7000'


@pytest.fixture(scope='function')
def auth_cookie():
    """ This fixture allows to get auth cookie. """

    url = '{0}/login'.format(host)
    result = requests.get(url,
                          auth=HTTPBasicAuth(user, password))
    data = result.json()

    # Return auth_cookie to test:
    yield data['auth_cookie']


def add_book(auth_cookie, title=None, author=None):
    """
    This function add book
    """

    url = '{0}/add_book'.format(host)

    if (not title) and (not author):
        new_book = dict()
    elif title and author:
        new_book = dict(title=title, author=author)
    elif author and (not title):
        new_book = dict(author=author)
    else:
        new_book = dict(title=title)


    # Create new book:
    # Note: here we sending POST request with cookie and body!
    result = requests.post(url, params=new_book,
                           cookies={'my_cookie': auth_cookie})
    assert result.status_code == 200, 'status code is not 200'
    data = result.json()
    # Get id of created book:
    new_book['id'] = data['id']
    return new_book


def get_list_of_books(auth_cookie, sort=None, limit=None):
    """  This function return list of books with given params """

    if (not sort) and (not limit):
        filter_book = dict()
    elif sort and limit:
        filter_book = dict(sort=sort, limit=limit)
    elif limit and (not sort):
        filter_book = dict(limit=limit)
    else:
        filter_book = dict(sort=sort)
    url = 'http://0.0.0.0:7000/books'
    result = requests.get(url, params=filter_book, cookies={'my_cookie': auth_cookie})
    assert result.status_code == 200, 'status code is not 200'
    data = result.json()
    return data


def delete_all_books(auth_cookie):
    """ This function delete all books in list"""
    url = '{0}/delete_books'.format(host)
    result = requests.delete(url, cookies={'my_cookie': auth_cookie})
    assert result.status_code == 200, 'status code is not 200'


def test_login():
    """ This test checks that login REST API works fine. """

    url = '{0}/login'.format(host)

    # Send GET REST API request with basic auth:
    result = requests.get(url,
                          auth=HTTPBasicAuth(user, password))
    data = result.json()

    # Verify that server returns some auth cookie:
    assert result.status_code == 200, 'status code is not 200'
    assert data['auth_cookie'] > '', 'empty auth cookie'


def test_wrong_user():
    """ This test checks that login REST API works fine. """

    url = '{0}/login'.format(host)

    # Send GET REST API request with basic auth:
    result = requests.get(url,
                          auth=HTTPBasicAuth(wrong_user, password))
    assert result.status_code == 401, 'status code is not 401'


def test_wrong_password():
    """ This test checks that login REST API works fine. """

    url = '{0}/login'.format(host)

    # Send GET REST API request with basic auth:
    result = requests.get(url,
                          auth=HTTPBasicAuth(user, wrong_password))
    assert result.status_code == 401, 'status code is not 401'


def test_wrong_credentials():
    """ This test checks that login REST API works fine. """

    url = '{0}/login'.format(host)

    # Send GET REST API request with basic auth:
    result = requests.get(url,
                          auth=HTTPBasicAuth(wrong_user, wrong_password))
    assert result.status_code == 401, 'status code is not 401'


def test_list_of_books(auth_cookie):
    """ This test checks /books REST API function.  """

    add_book(auth_cookie, 'Bqwerty', 'Pushkin')
    add_book(auth_cookie, 'Aqwerty', 'Tolstoy')
    add_book(auth_cookie, '4Qwerty', 'Gorkiy')
    url = 'http://0.0.0.0:7000/books'
    result = requests.get(url, cookies={'my_cookie': auth_cookie})
    data = result.json()
    assert result.status_code == 200, 'status code is not 200'
    assert type(data) == list, 'type of list of books is not list'
    assert data != [], 'list of books is empty'


def test_list_book_by_id(auth_cookie):
    """ This test checks /books REST API function.  """

    delete_all_books(auth_cookie)
    first_book = add_book(auth_cookie, 'Bqwerty', 'Pushkin')
    second_book = add_book(auth_cookie, 'Aqwerty', 'Tolstoy')
    third_book = add_book(auth_cookie, '4Qwerty', 'Gorkiy')

    url = '{0}/books/{1}'.format(host, second_book['id'])
    result = requests.get(url, cookies={'my_cookie': auth_cookie})
    assert result.status_code == 200, 'status code is not 200'
    data = result.json()

    list_of_all_books = get_list_of_books(auth_cookie)
    assert data == second_book, 'list of book by id not equals required book'
    assert first_book, third_book in list_of_all_books


def test_list_book_by_nonexistent_id(auth_cookie):

    delete_all_books(auth_cookie)
    add_book(auth_cookie, 'Bqwerty', 'Pushkin')

    url = '{0}/books/{1}'.format(host, 'dfg')
    result = requests.get(url, cookies={'my_cookie': auth_cookie})
    data = result.json()
    assert result.status_code == 200, 'status code is not 200'
    assert data == {}, 'any books in data'


def test_sort_list_of_books(auth_cookie):

    delete_all_books(auth_cookie)
    add_book(auth_cookie, title='Bqwerty')
    add_book(auth_cookie, title='Aqwerty')
    add_book(auth_cookie, title='4Qwerty')
    data = get_list_of_books(auth_cookie, sort='by_title')

    first_book = data[0]
    second_book = data[1]
    third_book = data[2]
    assert first_book['title'] == '4Qwerty', 'first book has not required order'
    assert second_book['title'] == 'Aqwerty', 'second book has not required order'
    assert third_book['title'] == 'Bqwerty', 'third book has not required order'


def test_limit_of_books(auth_cookie):

    delete_all_books(auth_cookie)
    add_book(auth_cookie, title='Bqwerty')
    add_book(auth_cookie, title='Aqwerty')
    add_book(auth_cookie, title='4Qwerty')
    data = get_list_of_books(auth_cookie, limit=1)
    assert len(data) == 1, 'not one book in list'
    data = get_list_of_books(auth_cookie, limit=2)
    assert len(data) == 2, 'not two book in list'
    data = get_list_of_books(auth_cookie, limit=4)
    assert len(data) == 3, 'not three book in list'


def test_sort_and_limit_list_of_books(auth_cookie):


    delete_all_books(auth_cookie)
    add_book(auth_cookie, title='Bqwerty')
    add_book(auth_cookie, title='Aqwerty')
    add_book(auth_cookie, title='4Qwerty')
    data = get_list_of_books(auth_cookie, sort='by_title', limit=2)
    first_book = data[0]
    second_book = data[1]
    assert (len(data) == 2 and first_book['title'] == '4Qwerty' and second_book['title'] == 'Aqwerty')
    'no order or wronq quintity in list of boos'


def test_similar_id_in_list(auth_cookie):


    delete_all_books(auth_cookie)
    add_book(auth_cookie, title='Bqwerty')
    add_book(auth_cookie, title='Aqwerty')
    add_book(auth_cookie, title='4Qwerty')
    data = get_list_of_books(auth_cookie)
    a = []
    for i in data:
        if (i['id']) not in a:
            a.append(i['id'])
    assert len(a) == 3, 'similar id in list of books'


def test_add_book(auth_cookie):

    delete_all_books(auth_cookie)
    new_book = add_book(auth_cookie, 'Abcd', 'Petr Ivanov')
    all_books = get_list_of_books(auth_cookie)

    assert new_book in all_books, 'added book not in list of books'


def test_add_several_books(auth_cookie):


    delete_all_books(auth_cookie)
    first_book = add_book(auth_cookie, 'Bqwerty', 'Pushkin')
    second_book = add_book(auth_cookie, 'Aqwerty', 'Tolstoy')
    third_book = add_book(auth_cookie, '4Qwerty', 'Gorkiy')
    all_added_books = [first_book, second_book, third_book]
    all_books = get_list_of_books(auth_cookie)

    assert len(all_books) == 3, 'not three books in list'
    assert all_added_books == all_books, 'not all added books in list'


def test_add_book_with_empty_title(auth_cookie):

    delete_all_books(auth_cookie)
    new_book = add_book(auth_cookie, author='Pushkin')
    new_book['title'] = ''
    all_books = get_list_of_books(auth_cookie)
    assert new_book in all_books, 'title of added book not empty'


def test_add_book_with_empty_author(auth_cookie):

    delete_all_books(auth_cookie)
    new_book = add_book(auth_cookie, title='Pushkin')
    new_book['author'] = 'No Name'
    all_books = get_list_of_books(auth_cookie)
    assert new_book in all_books, 'author of added book no No Name'


def test_add_book_with_empty_data(auth_cookie):

    delete_all_books(auth_cookie)
    new_book = add_book(auth_cookie)
    new_book['title'] = ''
    new_book['author'] = 'No Name'
    all_books = get_list_of_books(auth_cookie)
    assert new_book in all_books, 'title or author of added book nor empty and No Name'


def test_delete_book(auth_cookie):


    delete_all_books(auth_cookie)
    first_book = add_book(auth_cookie, 'Bqwerty', 'Pushkin')
    second_book = add_book(auth_cookie, 'Aqwerty', 'Tolstoy')
    third_book = add_book(auth_cookie, '4Qwerty', 'Gorkiy')

    # Delete book (Note: DELETE REST API request with cookie!):
    url = '{0}/books/{1}'.format(host, second_book['id'])
    result = requests.delete(url,
                             cookies={'my_cookie': auth_cookie})
    assert result.status_code == 200, 'status code is not 200'
    # Get list of books:

    list_of_all_books = get_list_of_books(auth_cookie)

    # Verify that book is not presented in the list:
    assert second_book not in list_of_all_books, 'added book not deleted'
    assert (first_book, third_book in list_of_all_books), 'no none deleted books in list of books'


def test_delete_nonexistent_book(auth_cookie):


    delete_all_books(auth_cookie)
    first_book = add_book(auth_cookie, 'Bqwerty', 'Pushkin')
    second_book = add_book(auth_cookie, 'Aqwerty', 'Tolstoy')
    third_book = add_book(auth_cookie, '4Qwerty', 'Gorkiy')
    all_added_books = [first_book, second_book, third_book]


    # Delete book (Note: DELETE REST API request with cookie!):
    url = '{0}/books/{1}'.format(host, 'qwe')
    result = requests.delete(url,
                             cookies={'my_cookie': auth_cookie})
    assert result.status_code == 200, 'status code is not 200'
    # Get list of books:

    list_of_all_books = get_list_of_books(auth_cookie)
    # Verify that book is not presented in the list:
    assert all_added_books == list_of_all_books, 'added books in list after deleting by nonexisting id'


def test_delete_all_books(auth_cookie):


    add_book(auth_cookie, 'Bqwerty', 'Pushkin')
    add_book(auth_cookie, 'Aqwerty', 'Tolstoy')
    add_book(auth_cookie, '4Qwerty', 'Gorkiy')

    delete_all_books(auth_cookie)

    # Get list of books:
    list_of_all_books = get_list_of_books(auth_cookie)

    # Verify that book is not presented in the list:
    assert list_of_all_books == [], 'added books not deleted'


def test_validate_cookie():

    url = '{0}/books'.format(host)
    result = requests.get(url)
    data = result.json()
    assert data == {'data': 'invalid cookie'}, 'wrong data fo invalid cookie'

    url = '{0}/add_book'.format(host)
    result = requests.post(url)
    data = result.json()
    assert data == {'data': 'invalid cookie'}, 'wrong data fo invalid cookie'

    url = '{0}/books/<book_id>'.format(host)
    result = requests.get(url)
    data = result.json()
    assert data == {'data': 'invalid cookie'}, 'wrong data fo invalid cookie'

    url = '{0}/books/<book_id>'.format(host)
    result = requests.delete(url)
    data = result.json()
    assert data == {'data': 'invalid cookie'}, 'wrong data fo invalid cookie'

    url = '{0}/delete_books'.format(host)
    result = requests.delete(url)
    data = result.json()
    assert data == {'data': 'invalid cookie'}, 'wrong data fo invalid cookie'

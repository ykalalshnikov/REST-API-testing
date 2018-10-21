#!/usr/bin/python3
# -*- encoding=utf8 -*-

from uuid import uuid4
import flask
from flask import Flask
from flask import request
from flask_basicauth import BasicAuth
from flask import jsonify


app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'test_user'
app.config['BASIC_AUTH_PASSWORD'] = 'test_password'
basic_auth = BasicAuth(app)

BOOKS = []
SESSIONS = []


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def verify_cookie(req):
    """ This function verifies cookie. """

    cookie = req.cookies.get('my_cookie', '')

    return cookie in SESSIONS


@app.route('/login', methods=['GET'])
@basic_auth.required
def get_auth():
    """ This function verifies user and password and creates
        new cookie if user and password are correct.
    """

    cookie = str(uuid4())
    SESSIONS.append(cookie)

    return flask.jsonify({'auth_cookie': cookie})


@app.route('/books', methods=['GET'])
def get_list_of_books():
    """ This function returns the list of books. """

    global BOOKS

    if verify_cookie(request):

        sort_filter = request.args.get('sort', '')
        list_limit = (request.args.get('limit', -1))

        result = BOOKS

        if sort_filter == 'by_title':
            result = sorted(result, key=lambda x: x['title'])

        try:
            list_limit = int(list_limit)
            if list_limit > 0:
                result = result[:list_limit]

        except ValueError:
            pass

        return flask.jsonify(result)

    raise InvalidUsage('No valid auth cookie provided!')


@app.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    """ This function returns one book from the list. """

    if verify_cookie(request):
        result = {}

        for book in BOOKS:
            if book['id'] == book_id:
                result = book

        return flask.jsonify(result)

    raise InvalidUsage('No valid auth cookie provided!')


@app.route('/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    """ This function updates information about some book. """

    if verify_cookie(request):

        for i, book in enumerate(BOOKS):
            # Find the book with this ID:
            if book['id'] == book_id:
                book['title'] = request.values.get('title', book['title'])
                book['author'] = request.values.get('author', book['author'])

                # Update information about this book:
                BOOKS[i] = book

                return flask.jsonify(book)
        else:
            raise InvalidUsage('No book with given ID!', status_code=404)

    raise InvalidUsage('No valid auth cookie provided!')


@app.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    """ This function deletes book from the list. """

    global BOOKS

    if verify_cookie(request):
        # Create new list of book and skip one book
        # with specified id:
        new_books = [b for b in BOOKS if b['id'] != book_id]
        BOOKS = new_books

        return flask.jsonify({'deleted': book_id})

    raise InvalidUsage('No valid auth cookie provided!')


@app.route('/add_book', methods=['POST'])
def add_book():
    """ This function adds new book to the list. """

    global BOOKS

    if verify_cookie(request):
        book_id = str(uuid4())
        title = request.values.get('title', '')
        author = request.values.get('author', 'No Name')

        new_book = {'id': book_id, 'title': title, 'author': author}

        # add new book to the list:
        BOOKS.append(new_book)

        return flask.jsonify(new_book)

    raise InvalidUsage('No valid auth cookie provided!')


if __name__ == "__main__":
    app.run('0.0.0.0', port=7000)
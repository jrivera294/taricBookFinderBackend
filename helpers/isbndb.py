import requests
from django.conf import settings
from math import floor

api = settings.ISBN_API_KEY


def isbndb_ids_to_titles(id):
    """ Receives an ISBNdb ID, replaces the underscores with
    spaces and capitalize all words, and return the resulting string
    """

    string = id.replace('_', ' ')

    return string.title()


def isbndb_ids_to_capitalized_string(id):
    """ Receives an ISBNdb ID, replaces the underscores with
    spaces and capitalize the first word, and return the resulting string
    """

    string = id.replace('_', ' ')

    return string.capitalize()


def isbndb_request(url):
    """ Makes a request to ISBNdb API

    :param url: URL Request
    :return:    ISBNdb response
    """
    response = requests.get(url)

    # Check if request fails
    if response.status_code != 200:
        raise Exception('Error trying to request ISBNdb API', 500)

    json_response = response.json()

    # Check if request body contains errors
    if 'error' in json_response:
        if 'Unable to locate' in json_response['error']:
            status = 404
        else:
            status = 500

        raise Exception(json_response['error'], status)

    return json_response


def find_book(code):
    """ Find a book by ISBN, ISBNdb id or book id.

    :param      code: ISBN 10 or 13
    :return:    JSON with book information
    """
    url = 'http://isbndb.com/api/v2/json/' + api + '/book/' + code

    json_response = isbndb_request(url)

    book_data = json_response['data']

    # Transform Authors IDs to Strings
    """authors = []
    for author in book_data[0]['author_data']:
        authors.append(author['name'])"""

    # Transform Subject IDs to Strings
    subjects = []
    for subject in book_data[0]['subject_ids']:
        subjects.append(isbndb_ids_to_titles(subject))

    return {
        'title':        book_data[0]['title'],
        'title_long':   book_data[0]['title_long'],
        'author_data':  book_data[0]['author_data'],
        'subjects':     subjects,
        'publisher_name': book_data[0]['publisher_name'],
        'physical_description_text': book_data[0]['physical_description_text'],
        'summary':      book_data[0]['summary'],
        'edition_info': book_data[0]['edition_info'],
        'isbn10':       book_data[0]['isbn10'],
        'isbn13':       book_data[0]['isbn13']
    }


def find_books(string, index, page=0):
    """ Find books. Used to search by title, author or publisher

    :param string:  Search string
    :param index:   Index to search
    :param page:    Page number for pagination (optional)
    :return:        JSON with books, page_count, result_count and current_page
    """

    # Generate url
    if index == 'title':
        url = 'http://isbndb.com/api/v2/json/' + api \
              + '/books?q=' + string
    elif index == 'author':
        url = 'http://isbndb.com/api/v2/json/' + api \
              + '/books?q=' + string + '&i=author_name'
    elif index == 'publisher':
        url = 'http://isbndb.com/api/v2/json/' + api \
              + '/books?q=' + string + '&i=publisher_name'
    else:
        raise Exception('Invalid search index', 400)

    if page:
        url += '&p=' + page

    # Make query to ISBNdb
    json_response = isbndb_request(url)

    # Transform all the data from ISBNdb to Book class array
    books = []
    for book in json_response['data']:
        """authors = []
        for author in book['author_data']:
            authors.append(author['name'])"""

        subjects = []
        for subject in book['subject_ids']:
            subjects.append(isbndb_ids_to_titles(subject))

        books.append({
            'title':        book['title'],
            'title_long':   book['title_long'],
            'author_data':  book['author_data'],
            'subjects':     subjects,
            'publisher_name': book['publisher_name'],
            'physical_description_text': book['physical_description_text'],
            'summary':      book['summary'],
            'edition_info': book['edition_info'],
            'isbn10':       book['isbn10'],
            'isbn13':       book['isbn13']
        })

    return {
        'books':        books,
        "page_count":   json_response['page_count'],
        "result_count": json_response['result_count'],
        "current_page": json_response['current_page']
    }


def find_book_by_subject(string):
    """ Find books by subject.

    :param string:  Search string
    :return:        Books count, and books (id + title obtained from the ID)
    """
    url = 'http://isbndb.com/api/v2/json/' + api + '/subject/' + string.lower()

    json_response = isbndb_request(url)

    books = []
    for book in json_response['data'][0]['book_ids']:

        books.append({
            'id':     book,
            'title':  isbndb_ids_to_titles(book)
        })

    return {
        'books_count':  json_response['data'][0]['books_count'],
        'page_count':   floor(int(json_response['data'][0]['books_count'])/10),
        'books':        books
    }


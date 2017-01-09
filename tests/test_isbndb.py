from django.test import TestCase
from helpers.isbndb import *
from django.conf import settings


class ISBNDBTestCase(TestCase):

    def test_isbndb_request(self):
        """ isbndb_request make requests and raises the right errors  """
        api_key = settings.ISBN_API_KEY

        # Check that return the right response
        request = isbndb_request('http://isbndb.com/api/v2/json/' + api_key +
                           '/books?q=science&opt=keystats')
        self.assertEqual(request['keystats']['key_id'], api_key,
                         'isbndb_request should return keystats')

        # Check that raises the right errors
        with self.assertRaises(Exception) as inst:
            isbndb_request('http://isbndb.com/api/v2/json/bad_key/'
                           'books?q=science&opt=keystats')

        error, status = inst.exception.args
        self.assertEqual(error, 'Invalid api key: bad_key',
                         'isbndb_request should return invalid key error')
        self.assertEqual(status, 500,
                         'isbndb_request should return status 500 when invalid key error')

        with self.assertRaises(Exception) as inst:
            isbndb_request('http://isbndb.com/api/v2/json/' + api_key +
                           '/book/asdfg/')

        error, status = inst.exception.args
        self.assertEqual(error, 'Unable to locate asdfg',
                         'isbndb_request should return unable to locate')
        self.assertEqual(status, 404,
                         'isbndb_request should return status 404 when unable to locate')

    def test_find_book(self):
        book = find_book('9780201616415')

        self.assertEqual(book['title'], 'Extreme programming explained',
                         'Should return the right book')

        self.assertTrue('Computer Software Development' in book['subjects'],
                        'Should transform the subject ids in capitalized strings')

    def test_find_book_by_subject(self):
        result = find_book_by_subject('disease')

        # Query by "disease" should return books
        self.assertGreater(int(result['books_count']), 0,
                           'Should return books')

    def test_find_books(self):
        # Query for "informatica" books using the "title" index should return books
        result = find_books('informatica', 'title')
        self.assertGreater(int(result['result_count']), 0,
                           'Should return books with informatica in title')

        # Query for "informatica" books using the "title" index and page 3
        # should return books from the page 3
        result = find_books('informatica', 'title', '3')
        self.assertGreater(int(result['result_count']), 0,
                           'Should return books with informatica in title')
        self.assertEqual(int(result['current_page']), 3,
                         'Should return current page 3')

        # Query for "santillana" books using the "publisher" index should return books
        result = find_books('santillana', 'publisher')
        self.assertGreater(int(result['result_count']), 0,
                           'Should return books with santillana as publisher')

        # Query for "juan" books using the "author" index should return books
        result = find_books('juan', 'author')
        self.assertGreater(int(result['result_count']), 0,
                           'Should return books with juan as author')

        # Query for invalid index should raise error
        with self.assertRaises(Exception) as inst:
            find_books('', 'invalid_index')

        error, status = inst.exception.args
        self.assertEqual(error, 'Invalid search index',
                         'Should return invalid index')
        self.assertEqual(status, 400,
                         'Should return status 400 when invalid index')

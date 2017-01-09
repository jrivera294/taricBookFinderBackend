from helpers.isbndb import *
from django.http import JsonResponse


def book(request, code):
    """ Book search view. Can find books by ISBN codes or ISBNdb ID.

    :param request:
    :param code:    Book code. Can be ISBN10, ISBN13 or ISBNdb ID
    :return:        JsonResponse
    """

    # Find books
    try:
        book_json = find_book(code)
    except Exception as inst:
        if len(inst.args) != 2:
            raise inst

        error, status = inst.args
        return JsonResponse({'message': error}, status=status)

    return JsonResponse(book_json)


def books(request):
    """ Books search view. Can find books by title, author, publisher or subject

    query_params: q, index and page.

    :param request:
    :return:        JsonResponse
    """
    query_params = request.GET

    # Check that query params are present
    if 'index' not in query_params:
        return JsonResponse({
            'message': 'Index must be in query params'
        }, status=400)

    if 'q' not in query_params:
        return JsonResponse({
            'message': 'Query string (q) must be in query params'
        }, status=400)

    # Find books
    try:
        if query_params['index'] == 'subject':
            response = find_book_by_subject(query_params['q'])
        else:
            if 'page' in query_params:
                response = find_books(
                    query_params['q'],
                    query_params['index'],
                    query_params['page']
                )
            else:
                response = find_books(
                    query_params['q'],
                    query_params['index']
                )
    except Exception as inst:
        if len(inst.args) != 2:
            raise inst

        error, status = inst.args
        return JsonResponse({'message': error}, status=status)

    return JsonResponse(response)

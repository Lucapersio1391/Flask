from flask import jsonify, request, render_template, abort
from flask_paginate import Pagination, get_page_args
import functools


def pagination_json(f):
    """
    Decorator that handle the JSON (output) pagination.
    The wrapper function takes page_size and page_num.
    (respectively the number of items the user wants per page and the number of the page he/she wants to be returned)
    as well as all the parameterss of the function wrapped. 
    First of all we need to obtain 2 variables from the wrapped function:
    1) the output itself, which is a list
    2) the length of the output
    Then we have to handle 2 exceptions:
    1) if the page size is out of validity range (1-1000)
    2) if the page number does not exist. 
       In this case we have to distinguish between 2 scenarios:
            1) if the remainder of the operation --> length of result / number of nodes per page
               is equal to 0 it means that all the pages has the same items
            2) if the above operation gives a remainder different from zero it means that the last page
               has less items than those before. We have to add a page to the allowed range
    Finally we create the variable start (represent the starting point of each page retrieved) that
    will be used for supporting pagination. The result displayed is a list of dictionaries, 
    where each dictionary represents the node. 
    In this nested structure (dict) we have at the highest level a pair of key (results) - value (list of dicts)
    We want to return a JSON object so we create a proper response using the jsonify function of flask library 
    """
    @functools.wraps(f)
    def wrapper(page_size, page_num, *args, **kwargs):
        results = f(*args, **kwargs)
        count = len(f(*args, **kwargs))
        if page_size not in range(1,1001):
            abort(400, 'Invalid page size requested!')
        if page_num not in range((count//page_size) if count % page_size == 0 else ((count//page_size) + 1)):
             abort(400, 'Invalid page number requested!')
        start = page_num * page_size
        obj = {}
        obj['results'] = results[start:start + page_size]
        return jsonify(obj)      
    return wrapper

def pagination_html(f):
    """
    This decorator is out of the scope of this test, but it can be used instead of the above decorator,
    if we want to return a HTML page and not a JSON
    """
    @functools.wraps(f)
    def wrapper(page_size, page_num, *args, **kwargs):
        page, per_page, offset = get_page_args()
        per_page = page_size
        page = page_num + 1
        results = f(*args, **kwargs)
        offset = (page - 1) * per_page
        pagination_results = results[offset: offset + per_page]
        total = len(f(*args, **kwargs))
        pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
            
        return render_template('pagination.html',
                        results=pagination_results,
                        page=page,
                        per_page=per_page,
                        pagination=pagination
                        )       
    return wrapper

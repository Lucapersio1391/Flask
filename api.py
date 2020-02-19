from flask import Flask, abort, render_template, request, jsonify
from config import Database
from decorator import pagination_html, pagination_json

app = Flask(__name__)

# Initialize object
db = Database()

@app.route('/')
def home():
    """
    This is the landing page of the API.
    """
    return render_template('index.html')


@app.route('/<int:idNode>/', defaults={'language': '','page_size': 100, 'page_num': 0})
@app.route('/<int:idNode>/<language>/' , defaults={'page_size': 100, 'page_num': 0})
@app.route('/<int:idNode>/<language>/<int:page_size>/', defaults={'page_num': 0})
@app.route('/<int:idNode>/<language>/<int:page_size>/<int:page_num>/')
@pagination_json
def extract_nodes(idNode, language):
    """
    There are 4 decorators that handles the routing. They include all the parameters but the search_keyword,
    which is handled with a query string within the view. 
    From the highest to the lowest level we have all the parameters that can be inserted to filter the data.
    The view that handles the requests takes idNode and language as parameters (required).
    First of all we need to extract all the ids and the languages that can be found in the tables in order 
    to throw 404 pages if there are invalid values inserted or missing parameters.
    Error cases:
    1) if id does not exist in the db
    2) if the language is not inserted in the URL
    3) if we insert an invalid language (does not exists in the db)
       Particularly for this case I've inserted a variable (output) that varies according to the
       number of languages in the db.
    For the final result we use 2 intermediate outputs:
    1) children list: list of children ids for the node and language
    2) search keyword: search term inserted in the URL (default empty string)
    The result will be then paginated thanks to the decorator @paginate_json
    """
    extract_lang = db.languages_available()
    extract_ids = db.id_node_in_table()
    ids = [single_id['idNode'] for single_id in extract_ids]
    languages = [single_lan['language'] for single_lan in extract_lang]

    if idNode not in ids:
        abort(404,'The id you are looking for does not exist!')
    elif not language:
        abort(404,'There is a missing required parameter! Please insert also a language.') 
    elif language not in languages:
        l = len(languages) - 1
        output = "".join(" or {}".format(v) if i == l else " {}".format(v) for i, v in enumerate(languages))
        abort(404,'Invalid language! You can insert only {}'.format(output))

    children_list = db.extract_children_list(idNode, language)
    search_keyword = request.args.get('search_keyword', '')
    results = db.extract_results(children_list, search_keyword)
    return results

if __name__ == "__main__":
    app.run(debug=True)
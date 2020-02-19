API DESCRIPTION

1) DB settings

Open the file settings.ini, which is in the settings folder, and insert your DB settings (HOST, USER, PASSWORD and DB_NAME)

3) API

From the command line launch the API with: python api.py. 
When the server is on you'll be able to go the landing page of the app using a browser.
If you want to test the API using Postman APP you can download it at https://www.getpostman.com/downloads/

4) How the API works

There are 2 required parameters for this API:

- idNode: it's the unique id for each node;
- language: it can be english or italian.

In order for the server not to throw an error you have to insert both of these parameters as shown in the following example:
http://127.0.0.1:5000/5/english

where:
- http://127.0.0.1:5000 is the landing page URL;
- 5 is the idNode we are looking for;
- english is the language we want.

Note that URL, idNode and language must be separated by a slash (/).

The API accepts other 3 optional parameters:

- page_size: the number of nodes that you want to be displayed per page (the default value is 100);
- page_num: the page you want to retrieve (the default value is 0);
- search_keyword: search term with which you can filter results (the default value is an empty string).

Example:
http://127.0.0.1:5000/5/english/1/1/?search_keyword=m

where:
- 1 is the page size;
- 1 is the page number you get (it is the second page as it's 0-base indexed);
- ?search_keyword=m is the query string through which we can filter all the results that starts with the letter m.

Cases in which you get an error using these optional parameters:
- if you insert a page size out of the range validity (1000 is the max value);
- if you insert a page number that does not exist.

Note that search_keyword parameter is dependent upon the others. 
If we want to use it, we have to insert it at the end of the URL.

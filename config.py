import pymysql
import configparser
from os import path

class Database:
    """
    Database class will handle both connection with DB (using pymysql library) and data retrieval
    """
    def __init__(self):
        """
        We initialize the object with 3 attibutes:
        1) DB connection: using the PropertyParser class we extract settings from settings.ini file
        2) Cursor: used to execute query strings we pass. It is a DictCursor object that return a dict as result
        3) Join: This attribute will be used twice, so it is better to write it just once
        """
        propertyParser = PropertyParser()
        settings = propertyParser.get_properties_by_section('DB')
        self.con = pymysql.connect(host=settings['HOST'], user=settings['USER'],
                                password=settings['PASSWORD'], db=settings['DB_NAME'], cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()
        self.join = """
                        FROM node_tree node join
                        node_tree parent
                        on node.iLeft >= parent.iLeft and node.iRight 
                        <= parent.iRight
                        join node_tree_names
                        on parent.idNode = node_tree_names.idNode
                        """


    def languages_available(self):
        """
        Extract all possible languages from node_tree_names table
        :param: 
        :return: list of dicts with english or italian as values and language as key
        """
        query = """
        SELECT distinct language
        from node_tree_names
        """
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def id_node_in_table(self):
        """
        Extract all ids from node_tree table
        :param: 
        :return: list of dicts with id as values and idNode as key
        """
        query = """
        SELECT idNode
        from node_tree
        """
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def extract_children_list(self, id_node, language):
        """
        Given an id and a language as inputs, extract all the children of that node 
        (include the node itself).
        In this function we initialize 2 further attributes (self.id_node and self.language) 
        that will be used in the below function extract_results
        :param: id_node
                language        
        :return: children_list
        """
        query = """
        SELECT GROUP_CONCAT(node.idNode order by node.level) as children
        {}
        group by parent.idNode, 
        node_tree_names.language
        having parent.idNode = {} and node_tree_names.language = "{}"
        """.format(self.join, id_node, language)
        self.id_node, self.language = id_node, language
        self.cur.execute(query)
        children_list = self.cur.fetchall()
        return children_list


    def extract_results(self, children_list, search_keyword):
        """
        It takes as parameters the children list (output of the above function) and the search keyword.
        It returns the result of the query.
        The variable nodi is a list obtained from the output of the previous function.
        The variable children_list_fixed_for_in is ready to be inserted in the query.
        As we don't need in the output all the variables required for the calculation of the query,
        the keys language and iLeft are deleted.
        :param: children_list
                search_keyword: string to be passed for further filtering results     
        :return: results
        """
        children_list = self.extract_children_list(self.id_node, self.language)
        nodi = children_list[0]['children'].split(',')
        children_list_fixed_for_in = '(' + ','.join(elem for elem in nodi) + ')'
        query = """
        select 
        parent.idNode idNode, 
        node_tree_names.nodeName nodeName, 
        node_tree_names.language language, 
        parent.iLeft iLeft,
        count(parent.idNode) - 1 as count_children
        {}
        group by nodeName, idNode,language, iLeft
        having parent.idNode IN {} and node_tree_names.language = "{}" 
        and node_tree_names.nodeName LIKE "{}"
        order by iLeft
        """.format(self.join, children_list_fixed_for_in, self.language , search_keyword + "%")
        self.cur.execute(query)
        results = self.cur.fetchall()
        for result in results:
          del result['language']
          del result['iLeft']
        return results

class PropertyParser:
    """
    This class will be used to read the settings from settings.ini file and return the section as a dict
    """
    def __init__(self):
        """
        We initialize it with the path we are working into and with the configurations set
        """
        self.config = None
        this_dir = path.dirname(path.abspath(__file__))
        settings_file = path.join(this_dir, 'settings/settings.ini')
        self.set_config(settings_file)


    def get_properties_by_section(self, section):
        """
        This function takes as input the section and return a dict with all the items of that section
        :param: section to be parsed      
        :return: dict with properties
        """
        return dict(self.config.items(section))

    def set_config(self, prop_filename):
        """
        We used configparser function to be able to read and parse the settings.ini file
        :param: path to filename     
        :return: 
        """
        config = configparser.RawConfigParser(allow_no_value=True)
        config.optionxform = str
        with open(prop_filename, 'r', encoding='utf-8') as prop_file:
            config.read_file(prop_file)
        self.config = config

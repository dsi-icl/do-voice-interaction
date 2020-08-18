from .utils_graphql import GraphQL
from .utils import demo_contains_word, find_string_in_other_string

def search_demo_by_tag(graphql,tag):
    "Function that returns demos names corresponding to a tag"

    result = graphql.search_by_tag(tag.lower())

    if result['current']==None:
        return None
    elif len(result['current']['projects']) > 0:
        list_names = []
        for name in result['current']['projects']:
            list_names.append(name['name'])
        return list_names
    else:
        return []

def search_demo_by_word(graphql,name):
    "Function that filters projects by key word"
    available_demos = GraphQL.get_projects(graphql.config['url'])
    if available_demos!=None and len(available_demos)>0:
        result_search = demo_contains_word(name,available_demos.values())
        if result_search[0]:
            return result_search[1]

    return []

def search_process_tag(graphql,tag):
    "Function that is used in search action process to search by key tag"

    search_result = search_demo_by_tag(graphql,tag)
    if search_result == None:
        result = {'success':False,'message':"I can't access to any demo"}
    elif len(search_result) == 0:
        result = {'message':"I'm sorry, there is no demo on this topic"}
    elif len(search_result) > 10:
        result = {'message':'The list of demos is too long to read out. Would you like to refine it by other tags?'}
    else:
        result = {'message':'Here are the results for {}'.format(tag)+' : '+', '.join(search_result)}
    return result

def search_process_name(graphql,name):
    "Function that is used in search action process to search by key word"

    search_result = search_demo_by_word(graphql,name)
    if len(search_result) == 0:
        result = {'message':"I'm sorry, there is no demo on this topic"}
    elif len(search_result) > 10:
        result = {'message':'The list of demos is too long to read out. Would you like to refine it by other names?'}
    else:
        result = {'message':'Here are the results for {}'.format(name)+' : '+', '.join(search_result)}
    return result

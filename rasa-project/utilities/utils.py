from .utils_graphql import GraphQL

def search_demo_by_tag(graphql,tag):
    "Function that returns demos names corresponding to a tag"

    result = graphql.search_by_tag(tag)

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
    available_demos = GraphQL.get_projects()
    if available_demos!=None and len(available_demos)>0:
        result_search = demo_contains_word(name.lower(),available_demos.values())
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

def search_prosess_name(graphql,name):
    "Function that is used in search action process to search by key word"

    search_result = search_demo_by_word(graphql,name)
    if len(search_result) == 0:
        result = {'message':"I'm sorry, there is no demo on this topic"}
    elif len(search_result) > 10:
        result = {'message':'The list of demos is too long to read out. Would you like to refine it by other names?'}
    else:
        result = {'message':'Here are the results for {}'.format(name)+' : '+', '.join(search_result)}
    return result

def demo_contains_word(word, available_demos):
    """Function that indicates if one of the demo contains a word and returns all demos containing the tag

    Parameters:
    word (String): The word
    available_demos (List[String]): The list of available demos in the current environments

    Returns:
    [Boolean, List[String]]: The boolean and the list of found demos"""

    word_found = False
    list_chosen_demos = []
    for demo_name in available_demos:
        if word.lower() in demo_name.lower():
            list_chosen_demos.append(demo_name)
            if not word_found:
                word_found = True

    return word_found,list_chosen_demos


def find_string_in_other_string(input_name,available_demos):
    "Function that checks if each word of a string is contained in an other string"

    words = input_name.split()

    demo_found = False

    count = 0

    while not demo_found and count < len(available_demos):
        demo_name = available_demos[count]
        demo_found = True
        ind = 0

        while demo_found and ind<len(words):
            demo_found = words[ind] in demo_name
            ind += 1

        if demo_found:
            name = demo_name

        ind = 0
        count += 1

    if demo_found:
        return name

    return None

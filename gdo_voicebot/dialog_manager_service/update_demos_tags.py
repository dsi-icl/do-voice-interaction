import fileinput
import functools

from utilities.utils_graphql import GraphQL
from utilities.utils import prepare_lines


def write_entities(config_path,entity_name):
    "Function that updates and writesdemo oor tag entities in nlu file"
    try:
        file = None
        #we retrieve the list of available demos
        my_graphQL = GraphQL(config_path)

        #we open the nlu.md file in read mode to retrieve all the lines of the file
        file = open("./data/nlu.md","r")
        lines = file.readlines()

        if entity_name=='demo':
            #clear the lru_cache
            GraphQL.get_projects.cache_clear()
            available_demos = list(GraphQL.get_projects(my_graphQL.config['url']).values())
            lines = prepare_lines(lines,'intent:open','intent:out_of_scope',available_demos,'- Open ',entity_name)
        else:
            #clear the lru_cache
            GraphQL.get_tags.cache_clear()
            tags = GraphQL.get_tags(my_graphQL.config['url'])
            lines = prepare_lines(lines,'intent:search','intent:shutdown',tags,'- Look for ',entity_name)


        #we now open the file in write mode
        file = open("./data/nlu.md","w")
        #we update the file with the new lines
        file.writelines(lines)
        file.close()

    except Exception as e:
        print("Exception : ",str(e))
        if file!=None and not file.closed():
            file.close()

write_entities('./config/config.yml','demo')
write_entities('./config/config.yml','tag')

import fileinput

from util_graphql import GraphQL

def write_demos_entities():

    #we retrieve the list of available demos
    my_graphQL = GraphQL()

    if not my_graphQL.environment_is_opened():
        my_graphQL.open_environment('students')

    available_demos = list(my_graphQL.get_projects().values())

    #we open the nlu.md file in read mode to retrieve all the lines of the file
    file = open("./data/nlu.md","r")
    lines = file.readlines()

    #indexes where we will have to add the new known entities
    indexes = []

    #boolean to know if we are in the right intent
    in_right_intent = False

    for ind,line in enumerate(lines):

        #if there is an empty line we automatically store the index of this one without carrying out a test, in order to be able to add our demos.
        if in_right_intent and line=="\n":
            indexes.append(ind)

        elif in_right_intent:
            for item in available_demos:
                if item in line:
                    #if the demo is already known by the file it means that there is no need to add it, so we remove it from our list.
                    available_demos.remove(item)
                else:
                    indexes.append(ind)
        #we check this condition to detect the passage into the intended intent
        if 'open' in line and not in_right_intent:
            in_right_intent = True

        #if we detect the name of the next intent then we are out of the open intent and we stop the loop
        if 'out_of_scope' in line:
            break

    #we insert our new demos in new lines with stored indices
    for i,item in enumerate(available_demos):
        lines.insert(indexes[i],"- ["+item+"]"+"(demo)"+"\n")

    #we now open the file in write mode
    file = open("./data/nlu.md","w")
    #we update the file with the new lines
    file.writelines(lines)
    file.close()

write_demos_entities()

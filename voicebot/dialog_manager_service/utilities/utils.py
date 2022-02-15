import yaml

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
            demo_found = words[ind].lower() in demo_name.lower()
            ind += 1

        if demo_found:
            name = demo_name

        ind = 0
        count += 1

    if demo_found:
        return name

    return None

def prepare_lines(lines,intent_up,intent_down,demos,command,slot):
    "Function that prepare the new lines to add in the nlu file"

    #indexes where we will have to add the new known entities
    indexes = []
    #boolean to know if we are in the right intent
    in_right_intent = False

    for ind,line in enumerate(lines):
        #if there is an empty line we automatically store the index of this one without carrying out a test, in order to be able to add our demos.
        if in_right_intent and line=="\n":
            indexes.append(ind)
        elif in_right_intent:
            for item in demos:
                if item.lower() in line:
                    #if the demo is already known by the file it means that there is no need to add it, so we remove it from our list.
                    demos.remove(item)
                else:
                    indexes.append(ind)
        #we check this condition to detect the passage into the intended intent
        if intent_up in line and not in_right_intent:
            in_right_intent = True
        #if we detect the name of the next intent then we are out of the open intent and we stop the loop
        if intent_down in line:
            break

    #we insert our new demos in new lines with stored indices
    for i,item in enumerate(demos):
        lines.insert(indexes[i],command+'['+item.lower()+']'+'('+slot+')'+'\n')

    return lines

def parse_config(config_path):
    "Function tha parses yml config file"
    with open(config_path,'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        graphql_config = config['graphql']
        config = {}
        for element in graphql_config:
            for key in element.keys():
                config[key]=element[key]
        return config

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from functools import lru_cache
import ast
import operator

class GraphQL:

    """Class managing all methods related to the GDO Controller with this characteristic :
    - its client"""

    def __init__(self):

        sample_transport=RequestsHTTPTransport(
            url='http://129.31.142.150:4000/graphql',
            verify=False,
            retries=3,
        )

        self.client = Client(
            transport=sample_transport,
            fetch_schema_from_transport=True,
        )


    def open_environment(self,name_environment):
        "Function that opens the chosen environment"

        mutation = gql('''
            mutation changeEnvironment($id : String!) {
                changeEnvironment(id:$id){
                    id
                }
            }
        ''')
        params = {
            "id":name_environment
        }
        result = self.client.execute(mutation, variable_values=params)

        return result

    def open_environment_action(self,environment_slot):
        "Function that manages the open environment rasa action"

        try:
            current_environment = self.get_current_environment()
            list_available_environments = self.get_available_environments()
            result = {'success':True}
            if environment_slot == None and self.environment_is_opened():
                result.update({'message':'The current environment is {}'.format(current_environment)})
            elif environment_slot == None:
                result.update({'message':'No environment is open. The available environments are : '+', '.join(list_available_environments)})
            elif environment_slot == current_environment:
                result.update({'message':'The environment is already the '+str(environment_slot)+' one'})
            elif environment_slot not in list_available_environments:
                result.update({'message':"There's no such available environment. The available environments are : "+", ".join(list_available_environments)})
            else:
                result.update({'message':'The environment has been set to {}'.format(self.open_environment(environment_slot)["changeEnvironment"]["id"])})
        except Exception as exc:
            result = {'success':False,'message':str(exc)}
            result.update(ast.literal_eval(str(exc)))
        finally:
            return result

    def login(self,username,password):
        "Function to log in to the GDO launcher"

        mutation = gql('''
            mutation login($username: String!, $password: String!) {
            login(username:$username,password:$password)
            }
        ''')
        params = {
            "username": username,
            "password": password
        }
        result = self.client.execute(mutation, variable_values=params)

        return result

    def environment_is_opened(self):
        "Function to check if an environment is opened"

        query = gql('''
            query current {
                current{
                    id
                }
            }
        '''
        )
        result = self.client.execute(query)
        return result["current"]!=None


    def logout(self):
        "Function to log out"

        mutation = gql('''
            mutation logout {
                logout
            }
        ''')
        result = self.client.execute(mutation)
        return result['logout']


    def turn_on_gdo(self):
        "Function that truns on the GDO"

        try:
            mutation = gql('''
                mutation executePowerAction {
                    executePowerAction(action:"on")
                }
            '''
            )
            result = {"success":True}
            result.update(self.client.execute(mutation))
        except Exception as exc:
            result = {'success':False,'message':str(exc)}
            result.update(ast.literal_eval(str(exc)))
        finally:
            return result

    def turn_off_gdo(self):
        "Function that turns off the GDO"

        try:
            mutation = gql('''
                mutation executePowerAction {
                    executePowerAction(action:"off")
                }
            '''
            )
            result = {"success":True}
            result.update(self.client.execute(mutation))
        except Exception as exc:
            result = {'success':False,'message':str(exc)}
            result.update(ast.literal_eval(str(exc)))
        finally:
            return result

    def mode_is_selected(self):
        "Function that indicates if a mode is selected"

        query = gql('''
            query mode {
                mode{
                    id
                }
            }
        ''')
        result = self.client.execute(query)

        return result['mode']!=None

    def choose_mode(self,mode):
        "Function thar permits to choose a mode between section and cluster or to switch the mode"

        mutation = gql('''
            mutation changeMode($id : String!) {
                changeMode(id:$id){
                    id
                }
            }
        '''
        )
        params = {
            "id":mode
        }
        result = self.client.execute(mutation, variable_values=params)

        return result

    def switch_mode(self,mode_slot,switch_action_slot):
        "Function that manages ActionSwitchMode"
        try:
            current_mode = self.get_current_mode()
            result = {'success':True}

            if mode_slot!="cluster" and mode_slot!="section":
                mode_slot = None

            if mode_slot == None and current_mode == None:
                result.update({'message':'No mode has been selected. You can choose between cluster or section'})
            elif mode_slot == None and switch_action_slot!=None and current_mode=='section':
                result.update({'message':'The mode has been changed to {}'.format(self.choose_mode('cluster')['changeMode']['id'])})
            elif mode_slot == None and switch_action_slot!=None and current_mode=='cluster':
                result.update({'message':'The mode has been changed to {}'.format(self.choose_mode('section')['changeMode']['id'])})
            elif mode_slot == None:
                result.update({'message':'The current mode is {}'.format(current_mode)})
            elif current_mode == mode_slot:
                result.update({'message':'The mode is already {}'.format(current_mode)})
            else:
                result.update({'message':'The mode has been changed to {}'.format(self.choose_mode(mode_slot)['changeMode']['id'])})
        except Exception as exc:
            result = {'success':False,'message':str(exc)}
            result.update(ast.literal_eval(str(exc)))
        finally:
            return result

    def get_current_mode(self):
        "Function that returns the name of the current mode"

        query = gql('''
            query mode {
                mode{
                    id
                }
            }
        ''')
        result = self.client.execute(query)

        if result["mode"] == None:
            return None

        return result["mode"]["id"]

    def get_current_environment(self):
        "Function that returns the name of the current environment"

        query = gql('''
            query current {
                current{
                    id
                }
            }
        '''
        )
        result = self.client.execute(query)

        if result["current"]==None:
            return None

        return result["current"]["id"]

    def clear_screen(self):
        "Function that clears the screen and returns a boolean which indicates if it has been done or not"

        try:
            mutation = gql('''
                mutation cleanSpace {
                  cleanSpace
                }
            ''')
            result = {"success":True}
            result.update(self.client.execute(mutation))
        except Exception as exc:
            result = {'success':False,'message':str(exc)}
            result.update(ast.literal_eval(str(exc)))
        finally:
            return result

    def action_list_demos(self,bot_last_messagae):
        "Function that displays the list of demos"

        try:
            result= {'success':True}
            if self.environment_is_opened():
                list_demos = GraphQL.get_projects()
                if list_demos == None:
                    result.update({'message':'There are no demos available in the current environment {}'.format(self.get_current_environment())})
                elif len(list_demos)>10:
                    if bot_last_messagae == "The list is pretty long ({} demos). Do you still want me to read it out ?".format(len(list_demos)):
                        result.update({'message':'Here are the available demos : '+', '.join(list_demos.values())})
                    else:
                        result.update({'message':"The list is pretty long ({} demos). Do you still want me to read it out ?".format(len(list_demos))})
                else:
                    result.update({'message':'Here are the available demos : '+', '.join(list_demos.values())})
            else:
                result.update({'message':"No environment is open so I can't load the list of demos. You can choose an environment between : "+" ,".join(self.get_available_environments())})
        except Exception as e:
            result = {'success':False,'message':str(exc)}
            result.update(ast.literal_eval(str(exc)))
        finally:
            return result

    @staticmethod
    @lru_cache(maxsize=None)
    def get_projects():
        "Function that returns a map with all available projects (id->name) and None if no environment is selected"

        sample_transport=RequestsHTTPTransport(
            url='http://129.31.142.150:4000/graphql',
            verify=False,
            retries=3,
        )
        client = Client(
            transport=sample_transport,
            fetch_schema_from_transport=True,
        )
        query = gql('''
            query current {
                current{
                    projects{
                        id,name
                    }
                }
            }
        '''
        )
        result = client.execute(query)
        if result['current'] == None:
            return None
        map_projects = {}

        for project in result["current"]["projects"]:
            map_projects[project['id']] = project['name'].lower()
        client.close()

        return map_projects

    def load_project(self,name_project):
        "Function that loads a project, and returns a string to indicate, if the project has been correctly launched"

        mutation = gql('''
            mutation loadProject($projectID: String!) {
                loadProject(projectID:$projectID){
                    id
                }
            }
        '''
        )

        map_projects = GraphQL.get_projects()
        for id, name in map_projects.items():
            if name == name_project:
                id_project = id
        params = {
            "projectID":id_project
        }

        self.client.execute(mutation,variable_values=params)


    def launch_project(self,name_project):
        try:
            result = {'success':True}
            if not self.environment_is_opened():
                result.update({'success':False,'message':'No environment is open'})
            elif name_project == None:
                result.update({'message':'There is no such demo available. Would you like to hear the list ?','list':True})
            else:
                map_projects = GraphQL.get_projects()
                if name_project in map_projects.values():
                    self.load_project(name_project)
                    result.update({'message':'{} is open'.format(name_project),'project':None,'list':False})
                else:
                    similar_project = GraphQL.find_string_in_other_string(name_project,list(map_projects.values()))
                    if similar_project != None:
                        result.update({'message':"I've found this demo : {}. Do you want me to open it ?".format(similar_project),'project':similar_project,'list':False})
                    else:
                        result.update({'success':False,'message':'There is no such demo available. Would you like to hear the list ?'})
        except Exception as exc:
            result = {'success':False,'message':str(exc)}
            result.update(ast.literal_eval(str(exc)))
        finally:
            return result


    def get_available_environments(self):
        "Function that returns all available environments"

        query = gql('''
            query environments {
                environments{
                    id
                }
            }
        '''
        )
        result = self.client.execute(query)
        list_environments = []
        for environment in result['environments']:
            list_environments.append(environment['id'])

        return list_environments


    def get_current_am_User(self):
        "Function that gives the id of the username amUser"

        query = gql('''
            query environments {
                environments{
                    amUser
                }
            }
        '''
        )

        result = self.client.execute(query)

        return result["environments"][0]["amUser"]

    @staticmethod
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



    def project_has_video_controller(self,id):
        "Function that checks if a project has a video or not"

        query = gql('''
            query has_video_controller($id:String!) {
                current {
                    project(id:$id){
                        videoController
                    }
                }
            }
        '''
        )
        params = {
            "id":id
        }
        result = self.client.execute(query,variable_values=params)

        return result["current"]["project"]["videoController"]


    def project_has_html_controller(self,id):
        "Function that checks if a project has a html page or not"

        query = gql('''
            query has_html_controller($id:String!) {
                current {
                    project(id:$id){
                        htmlController
                    }
                }
            }
        '''
        )
        params = {
            "id":id
        }
        result = self.client.execute(query,variable_values=params)

        return result["current"]["project"]["htmlController"]


    def action_browsers(self,id):
        "Function that executes action on browsers"
        try:
            mutation = gql('''
                mutation executeHwAction($action:String!) {
                    executeHwAction(action:$action)
                }
            '''
            )

            params = {
                "action":id
            }
            if not self.environment_is_opened() :
                result = {'success':False,'message':'No environment is open'}
            elif not self.mode_is_selected():
                result = {'success':False,'message':'No mode has been selected'}
            else:
                result = {'success':True}
                result.update(self.client.execute(mutation,variable_values=params))
        except Exception as exc:
            result = {'success':False,'message':str(exc)}
            result.update(ast.literal_eval(str(exc)))
        finally:
            return result

    def open_browsers(self):
        "Function that opens browsers"

        return self.action_browsers("open")

    def close_browsers(self):
        "Function that closes browsers"

        return self.action_browsers("kill")

    def refresh_browsers(self):
        "Function that refreshs browsers"

        return self.action_browsers("refresh")


    def get_current_project(self):
        "Function that returns the current project"

        query = gql('''
            query getProject {
                current{
                    currentProject{id}
                }
            }
        '''
        )

        result = self.client.execute(query)
        if result["current"]["currentProject"]==None:
            return None
        else:
            return result["current"]["currentProject"]["id"]


    def action_controller(self,id_action,id_app,message):
        "Function that executes controller actions"

        try:
            query = gql('''
                mutation executeAppAction($action:String!,$app:String!) {
                    executeAppAction(action:$action,app:$app)
                }
            '''
            )
            params={
                "action":id_action,
                "app":id_app
            }
            result = {'success':True}
            result.update(self.client.execute(query,variable_values=params))
            response = self.get_current_project()
            if response == None:
                result = {'success':False,'message':'No project is open'}
            elif not self.project_has_video_controller(response):
                result =  {'success':False,'message':message}
        except Exception as exc:
            result = {'success':False,'message':str(exc)}
            result.update(ast.literal_eval(str(exc)))
        finally:
            return result

    def play(self):
        "Function that executes play action"
        return self.action_controller('play','OVE_APP_VIDEOS','There is no video controller for this project')


    def pause(self):
        "Function that executes pause action"
        return self.action_controller('pause','OVE_APP_VIDEOS','There is no video controller for this project')


    def stop(self):
        "Function that executes stop action"
        return self.action_controller('stop','OVE_APP_VIDEOS','There is no video controller for this project')

    def reset(self):
        "Function that executes reset action"
        return self.action_controller('seekTo?time=0','OVE_APP_VIDEOS','There is no video controller for this project')


    def play_loop(self):
        "Function that executes play_loop action"
        return self.action_controller('play?loop=true','OVE_APP_VIDEOS','There is no video controller for this project')


    def refresh(self):
        "Function that executes refresh action"
        return self.action_controller('refresh','OVE_APP_HTML','There is no html controller for this project')

    @staticmethod
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

    @staticmethod
    @lru_cache(maxsize=None)
    def get_tags():
        "Function that returns all the tags"

        sample_transport=RequestsHTTPTransport(
            url='http://129.31.142.150:4000/graphql',
            verify=False,
            retries=3,
        )
        client = Client(
            transport=sample_transport,
            fetch_schema_from_transport=True,
        )
        query = gql('''
            query getTags {
                current{
                   tags
                }
            }
        '''
        )
        result = client.execute(query)

        if result['current'] == None:
            return None
        else:
            return result['current']['tags']

    def search_demo_by_tag(self,tag):
        "Function that returns demos names corresponding to a tag"

        query = gql('''
            query searchProjects($tag:String) {
                current{
                   projects(tag:$tag){name}
                }
            }
        '''
        )
        params = {
            "tag":tag
        }
        result = self.client.execute(query,variable_values=params)

        if result['current']==None:
            return None
        elif len(result['current']['projects']) > 0:
            list_names = []
            for name in result['current']['projects']:
                list_names.append(name['name'])
            return list_names
        else:
            return []

    def search_demo_by_word(self,name):
        "Function that filters projects by key word"
        available_demos = GraphQL.get_projects()
        if available_demos!=None and len(available_demos)>0:
            result_search = GraphQL.demo_contains_word(name.lower(),available_demos.values())
            if result_search[0]:
                return result_search[1]

        return []

    def search_process_tag(self,tag):
        "Function that is used in search action process to search by key tag"

        search_result = self.search_demo_by_tag(tag)
        if search_result == None:
            result = {'success':False,'message':"I can't access to any demo"}
        elif len(search_result) == 0:
            result = {'message':"I'm sorry, there is no demo on this topic"}
        elif len(search_result) > 10:
            result = {'message':'The list of demos is too long to read out. Would you like to refine it by other tags?'}
        else:
            result = {'message':'Here are the results for {}'.format(tag)+' : '+', '.join(search_result)}
        return result

    def search_prosess_name(self,name):
        "Function that is used in search action process to search by key word"
        search_result = self.search_demo_by_word(name)
        if len(search_result) == 0:
            result = {'message':"I'm sorry, there is no demo on this topic"}
        elif len(search_result) > 10:
            result = {'message':'The list of demos is too long to read out. Would you like to refine it by other names?'}
        else:
            result = {'message':'Here are the results for {}'.format(name)+' : '+', '.join(search_result)}
        return result

    def search_action(self,name,tag,search_mode):
        "Funtion that executes search action"
        try:
            result = {'success':True,'message':'Do you want to search by tag or by key word ? Please choose one of the both options'}
            if not self.environment_is_opened():
                result.update({'success':False,'message':"I can't access to any demo if no environment is open. Please, open one of these environments before : "+" ,".join(self.get_available_environments())})
            elif 'tag' in search_mode and tag == None:
                result.update({'message':'Fine, please say "search" or "look for" and your tag. If you already did and got no answer for that request that means that no demo contains this tag'})
            elif tag != None:
                result.update(self.search_process_tag(tag))
            elif 'key word' in search_mode and name == None:
                result.update({'message':'Fine, please say "search" or "look for" and your key word. If you already did and got no answer for that request that means that no demo contains this key word'})
            elif name != None:
                result.update(self.search_prosess_name(name))
        except Exception as e:
            result = {'success':False,'message':str(exc)}
            result.update(ast.literal_eval(str(exc)))
        finally:
            return result


if __name__ == '__main__':
    my_graphQL = GraphQL()
    print(my_graphQL.launch_project('cyber data spark'))

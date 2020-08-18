from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from functools import lru_cache
from .utils import parse_config
import ast
import operator
import configparser
import os

class GraphQL:

    """Class managing all methods related to the GDO Controller with this characteristic :
    - its client"""

    def __init__(self,path):

        # self.config = configparser.ConfigParser()
        # self.config.read(path)
        self.config = parse_config(path)
        print(self.config['url'])
        sample_transport=RequestsHTTPTransport(
            url=self.config['url'],
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

    def environment_is_open(self):
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

        mutation = gql('''
            mutation executePowerAction {
                executePowerAction(action:"on")
            }
        '''
        )

        return self.client.execute(mutation)

    def turn_off_gdo(self):
        "Function that turns off the GDO"

        mutation = gql('''
            mutation executePowerAction {
                executePowerAction(action:"off")
            }
        '''
        )

        return self.client.execute(mutation)


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

        mutation = gql('''
            mutation cleanSpace {
              cleanSpace
            }
        ''')

        return self.client.execute(mutation)


    @staticmethod
    @lru_cache(maxsize=None)
    def get_projects(url):
        "Function that returns a map with all available projects (id->name) and None if no environment is selected"

        sample_transport=RequestsHTTPTransport(
            url=url,
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
            map_projects[project['id']] = project['name']
        client.close()

        return map_projects

    def load_project(self,name_project):
        "Function that loads a project"

        mutation = gql('''
            mutation loadProject($projectID: String!) {
                loadProject(projectID:$projectID){
                    id
                }
            }
        '''
        )

        map_projects = GraphQL.get_projects(self.config['url'])
        id_project = ''
        for id, name in map_projects.items():
            if name.lower() == name_project.lower():
                id_project = id
        params = {
            "projectID":id_project
        }

        self.client.execute(mutation,variable_values=params)


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

    def browser_actions(self,id):
        "Function that executes action on browsers"
        mutation = gql('''
            mutation executeHwAction($action:String!) {
                executeHwAction(action:$action)
            }
        '''
        )

        params = {
            "action":id
        }

        return self.client.execute(mutation,variable_values=params)

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

    def controller_actions(self,id_action,id_app):
        "Function that executes controller actions"

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

        return self.client.execute(query,variable_values=params)

    @staticmethod
    @lru_cache(maxsize=None)
    def get_tags(url):
        "Function that returns all the tags"

        sample_transport=RequestsHTTPTransport(
            url=url,
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

    def search_by_tag(self,tag):
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

        return self.client.execute(query,variable_values=params)

    def maps_images_control(self,action, param, app):
        "Function that zoom-in and zoom-out according to a delta level"

        mutation = gql('''
            mutation executeAppAction($action: String!, $param: String = "", $app: String!) {
                    executeAppAction(action:$action,param:$param,app:$app)
            }
        '''
        )
        params = {
            "action":action,
            "param":param,
            "app":app
        }

        result = self.client.execute(mutation,variable_values=params)

        return result['executeAppAction']

    def zoom_maps(self,delta_level):
        "Function to zoom-in or zoom-out maps"
        return self.maps_images_control("zoom",delta_level,"OVE_APP_MAPS")

    def zoom_images(self,delta_level):
        "Function to zoom-in or zoom-out images"
        return self.maps_images_control("zoom",delta_level,"OVE_APP_IMAGES")

    def move_maps(self,orientation):
        "Function to move in maps"
        return self.maps_images_control("move",orientation,"OVE_APP_MAPS")

    def move_images(self,orientation):
        "Function to move in maps"
        return self.maps_images_control("move",orientation,"OVE_APP_IMAGES")

if __name__ == '__main__':
    my_graphQL = GraphQL('../config/config.yml')

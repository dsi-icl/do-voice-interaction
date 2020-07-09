from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

class GraphQL:

    """Class managing all methods related to the GDO Controller with this characteristic :
    - its client"""

    def __init__(self):

        sample_transport=RequestsHTTPTransport(
            url='http://192.168.0.35:4000/graphql',
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
        '''
        )

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

        mutation = gql('''
            mutation executePowerAction {
                executePowerAction(action:"on")
            }
        '''
        )

        result = self.client.execute(mutation)
        return result['executePowerAction']

    def turn_off_gdo(self):
        "Function that turns off the GDO"

        mutation = gql('''
            mutation executePowerAction {
                executePowerAction(action:"off")
            }
        '''
        )

        result = self.client.execute(mutation)
        return result['executePowerAction']

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

        if self.environment_is_opened():
            mutation = gql('''
                mutation cleanSpace {
                  cleanSpace
                }
            ''')

            result = self.client.execute(mutation)

            return result["cleanSpace"] == "cleaned"

        return False

    def get_projects(self):
        "Function that returns a map with all available projects (id->name) and None if no environment is selected"

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

        result = self.client.execute(query)

        if result['current'] == None:
            return None

        map_projects = {}

        for project in result["current"]["projects"]:
            map_projects[project['id']] = project['name']

        return map_projects

    def load_project(self,name_project):
        "Function that loads a project, and returns a string to indicate, if the project has been correctly launched"

        if not self.environment_is_opened():
            return "NO ENVIRONMENT IS OPENED"

        if not self.mode_is_selected():
            return "NO MODE IS SELECTED"

        map_projects = self.get_projects()

        if not name_project in map_projects.values():
            return "NO PROJECT WITH THIS NAME"


        mutation = gql('''
            mutation loadProject($projectID: String!) {
                loadProject(projectID:$projectID){
                    id
                }
            }
        ''')

        for id, name in map_projects.items():
            if name == name_project:
                id_project = id

        params = {
            "projectID":id_project
        }

        self.client.execute(mutation,variable_values=params)
        return "OK"

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



if __name__ == '__main__':
    my_graphQL = GraphQL()
    print(my_graphQL.open_environment("students"))
    # my_graphQL.login('guest','guest')
    # my_graphQL.logout()
    # my_graphQL.turn_on_gdo()
    # my_graphQL.turn_off_gdo()
    print(my_graphQL.choose_mode("cluster"))

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from util_graphql import GraphQL

import unittest

class TestRequestsGDO(unittest.TestCase):

    def test_open_environment(self):

        my_graphQL = GraphQL()
        result = my_graphQL.open_environment("students")

        self.assertEqual(result["changeEnvironment"]["id"],"students")

        my_graphQL.client.close()


    def test_get_current_environment(self):

        my_graphQL = GraphQL()
        my_graphQL.open_environment("students")

        self.assertEqual(my_graphQL.get_current_environment(),"students")

        my_graphQL.client.close()

    def test_environment_is_opened(self):

        my_graphQL = GraphQL()

        if not my_graphQL.environment_is_opened():
            self.assertEqual(my_graphQL.get_current_environment(),None)

        my_graphQL.client.close()


    def test_mode_is_selected(self):

        my_graphQL = GraphQL()

        if not my_graphQL.mode_is_selected():
            self.assertEqual(my_graphQL.get_current_mode(),None)

        my_graphQL.client.close()

    def test_login(self):

        my_graphQL = GraphQL()

        if not my_graphQL.environment_is_opened():
            my_graphQL.open_environment("students")

        result = my_graphQL.login("admin","adminadmin")

        self.assertEqual(result['login'],'ok')
        self.assertEqual(my_graphQL.get_current_am_User(),'admin')

        result = my_graphQL.login("guest","guest")

        self.assertEqual(result['login'],'ok')
        self.assertEqual(my_graphQL.get_current_am_User(),'guest')

        my_graphQL.client.close()


    def test_logout(self):

        my_graphQL = GraphQL()

        self.assertEqual(my_graphQL.logout(),'ok')

        my_graphQL.client.close()


    def test_turn_on_gdo(self):

        my_graphQL = GraphQL()

        self.assertEqual(my_graphQL.turn_on_gdo(),'on')

        my_graphQL.client.close()


    def test_turn_off_gdo(self):

        my_graphQL = GraphQL()

        self.assertEqual(my_graphQL.turn_off_gdo(),'off')

        my_graphQL.client.close()

    def test_choose_mode(self):

        my_graphQL = GraphQL()

        if my_graphQL.get_current_mode()=='section':
            result = my_graphQL.choose_mode('section')
            self.assertEqual(result['changeMode']['id'],None)
            result = my_graphQL.choose_mode('cluster')
            self.assertEqual(result['changeMode']['id'],'cluster')

        if my_graphQL.get_current_mode()=='cluster':
            result = my_graphQL.choose_mode('cluster')
            self.assertEqual(result['changeMode']['id'],None)
            result = my_graphQL.choose_mode('section')
            self.assertEqual(result['changeMode']['id'],'section')

        my_graphQL.client.close()


    def test_clear_screen(self):

        my_graphQL = GraphQL()

        if my_graphQL.environment_is_opened():
            result = my_graphQL.clear_screen()
            self.assertEqual(result,True)

        my_graphQL.client.close()

    def test_get_projects(self):

        my_graphQL = GraphQL()

        my_graphQL.open_environment("students")

        map = my_graphQL.get_projects()

        list_projects = ['airesearch','amr','test-controllers']
        for ind,project in enumerate(map.values()):
            self.assertEqual(project,list_projects[ind])

        my_graphQL.client.close()


    def test_load_project(self):

        my_graphQL = GraphQL()

        if not my_graphQL.environment_is_opened():
            response = my_graphQL.load_project("airesearch")
            self.assertEqual(response,"NO ENVIRONMENT IS OPENED")

        if my_graphQL.environment_is_opened() and not my_graphQL.mode_is_selected():
            response = my_graphQL.load_project("airesearch")
            self.assertEqual(response,"NO MODE IS SELECTED")

        if my_graphQL.environment_is_opened() and my_graphQL.mode_is_selected():
            response = my_graphQL.load_project("mars selfies")
            self.assertEqual(response,"NO PROJECT WITH THIS NAME")

            response = my_graphQL.load_project("airesearch")
            self.assertEqual(response,"OK")

        my_graphQL.client.close()



if __name__ == '__main__':
    unittest.main()

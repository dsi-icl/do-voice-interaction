from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import time
import unittest
import sys
sys.path.append("../..")
from utilities.utils_graphql import GraphQL

class TestRequestsGDO(unittest.TestCase):

    def test_open_environment(self):

        my_graphQL = GraphQL('../../config/config.yml')
        result = my_graphQL.open_environment("students")
        self.assertEqual(result["changeEnvironment"]["id"],"students")
        my_graphQL.client.close()


    def test_get_current_environment(self):

        my_graphQL = GraphQL('../../config/config.yml')
        my_graphQL.open_environment("students")
        self.assertEqual(my_graphQL.get_current_environment(),"students")
        my_graphQL.client.close()

    def test_environment_is_open(self):

        my_graphQL = GraphQL('../../config/config.yml')
        if not my_graphQL.environment_is_open():
            self.assertEqual(my_graphQL.get_current_environment(),None)
        my_graphQL.client.close()


    def test_mode_is_selected(self):

        my_graphQL = GraphQL('../../config/config.yml')
        if not my_graphQL.mode_is_selected():
            self.assertEqual(my_graphQL.get_current_mode(),None)
        my_graphQL.client.close()


    def test_logout(self):

        my_graphQL = GraphQL('../../config/config.yml')
        self.assertEqual(my_graphQL.logout(),'ok')
        my_graphQL.client.close()


    def test_turn_on_gdo(self):

        my_graphQL = GraphQL('../../config/config.yml')
        self.assertEqual(my_graphQL.turn_on_gdo()["executePowerAction"],'on')
        my_graphQL.client.close()


    def test_turn_off_gdo(self):

        my_graphQL = GraphQL('../../config/config.yml')
        self.assertEqual(my_graphQL.turn_off_gdo()["executePowerAction"],'off')
        my_graphQL.client.close()

    def test_choose_mode(self):

        my_graphQL = GraphQL('../../config/config.yml')

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

        my_graphQL = GraphQL('../../config/config.yml')

        if my_graphQL.environment_is_open():
            result = my_graphQL.clear_screen()
            self.assertEqual(result['cleanSpace'],"cleaned")

        my_graphQL.client.close()

    def test_turn_on_gdo(self):

        my_graphQL = GraphQL('../../config/config.yml')
        self.assertEqual(my_graphQL.turn_on_gdo()["executePowerAction"],'on')
        my_graphQL.client.close()


    def test_turn_off_gdo(self):

        my_graphQL = GraphQL('../../config/config.yml')
        self.assertEqual(my_graphQL.turn_off_gdo()["executePowerAction"],'off')
        my_graphQL.client.close()

    def test_open_browsers(self):

        my_graphQL = GraphQL('../../config/config.yml')

        if not my_graphQL.environment_is_open():
            my_graphQL.open_environment("students")

        if not my_graphQL.mode_is_selected():
            my_graphQL.choose_mode("section")

        self.assertEqual(my_graphQL.browser_actions("open")['executeHwAction'],"done")

        my_graphQL.client.close()

    def test_close_browsers(self):

        my_graphQL = GraphQL('../../config/config.yml')

        if not my_graphQL.environment_is_open():
            my_graphQL.open_environment("students")

        if not my_graphQL.mode_is_selected():
            my_graphQL.choose_mode("section")

        self.assertEqual(my_graphQL.browser_actions("kill")['executeHwAction'],"done")

        my_graphQL.client.close()

    def test_reset_browsers(self):

        my_graphQL = GraphQL('../../config/config.yml')

        if not my_graphQL.environment_is_open():
            my_graphQL.open_environment("students")

        if not my_graphQL.mode_is_selected():
            my_graphQL.choose_mode("section")

        self.assertEqual(my_graphQL.browser_actions("refresh")['executeHwAction'],"done")

        my_graphQL.client.close()

    def test_get_current_project(self):

        my_graphQL = GraphQL('../../config/config.yml')
        if not my_graphQL.environment_is_open():
            my_graphQL.open_environment("students")

        random_name = list(GraphQL.get_projects(my_graphQL.config['url']).values())[0]
        my_graphQL.load_project(random_name)
        self.assertEqual(my_graphQL.get_current_project(),list(GraphQL.get_projects(my_graphQL.config['url']).keys())[0])
        my_graphQL.clear_screen()
        self.assertEqual(my_graphQL.get_current_project(),None)
        my_graphQL.client.close()

    def test_play(self):

        my_graphQL = GraphQL('../../config/config.yml')
        if not my_graphQL.environment_is_open():
            my_graphQL.open_environment("students")

        project = my_graphQL.get_current_project()
        if project == None:
            random_name = list(GraphQL.get_projects(my_graphQL.config['url']).values())[0]
            my_graphQL.load_project(random_name)
            project = my_graphQL.get_current_project(),

        self.assertEqual(my_graphQL.controller_actions("play",'OVE_APP_VIDEOS')['executeAppAction'],"done")
        my_graphQL.client.close()

    def test_pause(self):

        my_graphQL = GraphQL('../../config/config.yml')
        if not my_graphQL.environment_is_open():
            my_graphQL.open_environment("students")

        project = my_graphQL.get_current_project()
        if project == None:
            random_name = list(GraphQL.get_projects(my_graphQL.config['url']).values())[0]
            my_graphQL.load_project(random_name)
            project = my_graphQL.get_current_project()

        self.assertEqual(my_graphQL.controller_actions("pause",'OVE_APP_VIDEOS')['executeAppAction'],"done")
        my_graphQL.client.close()

    def test_stop(self):

        my_graphQL = GraphQL('../../config/config.yml')
        if not my_graphQL.environment_is_open():
            my_graphQL.open_environment("students")

        project = my_graphQL.get_current_project()
        if project == None:
            random_name = list(GraphQL.get_projects(my_graphQL.config['url']).values())[0]
            my_graphQL.load_project(random_name)
            project = my_graphQL.get_current_project()

        self.assertEqual(my_graphQL.controller_actions("stop",'OVE_APP_VIDEOS')['executeAppAction'],"done")
        my_graphQL.client.close()

    def test_play_loop(self):

        my_graphQL = GraphQL('../../config/config.yml')
        if not my_graphQL.environment_is_open():
            my_graphQL.open_environment("students")

        project = my_graphQL.get_current_project()
        if project == None:
            random_name = list(GraphQL.get_projects(my_graphQL.config['url']).values())[0]
            my_graphQL.load_project(random_name)
            project = my_graphQL.get_current_project()

        self.assertEqual(my_graphQL.controller_actions("play?loop=true",'OVE_APP_VIDEOS')['executeAppAction'],"done")
        my_graphQL.client.close()

    def test_reset(self):

        my_graphQL = GraphQL('../../config/config.yml')
        if not my_graphQL.environment_is_open():
            my_graphQL.open_environment("students")

        project = my_graphQL.get_current_project()
        if project == None:
            random_name = list(GraphQL.get_projects(my_graphQL.config['url']).values())[0]
            my_graphQL.load_project(random_name)
            project = my_graphQL.get_current_project()

        self.assertEqual(my_graphQL.controller_actions("seekTo?time=0",'OVE_APP_VIDEOS')['executeAppAction'],"done")
        my_graphQL.client.close()

    def test_refresh(self):

        my_graphQL = GraphQL('../../config/config.yml')
        if not my_graphQL.environment_is_open():
            my_graphQL.open_environment("students")

        project = my_graphQL.get_current_project()
        if project == None:
            random_name = list(GraphQL.get_projects(my_graphQL.config['url']).values())[0]
            my_graphQL.load_project(random_name)
            project = my_graphQL.get_current_project()

        self.assertEqual(my_graphQL.controller_actions("refresh",'OVE_APP_HTML')['executeAppAction'],"done")
        my_graphQL.client.close()


    # def test_get_projects(self):
    #
    #     my_graphQL = GraphQL('../../config/config.yml')
    #
    #     my_graphQL.open_environment("students")
    #
    #     map = GraphQL.get_projects()
    #
    #     list_projects = ['airesearch','amr','test-controllers']
    #     for ind,project in enumerate(map.values()):
    #         self.assertEqual(project,list_projects[ind])
    #
    #     my_graphQL.client.close()


if __name__ == '__main__':
    unittest.main()

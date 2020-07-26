# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from functools import lru_cache
from util_graphql import GraphQL

class ActionOpen(Action):

    def name(self) -> Text:
        return "action_open"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        my_graphQL = GraphQL()

        if tracker.get_slot("demo_name") != None:
            response = my_graphQL.load_project(tracker.get_slot("demo_name"))
        elif tracker.get_slot("demo")==None:
            dispatcher.utter_message(text="There is no such demo available. Would you like to hear the list ?")
            my_graphQL.client.close()
            return [SlotSet("demo",None),SlotSet("demo_name",None)]
        else:
            response = my_graphQL.load_project(tracker.get_slot("demo"))


        if response=="NO ENVIRONMENT IS OPENED":
            list_environments = my_graphQL.get_available_environments()
            dispatcher.utter_message("Please, choose an environment before. Here are the available environments : "+", ".join(list_environments))
            dispatcher.utter_message("You'll might have to choose a mode before launching ",tracker.get_slot("demo"))
        if response=="NO MODE IS SELECTED":
            dispatcher.utter_message(text="Please, select a mode between cluster and section")

        if response=="NO PROJECT WITH THIS NAME":
            available_demos = GraphQL.get_projects()
            name = GraphQL.find_string_in_other_string(tracker.get_slot("demo"),list(available_demos.values()))
            if name != None:
                dispatcher.utter_message(text="I've found this demo : "+str(name)+". If you want me to open it, please say open?")
                return [SlotSet("demo",None), SlotSet("demo_name",name)]
            else:
                dispatcher.utter_message(text="There is no such demo available. Would you like to hear the list ?")

        if response=="OK":
            dispatcher.utter_message(text="Opening demo...")

        my_graphQL.client.close()

        return [SlotSet("demo",None),SlotSet("demo_name",None)]

class ActionListDemos(Action):

    def name(self) -> Text:
        return "action_list_demos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        my_graphQL = GraphQL()

        response = GraphQL.get_projects()

        if response == None :
            list_environments = my_graphQL.get_available_environments()
            dispatcher.utter_message("I'm sorry, something went wrong. It seems that no environment is opened. Please choose an environment before. Here are all available environments : "+" ,".join(list_environments))

        elif len(response.values()) == 0:
            dispatcher.utter_message(text="There are no available demo.")

        else :
            dispatcher.utter_message("Here is the list of available demos : "+", ".join(response.values()))

        my_graphQL.client.close()

        return []


class ActionShutDown(Action):

    def name(self) -> Text:
        return "action_shutdown"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        my_graphQL = GraphQL()

        if my_graphQL.turn_off_gdo()=="off":
            print("The screens are shut down")
            dispatcher.utter_message("The screens are shut down")
        else:
            dispatcher.utter_message(text="Something went wrong. Do you want me to restart ?")

        my_graphQL.client.close()

        return []

class ActionTurnOnGDO(Action):

    def name(self) -> Text:
        return "action_turn_on_gdo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        my_graphQL = GraphQL()

        if my_graphQL.turn_on_gdo()=="on":
            print("The GDO is on")
            dispatcher.utter_message(text="The Global Data Observatory is on")
        else:
            dispatcher.utter_message(text="Something went wrong. Do you want me to restart ?")

        my_graphQL.client.close()

        return []

class ActionControl(Action):

        def name(self) -> Text:
            return "action_control"


        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            control = tracker.get_slot("control_command")

            if control != None:
                control = control.lower()

            if control=="play":
                print("Playing the video/audio...")
                dispatcher.utter_message("I'm playing the video/audio")
            elif control=="pause":
                print("The video/audio is paused")
                dispatcher.utter_message("The video/audio is paused")
            elif control=="stop":
                print("The video/audio is stopped")
                dispatcher.utter_message("I stopped the video/audio")
            elif control=="mute":
                print("The video/audio is muted")
                dispatcher.utter_message("I've muted the video/audio")
            elif control=="refresh":
                print("Refreshing the webpage...")
                dispatcher.utter_message("Webpage refreshing in progress")
            else :
                print("Unknown control command")
                dispatcher.utter_message("I'm sorry, I can't execute this command. Either I misunderstood it (in that case, please repeat it) or it's not part of my features (ask help to have more information).")

            return [SlotSet("control_command",None)]

class ActionSearch(Action):

        def name(self) -> Text:
            return "action_search"

        def demo_contains_tag(self,tag, available_demos):

            tag_found = False
            list_chosen_demos = []
            for demo_name in available_demos:
                if tag in demo_name.lower():
                    list_chosen_demos.append(demo_name)
                    if not tag_found:
                        tag_found = True

            return tag_found,list_chosen_demos


        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            tag = tracker.get_slot("demo")

            my_graphQL = GraphQL()

            available_demos = GraphQL.get_projects()

            if available_demos == None:
                dispatcher.utter_message(text="First, open an environment please")
            elif tag == None:
                dispatcher.utter_message(text="I'm sorry, there is no demos on this topic")
            else:
                dispatcher.utter_message(text="Reading the demos...")
                available_demos_names = available_demos.values()
                result_search = self.demo_contains_tag(tag.lower(),available_demos_names)
                if result_search[0]:
                    ids_demos_tag =result_search[1]
                    if len(ids_demos_tag)<=10:
                        dispatcher.utter_message("Results for "+str(tracker.get_slot("demo"))+" : "+", ".join(ids_demos_tag))
                    else:
                        dispatcher.utter_message(text="The list of demos is too long to read out. Would you like to refine it by other tags?")
                else:
                    dispatcher.utter_message(text="I'm sorry, there is no demos on this topic")

            my_graphQL.client.close()

            return [SlotSet("demo",None)]


class ActionClearSpace(Action):

        def name(self) -> Text:
            return "action_clear_space"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            my_graphQL = GraphQL()

            if not my_graphQL.clear_screen():
                dispatcher.utter_message(text="No environment is opened. I can't display clear the screens")
            else:
                print("Clear space")
                dispatcher.utter_message("The space is cleaned")

            my_graphQL.client.close()

            return []

class ActionSwitchMode(Action):

        def name(self) -> Text:
            return "action_switch_modes"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            my_graphQL = GraphQL()

            mode = tracker.get_slot('mode')
            current_mode = my_graphQL.get_current_mode()

            if mode == None:
                if current_mode == None:
                    dispatcher.utter_message(text="No mode has been selected. You can choose between cluster or section")
                else :
                    dispatcher.utter_message(text="The current mode is {}".format(current_mode))
                    if current_mode == "section":
                        new_mode = my_graphQL.choose_mode("cluster")
                        dispatcher.utter_message(text="The mode has been changed to {}".format(new_mode['changeMode']['id']))
                    elif current_mode == "cluster":
                        new_mode = my_graphQL.choose_mode("section")
                        dispatcher.utter_message(text="The mode has been changed to {}".format(new_mode['changeMode']['id']))
            else:
                if current_mode == mode:
                    dispatcher.utter_message(text="The mode is already {}".format(current_mode))
                else:
                    new_mode = my_graphQL.choose_mode(mode)
                    dispatcher.utter_message(text="The mode has been changed to {}".format(new_mode['changeMode']['id']))

            my_graphQL.client.close()

            return [SlotSet("mode",None)]

class ActionOpenEnvironment(Action):

        def name(self) -> Text:
            return "action_open_environment"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            my_graphQL = GraphQL()

            environment = tracker.get_slot('work_environment')

            current_environment = my_graphQL.get_current_environment()

            list_available_environments = my_graphQL.get_available_environments()

            if environment==None:
                if my_graphQL.environment_is_opened():
                    dispatcher.utter_message(text="The current environment is {}".format(current_environment))
                else :
                    dispatcher.utter_message("No environment is open")
                dispatcher.utter_message(text="The available environments are : "+", ".join(list_available_environments))
            else:
                if environment == current_environment:
                    dispatcher.utter_message(text="The environment is already the "+str(environment)+" one")
                elif environment not in list_available_environments:
                    dispatcher.utter_message(text="There's no such available environment")
                    dispatcher.utter_message(text="The available environments are : "+", ".join(list_available_environments))
                else:
                    dispatcher.utter_message(text="The environement has been set to {}".format(my_graphQL.open_environment(environment)["changeEnvironment"]["id"]))

            my_graphQL.client.close()

            return [SlotSet("work_environment",None)]

class ActionHelp(Action):

        def name(self) -> Text:
            return "action_help"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            dispatcher.utter_message(text="I can execute the following commands :")
            dispatcher.utter_message(text="-[Please]? open <demo>")
            dispatcher.utter_message(text="-Show me something on <tag>")
            dispatcher.utter_message(text="-Launch <demo>")
            dispatcher.utter_message(text="-Activate <demo>")
            dispatcher.utter_message(text="-Shutdown screens")
            dispatcher.utter_message(text="-Reset browsers")
            dispatcher.utter_message(text="-Do a clearspace")
            dispatcher.utter_message(text="-Refresh the screens")
            dispatcher.utter_message(text="-Pause [the video/the audio]")
            dispatcher.utter_message(text="-Play <video>")
            dispatcher.utter_message(text="-Start animation")
            dispatcher.utter_message(text="-Stop animation")
            dispatcher.utter_message(text="-Quit [video/audio]")
            dispatcher.utter_message(text="-Mute [video/audio]")
            dispatcher.utter_message(text="-Full black screens")
            dispatcher.utter_message(text="-Open environment")
            dispatcher.utter_message(text="-Switch mode")
            dispatcher.utter_message(text="-Turn on the Global Data Observatory")
            dispatcher.utter_message(text="-Shutdown the Global Data Observatory")
            dispatcher.utter_message(text="-Open/Close/Reset browsers")

            return []

class ActionResetSlot(Action):

    def name(self):
        return "action_reset_slot"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("demo", None), SlotSet("demo_name",None)]

class ActionOpenBrowsers(Action):

    def name(self):
        return "action_open_browsers"

    def run(self, dispatcher, tracker, domain):

        my_graphQL = GraphQL()

        if not my_graphQL.environment_is_opened():
            dispatcher.utter_message(text="Please, open en environment before")
        elif not my_graphQL.mode_is_selected():
            dispatcher.utter_message(text="Please, select a mode before")
        elif my_graphQL.open_browsers():
            dispatcher.utter_message(text="The browsers are open")
        else:
            dispatcher.utter_message(text="Something went wrong. Do you want me to try again ?")

        my_graphQL.client.close()
        return []

class ActionCloseBrowsers(Action):

    def name(self):
        return "action_close_browsers"

    def run(self, dispatcher, tracker, domain):

        my_graphQL = GraphQL()

        if not my_graphQL.environment_is_opened():
            dispatcher.utter_message(text="Please, open en environment before")
        elif not my_graphQL.mode_is_selected():
            dispatcher.utter_message(text="Please, select a mode before")
        elif my_graphQL.close_browsers():
            dispatcher.utter_message(text="The browsers are closed")
        else:
            dispatcher.utter_message(text="Something went wrong. Do you want me to try again ?")

        my_graphQL.client.close()
        return []

class ActionRefreshBrowsers(Action):

    def name(self):
        return "action_refresh_browsers"

    def run(self, dispatcher, tracker, domain):

        my_graphQL = GraphQL()

        if not my_graphQL.environment_is_opened():
            dispatcher.utter_message(text="Please, open en environment before")
        elif not my_graphQL.mode_is_selected():
            dispatcher.utter_message(text="Please, select a mode before")
        elif my_graphQL.refresh_browsers():
            dispatcher.utter_message(text="The browsers are refreshed")
        else:
            dispatcher.utter_message(text="Something went wrong. Do you want me to try again ?")

        my_graphQL.client.close()
        return []

class ActionRepeat(Action):

    def name(self):
        return "action_repeat"

    def run(self, dispatcher, tracker, domain):

        if len(tracker.events) >= 3:
                dispatcher.utter_message(tracker.events[-3].get('text'))

        return []

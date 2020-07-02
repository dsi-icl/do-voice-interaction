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

import requests
import requests_cache

from utils import get_access_token, get_list_demos

class ActionOpen(Action):

    def name(self) -> Text:
        return "action_open"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        requests_cache.install_cache('project cache')

        token = get_access_token('guest','guest')

        print("the name of the slot :",tracker.get_slot("demo"))
        if token!=None:
            response = requests.get('http://gdo-students.dsi.ic.ac.uk:6080/api/dev-store/list?metadata=true', headers={'AUTH_TOKEN': token})
            if response.status_code==200:
                available_demos = get_list_demos(response.json())
                if tracker.get_slot("demo") in available_demos:
                    dispatcher.utter_message(text="Opening demo")
                else:
                    dispatcher.utter_message(text="There is no such demo available. Would you like to hear the list ?")
            else:
                dispatcher.utter_message(text="I'm sorry, something went wrong. Do you want me to restart ? (Restart/no)")
        else:
            dispatcher.utter_message(text="I'm sorry, I don't have any access to the AssetManager RESTFUL service. I need assistance")
        return [SlotSet("demo",None)]

class ActionListDemos(Action):

    def name(self) -> Text:
        return "action_list_demos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        requests_cache.install_cache('project cache')

        token = get_access_token('guest','guest')

        if token!=None:
            response = requests.get('http://gdo-students.dsi.ic.ac.uk:6080/api/dev-store/list?metadata=true', headers={'AUTH_TOKEN': token})
            if response.status_code==200:
                available_demos = get_list_demos(response.json())
                dispatcher.utter_message("Here is the list of available demos : {}".format(available_demos))
            else:
                dispatcher.utter_message(text="I'm sorry, something went wrong.")
        else:
            dispatcher.utter_message(text="I'm sorry, I don't have any access to the AssetManager RESTFUL service.")
        return []

class ActionShutDown(Action):

    def name(self) -> Text:
        return "action_shutdown"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("Shutting down screens...")
        dispatcher.utter_message("Screens shutdown in progress")

        return []

class ActionUniformScreens(Action):

    def name(self) -> Text:
        return "action_uniform_screens"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        color = tracker.get_slot("color")

        if color != None:
            color = color.lower()

        if color=="white":
            print("Full white screens")
            dispatcher.utter_message("White background in progress")
        elif color=="black":
            print("Full black screens")
            dispatcher.utter_message("Black background in progress")
        else:
            print("Did not identify the background color")
            dispatcher.utter_message("I'm sorry I can only display a black or white background.")

        return [SlotSet("color",None)]

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

            requests_cache.install_cache('project cache')

            token = get_access_token('guest','guest')

            print("the name of the slot :",tracker.get_slot("demo"))

            if token!=None and tag!= None:
                response = requests.get('http://gdo-students.dsi.ic.ac.uk:6080/api/dev-store/list?metadata=true', headers={'AUTH_TOKEN': token})
                if response.status_code==200:
                    available_demos = get_list_demos(response.json())
                    result_search = self.demo_contains_tag(tag.lower(),available_demos)
                    if result_search[0]:
                        ids_demos_tag =result_search[1]
                        dispatcher.utter_message(text="Reading the demos")
                        dispatcher.utter_message("Results for {} : {}".format(tracker.get_slot("demo"),ids_demos_tag))
                    else:
                        dispatcher.utter_message(text="The list of demos is too long to read out. Would you like to refine it by other tags?")
                else:
                    dispatcher.utter_message(text="I'm sorry, something went wrong. Do you want me to restart ? (Restart/no)")
            elif token == None:
                dispatcher.utter_message(text="I'm sorry, I don't have any access to the AssetManager RESTFUL service. I need assistance")
            else:
                dispatcher.utter_message(text="I'm sorry, there is no demos on this topic")


            return [SlotSet("demo",None)]

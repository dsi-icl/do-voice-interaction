# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from functools import lru_cache
from util_graphql import GraphQL

class ActionOpen(Action):
    """A class used to open demos"""

    def name(self) -> Text:
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""

        return "action_open"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Function that manages the robot's behavior for the ''open''action.

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        my_graphQL = GraphQL()

        #demo_name is a slot used to store the demo name suggested by the bot according to the user request.
        #If it's not empty the it means that the user accepted to open the suggested demo
        if tracker.get_slot("demo_name") != None:
            response = my_graphQL.load_project(tracker.get_slot("demo_name"))
            #We store the demo name to be open
            demo = tracker.get_slot("demo_name")
        #The demo slot is an entity and a text slot. Each day, demo values will be updated in the nlu.md file executing the utils file.
        #If the slot is empty it means that user request doesn't contain any available project name.
        elif tracker.get_slot("demo")==None:
            dispatcher.utter_message(text="There is no such demo available. Would you like to hear the list ?")
            my_graphQL.client.close()
            return [SlotSet("demo",None),SlotSet("demo_name",None)]
        else:
            response = my_graphQL.load_project(tracker.get_slot("demo"))
            #We store the demo name to be open
            demo = tracker.get_slot("demo")

        if response=="NO ENVIRONMENT IS OPENED":
            list_environments = my_graphQL.get_available_environments()
            dispatcher.utter_message("Please, choose an environment before. Here are the available environments : "+", ".join(list_environments))
            dispatcher.utter_message("You'll might have to choose a mode before launching {}".format(tracker.get_slot("demo")))

        elif response=="NO MODE IS SELECTED":
            dispatcher.utter_message(text="Please, select a mode between cluster and section")

        elif response=="NO PROJECT WITH THIS NAME":
            available_demos = GraphQL.get_projects()
            name = GraphQL.find_string_in_other_string(demo,list(available_demos.values()))
            #If a demo contains this name it will be suggested
            if name != None:
                dispatcher.utter_message(text="I've found this demo : "+str(name)+". If you want me to open it, please say open?")
                my_graphQL.client.close()
                return [SlotSet("demo",None), SlotSet("demo_name",name)]
            else:
                dispatcher.utter_message(text="There is no such demo available. Would you like to hear the list ?")

        elif response=="OK":
            dispatcher.utter_message(text="Opening demo...")
            my_graphQL.client.close()
            return [SlotSet("demo",None),SlotSet("demo_name",None),SlotSet("current_demo",demo)]

        my_graphQL.client.close()
        return [SlotSet("demo",None),SlotSet("demo_name",None)]

class ActionListDemos(Action):
    """A class used to list available demos"""

    def name(self) -> Text:
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""

        return "action_list_demos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Function that manages the robot's behavior to display available demos.

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        try:
            my_graphQL = GraphQL()
        except Exception as e:
            dispatcher.utter_message(text="I'm sorry, something went wrong. {}".format(e))
            print(e)
            return []

        robot_last_message = ""
        if len(tracker.events) >= 3:
            robot_last_message = tracker.events[-3].get('text')

        print("Trying to get available demos...")
        response = my_graphQL.action_list_demos(robot_last_message)
        if response['success']:
            dispatcher.utter_message(text=response['message'])
            print("Success :)")
        else:
            dispatcher.utter_message(text="Something went wrong. {}".format(response['message']))
            dispatcher.utter_message(text="Should I try again ?")
            print(response['message'])
        return []


class ActionShutDown(Action):
    """A class used to shutdown the GDO"""

    def name(self) -> Text:
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""

        return "action_shutdown"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Function that manages the robot's behavior to shutdown the GDO

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        try:
            my_graphQL = GraphQL()
        except Exception as e:
            dispatcher.utter_message(text="I'm sorry, something went wrong. {}".format(e))
            print(e)
            return []

        response = my_graphQL.turn_off_gdo()

        print("Trying to shutdown the GDO...")
        if response['success'] and response['executePowerAction']=="off":
            dispatcher.utter_message(text="The Global Data Observatory is off")
            print("The GDO is off :)")
        elif not response['success']:
            dispatcher.utter_message(text="Something went wrong. {}".format(response['message']))
            dispatcher.utter_message(text="Do you want me to try again ?")
            print(response["message"])
        else:
            dispatcher.utter_message(text="Something went wrong. Do you want me to try again ?")
            print("Fail :(")

        my_graphQL.client.close()

class ActionTurnOnGDO(Action):
    """A class used to turn on the GDO"""

    def name(self) -> Text:
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""

        return "action_turn_on_gdo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Function that manages the robot's behavior to turn on the GDO.

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        try:
            my_graphQL = GraphQL()
        except Exception as e:
            dispatcher.utter_message(text="I'm sorry, something went wrong. {}".format(e))
            print(e)
            return []

        response = my_graphQL.turn_on_gdo()

        print("Trying to turn on the GDO...")
        print(response)
        if response['success'] and response['executePowerAction']=="on":
            dispatcher.utter_message(text="The Global Data Observatory is on")
            print("The GDO is on :)")
        elif not response['success']:
            dispatcher.utter_message(text="Something went wrong. {}".format(response['message']))
            dispatcher.utter_message(text="Do you want me to try again ?")
            print(response["message"])
        else:
            dispatcher.utter_message(text="Something went wrong. Do you want me to try again ?")
            print("Fail :(")

        my_graphQL.client.close()

        return []

class ActionControl(Action):
    """A class used to execute a controller action"""

    def name(self) -> Text:
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""

        return "action_control"

    def process_response(self, dispatcher: CollectingDispatcher, message_success: str, message_fail: str, response):
        if response['success'] == True and response['executeAppAction']=='done':
            dispatcher.utter_message(message_success)
            print("Done ! :)")
        elif response['success'] == True:
            dispatcher.utter_message(message_fail)
            print("The action has not been executed :(")
        else:
            dispatcher.utter_message("I'm sorry. Something went wrong.")
            dispatcher.utter_message(response['message'])
            print(response['message'])


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Function that manages the robot's behavior to execute a control command.

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        try:
            my_graphQL = GraphQL()
        except Exception as e:
            dispatcher.utter_message(text="I'm sorry, something went wrong. {}".format(e))
            print(e)
            return []

        control = tracker.get_slot("control_command")

        #If the control command is not recognized, we inform the user
        if control == None:
            dispatcher.utter_message("Sorry I didn't get the command")
            return [SlotSet("control_command",None)]
        else:
            control = control.lower()

        if control=="play":
            print("Trying to play the video/audio...")
            response = my_graphQL.play()
            self.process_response(dispatcher,"I'm playing the video","I didn't start playing the video. Try again please",response)
        elif control=="pause":
            print("Trying to pause the video/audio...")
            response = my_graphQL.pause()
            self.process_response(dispatcher,"I paused the video","I didn't pause the video. Try again please",response)
        elif control=="stop":
            print("Trying to stop the video/audio...")
            response = my_graphQL.stop()
            self.process_response(dispatcher,"I stopped the video","I didn't stop the video. Try again please",response)
        elif control=="reset":
            print("Trying to reset the video/audio...")
            response = my_graphQL.reset()
            self.process_response(dispatcher,"I reset the video","I didn't reset the video. Try again please",response)
        elif control=="play loop":
            print("Trying to play loop the video/audio...")
            response = my_graphQL.play_loop()
            self.process_response(dispatcher,"I played loop the video","I didn't play loop the video. Try again please",response)
        elif control=="refresh":
            print("Trying to refresh the webpage...")
            response = my_graphQL.refresh()
            self.process_response(dispatcher,"I refreshed the page","I didn't refresh the page. Try again please",response)


        return [SlotSet("control_command",None)]

class ActionSearch(Action):
    """A class used to search a demo"""

    def name(self) -> Text:
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""

        return "action_search"

    def demo_contains_tag(self,tag, available_demos):
        """Function that indicates if one of the demo contains a tag and returns all demos containing the tag

        Parameters:
        tag (String): The tag
        available_demos (List[String]): The list of available demos in the current environments

        Returns:
        [Boolean, List[String]]: The booleand and the list of found demos"""

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
        """Function that manages the robot's behavior to search a demo.

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        tag = tracker.get_slot("demo")

        try:
            my_graphQL = GraphQL()
        except Exception as e:
            dispatcher.utter_message(text="I'm sorry, something went wrong. {}".format(e))
            print(e)
            return []

        available_demos = None

        if my_graphQL.environment_is_opened():
            available_demos = GraphQL.get_projects()

        if available_demos == None:
            dispatcher.utter_message(text="First, open an environment please")
        elif tag == None:
            dispatcher.utter_message(text="I'm sorry, there is no demo on this topic")
        else:
            dispatcher.utter_message(text="Reading demos...")
            available_demos_names = available_demos.values()
            result_search = self.demo_contains_tag(tag.lower(),available_demos_names)
            #if something corresponds to the tag
            if result_search[0]:
                ids_demos_tag =result_search[1]
                if len(ids_demos_tag)<=10:
                    dispatcher.utter_message("Results for "+str(tracker.get_slot("demo"))+" : "+", ".join(ids_demos_tag))
                else:
                    dispatcher.utter_message(text="The list of demos is too long to read out. Would you like to refine it by other tags?")
            else:
                dispatcher.utter_message(text="I'm sorry, there is no demo on this topic")

        my_graphQL.client.close()

        return [SlotSet("demo",None)]


class ActionClearSpace(Action):
    """A class used to clear the space"""

    def name(self) -> Text:
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""

        return "action_clear_space"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Function that manages the robot's behavior to clear the space.

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        try:
            my_graphQL = GraphQL()
        except Exception as e:
            dispatcher.utter_message(text="I'm sorry, something went wrong. {}".format(e))
            print(e)
            return []

        response = my_graphQL.clear_screen()

        print("Trying to clear the space...")
        if response['success']:
            dispatcher.utter_message("The space is cleaned")
            print("Clear space done ;)")
        else:
            dispatcher.utter_message(text="I'm sorry, something went wrong. I can't clear the screens. {}".format(response['message']))
            print(response['message'])

        my_graphQL.client.close()

        return []

class ActionSwitchMode(Action):
    """A class used to switch the mode"""

    def name(self) -> Text:
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""

        return "action_switch_modes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Function that manages the robot's behavior to switch the mode.

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        try:
            my_graphQL = GraphQL()
        except Exception as e:
            dispatcher.utter_message(text="I'm sorry, something went wrong. {}".format(e))
            print(e)
            return []

        response = my_graphQL.switch_mode(tracker.get_slot('mode'),tracker.get_slot('switch_action'))
        print("Switch mode action in process...")
        if response['success']:
            dispatcher.utter_message(text=response['message'])
            print(response['message'])
        else:
            dispatcher.utter_message(text="I'm sorry, I can't do that. {}".format(response['message']))
            print("Fail :(")

        my_graphQL.client.close()
        return [SlotSet("mode",None),SlotSet("switch_action",None)]

class ActionOpenEnvironment(Action):
    """A class used to open an environment"""

    def name(self) -> Text:
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""

        return "action_open_environment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Function that manages the robot's behavior to open an environment.

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        try:
            my_graphQL = GraphQL()
        except Exception as e:
            dispatcher.utter_message(text="I'm sorry, something went wrong. {}".format(e))
            print(e)
            return []

        environment = tracker.get_slot('work_environment')

        response = my_graphQL.open_environment_action(environment)
        print("Open environment action in process...")
        if response['success']:
            dispatcher.utter_message(text=response['message'])
            print("Successfully accomplished :)")
        else:
            dispatcher.utter_message(text="I'm sorry, something went wrong. {}".format(response['message']))
            print(reponse['message'])

        my_graphQL.client.close()
        return [SlotSet("work_environment",None)]

class ActionHelp(Action):
    """A class used to give information"""

    def name(self) -> Text:
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""
        return "action_help"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Function that manages the robot's behavior to give help information.

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        dispatcher.utter_message(text="I can execute the following commands :")
        dispatcher.utter_message(text="Open demo")
        dispatcher.utter_message(text="Show me something on tag")
        dispatcher.utter_message(text="Launch demo")
        dispatcher.utter_message(text="Activate demo")
        dispatcher.utter_message(text="Shutdown screens")
        dispatcher.utter_message(text="Do a clearspace")
        dispatcher.utter_message(text="Refresh the screens")
        dispatcher.utter_message(text="Pause the video/the audio")
        dispatcher.utter_message(text="Play video")
        dispatcher.utter_message(text="Start animation")
        dispatcher.utter_message(text="Stop animation")
        dispatcher.utter_message(text="Quit video/audio")
        dispatcher.utter_message(text="Mute video/audio")
        dispatcher.utter_message(text="Full black screens")
        dispatcher.utter_message(text="Open environment")
        dispatcher.utter_message(text="Switch mode")
        dispatcher.utter_message(text="Turn on the Global Data Observatory")
        dispatcher.utter_message(text="Shutdown the Global Data Observatory")
        dispatcher.utter_message(text="Open/Close/Reset browsers")

        return []

class ActionResetSlot(Action):
    """A class used to reset slots"""

    def name(self):
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""

        return "action_reset_slot"

    def run(self, dispatcher, tracker, domain):
        """Function that resets slots.

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        return [SlotSet("demo", None), SlotSet("demo_name",None)]

class ActionOpenBrowsers(Action):
    """A class used to open browsers"""

    def name(self):
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""

        return "action_open_browsers"

    def run(self, dispatcher, tracker, domain):
        """Function that manages the robot's behavior to open browsers.

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        try:
            my_graphQL = GraphQL()
        except Exception as e:
            print(e)
            dispatcher.utter_message(text="I'm sorry, something went wrong. {}".format(e))
            return []

        response = my_graphQL.open_browsers();
        print("Trying to open browsers...")
        if response['success'] and response["executeHwAction"]=="done":
            dispatcher.utter_message(text="The browsers are open")
            print("Browsers are open ;)")
        elif response['success']:
            dispatcher.utter_message(text="Something went wrong. Do you want me to try again ?")
            print("Fail :(")
        else:
            dispatcher.utter_message(text="I'm sorry, something went wrong. {}".format(response['message']))
            print(response['message'])

        my_graphQL.client.close()
        return []

class ActionCloseBrowsers(Action):
    """A class used to close browsers"""

    def name(self):
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""

        return "action_close_browsers"

    def run(self, dispatcher, tracker, domain):
        """Function that manages the robot's behavior to close browsers.

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        try:
            my_graphQL = GraphQL()
        except Exception as e:
            dispatcher.utter_message(text="I'm sorry, something went wrong. {}".format(e))
            print(e)
            return []

        response = my_graphQL.close_browsers();
        print("Trying to close browsers...")
        if response['success'] and response["executeHwAction"]=="done":
            dispatcher.utter_message(text="The browsers are close")
            print("Browsers are close ;)")
        elif response['success']:
            dispatcher.utter_message(text="Something went wrong. Do you want me to try again ?")
            print("Fail :(")
        else:
            dispatcher.utter_message(text="I'm sorry, something went wrong. {}".format(response['message']))
            print(response['message'])

        my_graphQL.client.close()
        return []

class ActionRefreshBrowsers(Action):
    """A class used to refresh browsers"""

    def name(self):
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""

        return "action_refresh_browsers"

    def run(self, dispatcher, tracker, domain):
        """Function that manages the robot's behavior to refresh browsers.

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        try:
            my_graphQL = GraphQL()
        except Exception as e:
            dispatcher.utter_message(text="I'm sorry, something went wrong. {}".format(e))
            print(e)
            return []

        response = my_graphQL.refresh_browsers();
        print("Trying to refresh browsers...")
        if response['success'] and response["executeHwAction"]=="done":
            dispatcher.utter_message(text="The browsers are reset")
            print("Browsers are reset ;)")
        elif response['success']:
            dispatcher.utter_message(text="Something went wrong. Do you want me to try again ?")
            print("Fail :(")
        else:
            dispatcher.utter_message(text="I'm sorry, something went wrong. {}".format(response['message']))
            print(response['message'])

        my_graphQL.client.close()
        return []

class ActionRepeat(Action):
    """A class used to repeat the last bot answer"""

    def name(self):
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""
        return "action_repeat"

    def run(self, dispatcher, tracker, domain):
        """Function that repeats the last utter_message.

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""
        print('Trying to repeat')
        if len(tracker.events) >= 3:
                dispatcher.utter_message(tracker.events[-3].get('text'))

        return []

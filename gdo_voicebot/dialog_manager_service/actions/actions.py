# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ReminderScheduled
# import datetime
# from datetime import timedelta
from functools import lru_cache
from utilities.utils_graphql import GraphQL
from utilities.utils_actions import *

try:
    print('Connection to graphql')
    my_graphQL = GraphQL('./config/config.yml')
except Exception as e:
    raise e
    print(e)

class ActionRespondAboutToday(Action):

    def name(self) -> Text:
        return "action_respond_about_today"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        emotion = tracker.get_slot("emotion")
        if emotion == "n/a" or emotion == "neutral":
            dispatcher.utter_message(text="I see. Well, I'm glad you made it to the Data Observatory.")
        elif emotion == "excited":
            dispatcher.utter_message(text="Wow, you have a great energy! I need to keep it up!")
        elif emotion == "sleepy":
            dispatcher.utter_message(text="Hmm... You sound a bit tired.")
        elif emotion == "happy":
            dispatcher.utter_message(text="I like listening to you. You have a happy presence.")
        elif emotion == "relaxed":
            dispatcher.utter_message(text="You seem pretty relaxed.")
        elif emotion == "frustrated":
            dispatcher.utter_message(text="I understand your frustration. What can I do for you?")
        elif emotion == "sad":
            dispatcher.utter_message(text="You seem sad... What can I do to cheer you up?")
        elif emotion == "mixed":
            dispatcher.utter_message(text="Are you alright? You seem a little off...")

        return []
class ActionTurnOnEmotionDetection(Action):

    def name(self) -> Text:
        return "action_turn_on_emotion_detection"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Emotion detection has been turned on.")
        return [SlotSet("emotion_detection_enabled", True)]

class ActionTurnOffEmotionDetection(Action):

    def name(self) -> Text:
        return "action_turn_off_emotion_detection"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Emotion detection has been turned off.")
        # When turning of emotion detection, reset the current emotion to n/a
        return [SlotSet("emotion_detection_enabled", False), SlotSet("emotion", "n/a")]
class ActionCheckEmotionDetectionEnabled(Action):

    def name(self) -> Text:
        return "action_check_emotion_detection_enabled"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        emotion_detection_enabled = tracker.get_slot("emotion_detection_enabled")
        if emotion_detection_enabled:
            dispatcher.utter_message(text="Emotion detection is currently enabled")
        else:
            dispatcher.utter_message(text="Emotion detection is currently disabled")
        
        return []
class ActionReceiveName(Action):

    def name(self) -> Text:
        return "action_receive_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        text = tracker.latest_message['text']
        dispatcher.utter_message(text=f"I'll remember your name {text}!")
        return [SlotSet("name", text)]


class ActionSayName(Action):

    def name(self) -> Text:
        return "action_say_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")
        if not name:
            dispatcher.utter_message(text="I don't know your name.")
        else:
            dispatcher.utter_message(text=f"Your name is {name}!")
        return []
         
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


        response = action_launch_project(my_graphQL,tracker.get_slot('demo'))

        print('Trying to launch a project')
        if response['success']:
            dispatcher.utter_message(text=response['message'])
            print('Success :)')
            if not response['list']:
                return [SlotSet('demo',response['project']),SlotSet('read_list',False),SlotSet('restart',False)]
            else:
                return [SlotSet('read_list',True),SlotSet('restart',False)]
        else:
            dispatcher.utter_message(text="I'm sorry, something went wrong. {}".format(response['message']))
            dispatcher.utter_message(text="Should I try again ?")
            print(response['message'])
            return [SlotSet('read_list',False),SlotSet('restart',True)]


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


        robot_last_message = ""
        if len(tracker.events) >= 3:
            robot_last_message = tracker.events[-3].get('text')

        print("Trying to get available demos...")
        response = action_list_demos(my_graphQL,robot_last_message)
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

        response = action_turn_off_gdo(my_graphQL)

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

        return []

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

        response = action_turn_on_gdo(my_graphQL)

        print("Trying to turn on the GDO...")
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

        control = tracker.get_slot("control_command")

        #If the control command is not recognized, we inform the user
        if control == None:
            dispatcher.utter_message("Sorry I didn't get the command")
            return [SlotSet("control_command",None)]
        else:
            control = control.lower()

        if control=="play":
            print("Trying to play the video/audio...")
            response = action_play(my_graphQL)
            self.process_response(dispatcher,"I'm playing the video","I didn't start playing the video. Try again please",response)
        elif control=="pause":
            print("Trying to pause the video/audio...")
            response = action_pause(my_graphQL)
            self.process_response(dispatcher,"I paused the video","I didn't pause the video. Try again please",response)
        elif control=="stop":
            print("Trying to stop the video/audio...")
            response = action_stop(my_graphQL)
            self.process_response(dispatcher,"I stopped the video","I didn't stop the video. Try again please",response)
        elif control=="reset":
            print("Trying to reset the video/audio...")
            response = action_reset(my_graphQL)
            self.process_response(dispatcher,"I reset the video","I didn't reset the video. Try again please",response)
        elif control=="play loop":
            print("Trying to play loop the video/audio...")
            response = action_play_loop(my_graphQL)
            self.process_response(dispatcher,"I played loop the video","I didn't play loop the video. Try again please",response)
        elif control=="refresh":
            print("Trying to refresh the webpage...")
            response = action_refresh(my_graphQL)
            self.process_response(dispatcher,"I refreshed the page","I didn't refresh the page. Try again please",response)

        return [SlotSet("control_command",None)]

class ActionSearch(Action):
    """A class used to search a demo"""

    def name(self) -> Text:
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""

        return "action_search"

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

        tag = tracker.get_slot("tag")
        key_word = tracker.get_slot("demo")
        search_mode = tracker.get_slot("search_mode")

        if search_mode == None:
            search_mode = ""


        result = action_search(my_graphQL,key_word,tag,search_mode)
        print("Trying to execute search action...")

        if result['success']:
            dispatcher.utter_message(text=result['message'])
            print("Success :)")
        else:
            dispatcher.utter_message(text="I'm sorry, something went wrong. {}".format(result['message']))
            dispatcher.utter_message(text="Do you want me to try again ?")
            print('Fail :(')
            return []

        return [SlotSet("demo",None),SlotSet("tag",None),SlotSet("search_mode",None)]


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

        response = action_clear_space(my_graphQL)

        print("Trying to clear the space...")
        if response['success']:
            dispatcher.utter_message("The space is clear")
            print("Clear space done ;)")
        else:
            dispatcher.utter_message(text="I'm sorry, something went wrong. I can't clear the screens. {}".format(response['message']))
            print(response['message'])

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

        mode = my_graphQL,tracker.get_slot('mode')
        if mode!=None and 'section' in mode:
            mode = 'section'
        elif mode!=None and 'cluster' in mode:
            mode = 'cluster'
        response = action_switch_mode(my_graphQL,mode,tracker.get_slot('switch_action'))
        print("Switch mode action in process...")
        if response['success']:
            dispatcher.utter_message(text=response['message'])
            print(response['message'])
        else:
            dispatcher.utter_message(text="I'm sorry, I can't do that. {}".format(response['message']))
            print("Fail :(")

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

        environment = tracker.get_slot('work_environment')
        if environment!=None and 'student' in environment:
            environment = 'students'

        response = action_open_environment(my_graphQL,environment)
        print("Open environment action in process...")
        if response['success']:
            dispatcher.utter_message(text=response['message'])
            print("Successfully accomplished :)")
        else:
            dispatcher.utter_message(text="I'm sorry, something went wrong. {}".format(response['message']))
            print(reponse['message'])

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
        """Function that manages the robot's behaviour to give help information.

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        dispatcher.utter_message(text="I can execute the following commands :")
        dispatcher.utter_message(text="Open/Launch/Start demo")
        dispatcher.utter_message(text="Close demo")
        dispatcher.utter_message(text="Show me something on tag/key word")
        dispatcher.utter_message(text="Launch demo")
        dispatcher.utter_message(text="Activate demo")
        dispatcher.utter_message(text="Shutdown screens")
        dispatcher.utter_message(text="Do a clearspace")
        dispatcher.utter_message(text="Refresh the screens")
        dispatcher.utter_message(text="Play/Pause/Stop/Reset/Play loop videos")
        dispatcher.utter_message(text="Full black screens")
        dispatcher.utter_message(text="Open environment")
        dispatcher.utter_message(text="Switch mode")
        dispatcher.utter_message(text="Turn on the Global Data Observatory")
        dispatcher.utter_message(text="Shutdown the Global Data Observatory")
        dispatcher.utter_message(text="Open/Close/Reset browsers")
        dispatcher.utter_message(text="Zoom in or zoom out a bit, a lot, moderately")
        dispatcher.utter_message(text="Move up/down/right/left on a map")

        return []

class ActionResetSlotOpenDemo(Action):
    """A class used to reset slots"""

    def name(self):
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""

        return "action_reset_slot_open"

    def run(self, dispatcher, tracker, domain):
        """Function that resets slots.

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        return [SlotSet("demo", None),SlotSet("read_list",False),SlotSet('restart',False)]

class ActionResetSlotSearch(Action):
    """A class used to reset slots"""

    def name(self):
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""

        return "action_reset_slot_search"

    def run(self, dispatcher, tracker, domain):
        """Function that resets slots.

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        return [SlotSet("demo",None),SlotSet("tag",None),SlotSet("search_mode",None)]

class ActionResetSlotZoom(Action):
    """A class used to reset slots"""

    def name(self):
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""

        return "action_reset_slot_zoom"

    def run(self, dispatcher, tracker, domain):
        """Function that resets slots.

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        return [SlotSet('zoom_action',None),SlotSet('zoom_big_level',None),SlotSet('zoom_small_level',None)]

class ActionResetSlotDirection(Action):
    """A class used to reset slots"""

    def name(self):
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""

        return "action_reset_slot_direction"

    def run(self, dispatcher, tracker, domain):
        """Function that resets slots.

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        return [SlotSet('direction',None)]

class ActionResetSlotBrowsers(Action):
    """A class used to reset slots"""

    def name(self):
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""

        return "action_reset_slot_browsers"

    def run(self, dispatcher, tracker, domain):
        """Function that resets slots.

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        return [SlotSet('open_browsers',None),SlotSet('close_browsers',None),SlotSet('reset_browsers',None)]

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

        response = action_browsers(my_graphQL,"open")

        print("Trying to open browsers...")
        if response['success'] and response["executeHwAction"]=="done":
            dispatcher.utter_message(text="The browsers are open")
            print("Browsers are open ;)")
        elif response['success']:
            dispatcher.utter_message(text="Something went wrong. Do you want me to try again ?")
            print("Fail :(")
            return []
        else:
            dispatcher.utter_message(text="I'm sorry, something went wrong. {}".format(response['message']))
            print(response['message'])

        return [SlotSet('open_browsers'),None]


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

        response = action_browsers(my_graphQL,"kill")

        print("Trying to close browsers...")
        if response['success'] and response["executeHwAction"]=="done":
            dispatcher.utter_message(text="The browsers are close")
            print("Browsers are close ;)")
        elif response['success']:
            dispatcher.utter_message(text="Something went wrong. Do you want me to try again ?")
            print("Fail :(")
            return []
        else:
            dispatcher.utter_message(text="I'm sorry, something went wrong. {}".format(response['message']))
            print(response['message'])

        return [SlotSet('close_browsers',None)]

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

        response = action_browsers(my_graphQL,"refresh")

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

        return [SlotSet('reset_browsers',None)]

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

class ActionZoom(Action):
    """A class used to zoom in or zoom out"""

    def name(self):
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""
        return "action_zoom"

    def run(self, dispatcher, tracker, domain):
        """Function that runs zoom-in or zoom-out commands

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        zoom_action = tracker.get_slot('zoom_action')
        zoom_small_level = tracker.get_slot('zoom_small_level')
        zoom_big_level = tracker.get_slot('zoom_big_level')

        print('Trying to execute zoom action')
        if zoom_small_level == None and zoom_big_level == None:
            response = action_zoom(my_graphQL,zoom_action)
        elif zoom_small_level == None:
            response = action_zoom(my_graphQL,zoom_action,'big')
        else:
            response = action_zoom(my_graphQL,zoom_action,'small')

        if response['success'] and response['message'] =='done':
            dispatcher.utter_message(text="It's done !")
            print('Zoom action successfully done :)')
            return [SlotSet('zoom_action',None),SlotSet('zoom_big_level',None),SlotSet('zoom_small_level',None)]
        elif response['success']:
            dispatcher.utter_message(text=response['message'])
            return [SlotSet('zoom_action',None)]
        else :
            dispatcher.utter_message(text="I'm sorry. I didn't manage to do it. {}. Should I try again ?".format(response['message']))
            print('Did not manage to do it :(')
            return []

class ActionMove(Action):
    """A class used to move on maps"""

    def name(self):
        """Function that returns the name of the action

        Returns:
        Text:The name of the action"""
        return "action_move"

    def run(self, dispatcher, tracker, domain):
        """Function that runs zoom-in or zoom-out commands

        Parameters:
        dispatcher (CollectingDispatcher): The dispatcher which is used to send messages back to the user. Use dispatcher.utter_message() for sending messages.
        tracker (Tracker): The state tracker for the current user. You can access slot values using tracker.get_slot(slot_name), the most recent user message is tracker.latest_message.text and any other rasa_sdk.Tracker property.
        domain (Dict[Text, Any]): The bot’s domain

        Returns:
        List[Dict[Text, Any]]: A dictionary of rasa_sdk.events.Event instances that is returned through the endpoint List[Dict[str, Any]]"""

        direction = tracker.get_slot('direction')
        response = action_move(my_graphQL,direction)

        if response['success'] and response['message'] == 'done':
            dispatcher.utter_message(text="It's done !")
            print('Move action successfully done :)')
            return [SlotSet('direction',None)]
        elif response['success']:
            dispatcher.utter_message(text=response['message'])
        else:
            dispatcher.utter_message(text="I'm sorry. I didn't manage to do it. {}. Should I try again ?".format(response['message']))
            print('Did not manage to do it :(')
        return []

# TODO : Reminder
# class ActionSetReminder(Action):
#     """Schedules a reminder, supplied with the last message's entities."""
#
#     def name(self) -> Text:
#         return "action_set_reminder"
#
#     async def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message("I will remind you in 10 seconds.")
#
#         date = datetime.datetime.now() + datetime.timedelta(seconds=10)
#         entities = tracker.latest_message.get("entities")
#
#         reminder = ReminderScheduled(
#             "EXTERNAL_reminder",
#             trigger_date_time=date,
#             entities=entities,
#             name="my_reminder",
#             kill_on_user_message=False,
#         )
#
# class ActionReactToReminder(Action):
#     """Reminds the user to finish presentation."""
#
#     def name(self) -> Text:
#         return "action_react_to_reminder"
#
#     async def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message("The meeting is finished !")
#
#         return []

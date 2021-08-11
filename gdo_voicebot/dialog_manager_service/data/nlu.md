## intent:greet
- hey
- hello
- hi
- good morning
- good evening
- good afternoon
- hey there

## intent:affirm
- yes
- indeed
- of course
- that sounds good
- correct
- confirm
- sure

## intent:deny
- no
- never
- I don't think so
- don't like that
- no way
- not really
- no I've changed my mind

## intent:goodbye
- bye
- goodbye
- see you around
- see you later
- see you
- good bye

## intent:help
- help please
- I need help
- Could you help me
- I want to ask you something
- request
- I need your support
- support

## intent:open  
- Open [dsi intro](demo)
- I would like to open [gaze](demo)
- open [amr](demo)
- launch [defra](demo)
- activate [An open bucket new works](demo)
- start [davidtest](demo)
- open [Mars selfies](demo)
- [bitcoin](demo)
- load [map of london](demo) please
- [twitter](demo)
- launch [london cycling map](demo)
- open [cycling map](demo) please
- Start [anotherthest](demo)
- I'd like to start [airesearch](demo)
- Could you activate the [test](demo) ?
- Open [DataSparks 2020 Project Luna](demo)
- I'd like to launch the [datest](demo)
- activate [dsi-international](demo)

## intent:out_of_scope
- I want to order food
- What is 2 + 2?
- Who's the US President?
- I need a job
- I want to dance !
- What's the day of birth of Julius Caesar ?
- What's the weather today ?
- what's in the movies
- when are the next Olympics

## intent:search
- Look for [wifi](tag)
- Look for [ml](tag)
- Look for [nlp](tag)
- Look for [politics](tag)
- Look for [twitter](tag)
- Look for [scivis](tag)
- Look for [astronomy](tag)
- Look for [mars](tag)
- Look for [ove-feature-showcase](tag)
- Look for [air-pollution](tag)
- Look for [transport](tag)
- Look for [datasparks](tag)
- Look for [cybersecurity](tag)
- Look for [privacy](tag)
- Look for [medical-imaging](tag)
- Look for [imagetiles](tag)
- Look for [healthcare](tag)
- Look for [ai](tag)
- Show me something on [network](tag)
- Can you show me something on [the data science institute](tag)
- Search [business](tag)
- search demo please
- I'd like to search something on [cryptocurrency](tag)
- I would like to search by [tags](search_mode)
- Make a search by [key words](search_mode)
- Search by [tag](search_mode)
- Look for by [key word](search_mode)

## intent:shutdown
- Shut down screens
- Turn out screens please
- Could you shutdown the Screens ?
- I'd like to shutdown the Screens
- Screens shutdown please
- Shut down GDO
- Turn off the GDO
- Can you turn off the screens
- Could you shutdown the global data observatory

## intent:turn_on_gdo
- Turn on the gdo
- Could you turn on the screens
- I'd like to turn on the Global Data Observatory
- Start the gdo please
- Can you turn on the gdo
- Turn on the screens
- I'd like to start the Global Data Observatory
- I would like to turn on the screens please

## intent:clear_space
- Clear the screens
- clean the space
- clear space
- Close current project
- Could you close the loaded demo
- Close demo please
- I'd like to close the project
- Close project
- I'd like to clean the space
- Could you clear the space please
- full black
- I would like black screens
- Display black screens
- I only want black screens
- I want a black background


## intent:control
- [Play](control_command) the video
- [play](control_command) the audio
- [Pause](control_command) please
- I would like to [pause](control_command) the video
- I want to [stop](control_command) the audio file
- [Stop](control_command) it
- Could you [mute](control_command) the video please
- I'd like to [refresh](control_command) the screen
- [Play loop](control_command) the video
- Can you [play loop](control_command) the music
- [Reset](control_command) the video
- Could you [reset](control_command) the video

## intent:switch_modes
- I'd like to switch the mode
- [switch](switch_action) the mode
- Mode [cluster](mode)
- mode [section](mode)
- Select [section](mode)
- Could you select [cluster](mode) please
- The [section](mode) mode would be fine
- I would like to take the [section](mode)
- I choose [cluster](mode) please
- [change]{"entity":"switch_action","value":"switch"} the mode
- [reverse]{"entity":"switch_action","value":"switch"} modes
- [permute]{"entity":"switch_action","value":"switch"} modes
- [swap]{"entity":"switch_action","value":"switch"} modes
- What's the current mode

## intent:open_environment
- Open [students](work_environment) environment
- Go to [production](work_environment) environment
- Show me available environments please
- List of available environments
- Select [development](work_environment) environment please
- Could you open the [production](work_environment)
- I'd like to go on the [students](work_environment)
- What's the current environment

## intent:open_browsers
- [Open browsers](open_browsers)
- Could you [open the browsers](open_browsers) please
- I want to [open the browsers](open_browsers)
- I'd like to [open the browsers](open_browsers)
- I would like to [open browsers](open_browsers) please

## intent:close_browsers
- [Close browsers](close_browsers) please
- Could you [close the browsers](close_browsers)
- I want to [close the browsers](close_browsers)
- I'd like to [close the browsers](close_browsers)
- I would like to [close browsers](close_browsers) please

## intent:refresh_browsers
- [Reset browsers](reset_browsers)
- Could you [reset the browsers](reset_browsers)
- I want to [reset the browsers](reset_browsers) please
- I'd like to [reset the browsers](reset_browsers)
- I would like to [reset browsers](reset_browsers) please

## intent:ask_repeat
- repeat
- Could you repeat
- Say it again please
- I'd like you to repeat
- What did you say please

## intent:list_available_demos
- Give me the list of available demos
- Show me all the projects please
- Available demos
- What's the list of available environments
- Available projects

## intent:zoom
- I'd like to zoom [in](zoom_action) [a little](zoom_small_level)
- Could you zoom [out](zoom_action) [a lot](zoom_big_level)
- Zoom [in](zoom_action)
- Zoom [out](zoom_action) please
- Can you zoom [in](zoom_action) [a bit](zoom_small_level)
- I want to zoom [out](zoom_action) [hard](zoom_big_level)
- Make a [big](zoom_big_level) zoom [in](zoom_action)
- Do a [small](zoom_small_level)
- make a [large](zoom_small_level)

## intent:move
- Move [up](direction)
- Can you go [down](direction)
- Could you move to the [left](direction)
- Go [up](direction)
- I want you to move to your [right](direction)
- Move
- I'd like to see the [top](direction) of the map
- Show me the [bottom](direction) of the image

<!-- #toDo : Reminder action -->
<!-- ## intent:ask_remind_end_of_meeting
- remind me when my meeting ends
- Could you remind me when my meeting ends
- remind me to sop my meeting
- remind me when the presentation should end
- I have to finish my presentation -->

## intent:start_small_talk
- i want to talk to you
- let's have a chat
- let's talk
- do you want to have a conversation?
- i want to have a conversation
- can we chat?

## intent:check_emotion_detection_enabled
- is emotion detection enabled?
- is emotion detection on?
- are you currently detecting emotion?
- is emotion recognition turned on?
- are you studying my emotion right now?
- have you turned off emotion recognition?
## intent:want_to_give_name
- i want to tell you my name
- Can you learn my name?
- ill give you my name
- remember my name

## intent:repeat_name
- do you know my name?
- repeat my name
- name of the current speaker
- who is the current speaker

## intent:give_name
- ovidiu
- aurelie
- mifu
- samuel
- amy

## intent:tell_about_today
- today i've been running errands and being busy
- today i had a video call with my family
- today i went to school
- i've not done much today
- nothing interesting
- i went to skate boarding with my friends
- i've been studying all day

## intent:ask_current_emotion
- what is my current emotion?
- can you tell me what my emotion is?
- what am i feeling?
- current emotion
- emotion right now

## intent:turn_on_emotion_detection
- start emotion detection
- turn sentiment recognition on
- turn on emotion detection
- recognise emotion
- enable emotion detection

## intent:turn_off_emotion_detection
- stop emotion detection
- turn sentiment recognition off
- turn off emotion detection
- stop emotion recognition
- disable emotion detection

#### This file contains tests to evaluate that your bot behaves as expected.
#### If you want to learn more, please see the docs: https://rasa.com/docs/rasa/user-guide/testing-your-assistant/

## welcome and asking for help 1
* greet: hello there!
  - utter_greet
* affirm: yes, indeed !
  - utter_help

## welcome and asking for help 2
* greet: good afternoon
  - utter_greet
* affirm: yes, indeed !
  - utter_help

## welcome and no help needed 1
* greet: hi there
  - utter_greet
* deny: no thank you
  - utter_goodbye

## welcome and no help needed 2
* greet: good morning
  - utter_greet
* deny: never
  - utter_goodbye

## quit 1
* goodbye: See you !
  - utter_goodbye

## quit 2
* goodbye: Bye
  - utter_goodbye

## help 1
* help: I've got a request for you
  - utter_help

## help 2
* help: Some support please
  - utter_help

## open success 1
* open: Please, launch the [airesearch](demo).
  - action_open

## open success 2
* open: Activate the [defra](demo) !
  - action_open

## out_of_scope 1
* out_of_scope: give the name of the French President ?
  - utter_out_of_scope

## out_of_scope 2
* out_of_scope: What time is it ?
  - utter_out_of_scope

## open fail and list 1
* open: I would like to start [Mars selfies](demo)
  - action_open
* affirm: Yes that sounds good
  - action_list_demos

## open fail and list 2
* open: open [london cycling map](demo)
  - action_open
* affirm: perfect sounds good
  - action_list_demos

## open fail 1
* open: activate montblanc
  - action_open
* deny: no thank you
  - utter_affirm

## open fail 2
* open: [bitcoin](demo)
  - action_open
* deny: no that's OK
  - utter_affirm

## open fail and restart 1
* open: Start [amr](demo)
  - action_open
* new_try: Yes, restart
  - action_open

## search 1
* search: Show me something on [mars](demo)
  - action_search

## search 2
* search: Can you show me something on [twitter](demo)
  - action_search
* affirm: yes please
  - utter_ask_new_search

## search 3
* search: Search something on [bitcoin](demo)
  - action_search
* deny: no
  - utter_affirm

## search 3
* search: Search something on pollution
  - action_search
* new_try: yes restart
  - action_search

## shutdown confirm 1
* shutdown: please, could you shutdown the screens ?
  - utter_confirm_shutdown
* affirm: yes
  - action_shutdown

## shutdown confirm 2
* shutdown: turn out screens
  - utter_confirm_shutdown
* affirm: of course
  - action_shutdown

## shutdown cancel 1
* shutdown: shutdown screens ?
  - utter_confirm_shutdown
* deny: no I've changed my mind
  - utter_affirm

## shutdown cancel 2
* shutdown: shutdown ?
  - utter_confirm_shutdown
* deny: no thanks
  - utter_affirm

## uniform screens 1
* uniform_background: Show me full [white](color) screens please
 - action_uniform_screens

## uniform screens 2
* uniform_background: Can I see a [black](color) background
- action_uniform_screens

## control pause
* control: I want to [pause](control_command) the video please
- action_control

## control stop
* control: [Stop](control_command) the music
- action_control

## control play
* control: Could you [play](control_command) the song please ?
- action_control

## control refresh
* control: I would like to [refresh](control_command) the webpage
- action_control

## control mute
* control: [Mute](control_command) this audio file
- action_control

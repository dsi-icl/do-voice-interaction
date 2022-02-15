#### This file contains tests to evaluate that your bot behaves as expected.
#### If you want to learn more, please see the docs: https://rasa.com/docs/rasa/user-guide/testing-your-assistant/

## welcome and asking for help 1
* greet: hello there!
  - utter_greet
* affirm: yes, indeed !
  - action_help

## welcome and asking for help 2
* greet: good afternoon
  - utter_greet
* affirm: yes, indeed !
  - action_help

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
* help: Help me
  - action_help

## help 2
* help: Some support please
  - action_help

## open success 1
* open: Please, launch the [airesearch](demo).
  - action_open
  - slot{"demo": null,"read_list":false,"restart":false}

## open success 2
* open: Activate the [defra](demo) !
  - action_open
  - slot{"demo": null,"read_list":false,"restart":false}

## out_of_scope 1
* out_of_scope: give the name of the French President ?
  - utter_out_of_scope

## out_of_scope 2
* out_of_scope: When it's your birthday ?
  - utter_out_of_scope

## open fail and list 1
* open: I would like to start [Mars selfies](demo)
  - action_open
  - slot{"read_list":true,"restart":false}
* affirm: Yes that sounds good
  - action_reset_slot_open
  - slot{"demo": null,"read_list":false,"restart":false}
  - action_list_demos

## open fail and restart
* open: open [london cycling map](demo)
  - action_open
  - slot{"read_list":false,"restart":true}
* affirm: perfect sounds good
  - action_open

## open fail 1
* open: activate montblanc
  - action_open
  - slot{"read_list":true,"restart":false}
* deny: no thank you
  - utter_affirm
  - action_reset_slot_open
  - slot{"demo": null,"read_list":false,"restart":false}

## open fail 2
* open: [bitcoin](demo)
  - action_open
  - slot{"read_list":false,"restart":true}
* deny: no that's OK
  - utter_affirm
  - action_reset_slot_open
  - slot{"demo": null,"read_list":false,"restart":false}

## search 1
* search: Show me something on [mars](tag)
  - action_search

## search 2
* search: Can you show me something on [twitter](tag)
  - action_search
* affirm: yes please
  - action_search

## search 3
* search: Search something on [bitcoin](demo)
  - action_search
* deny: no
  - utter_affirm
  - action_reset_slot_search

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

## shutdown confirm and fail, restart
* shutdown: Shut down the screens please
  - utter_confirm_shutdown
* affirm: Yes I confirm
  - action_shutdown
* affirm: yes
  - action_shutdown

## shutdown confirm and fail, give up
* shutdown: Shut down gdo
  - utter_confirm_shutdown
* affirm: Indeed
  - action_shutdown
* deny: No
  - utter_affirm

## control pause
* control: I want to [pause](control_command) the video please
- action_control

## control stop
* control: [Stop](control_command) the music
- action_control

## control play
* control: [play](control_command) the song
- action_control

## control refresh
* control: I would like to [refresh](control_command) the webpage
- action_control

## control mute
* control: [Mute](control_command) this audio file
- action_control

## clear space 1
* clear_space: I would like to clean the screens
- action_clear_space

## clear space 2
* clear_space: Please clear the space
- action_clear_space

## turn on gdo, confirm 1
* turn_on_gdo: Turn on the global data observatory, please
  - utter_confirm_turn_on_gdo
* affirm: yes I confirm
  - action_turn_on_gdo

## turn on gdo, cancel 1
* turn_on_gdo: Could you turn on the screens
  - utter_confirm_turn_on_gdo
* deny: no
  - utter_affirm

## turn on gdo, confirm, restart 1
* turn_on_gdo: I'd like to turn on the global data observatory
  - utter_confirm_turn_on_gdo
* affirm: Yes
  - action_turn_on_gdo
* affirm: Yes, please
  - action_turn_on_gdo

## turn on gdo, confirm, without restart 1
* turn_on_gdo: Please, I would like to turn on the screens
  - utter_confirm_turn_on_gdo
* affirm: Yes
  - action_turn_on_gdo
* deny: No

# switch modes 1
* switch_modes: Mode [cluster](mode)
  - action_switch_modes

# switch modes 2
* switch_modes: I'd like to [change]{"entity":"switch_action","value":"switch"} the mode
  - action_switch_modes

# switch modes 2
* switch_modes: Please could you [switch](switch_action) [cluster](mode) to [section](mode) ?
  - action_switch_modes

# open environment 1
* open_environment: Show me the current environment
  - action_open_environment

# open environment 2
* open_environment: Open [development](work_environment)
  - action_open_environment

# open environment 3
* open_environment: What are the available environments ?
  - action_open_environment

# open browsers 1
* open_browsers: [Open browsers](open_browsers)
  - action_open_browsers

# open browsers 2
* open_browsers: Could you [open the browsers](open_browsers)
  - action_open_browsers
* affirm: Yes
  - action_open_browsers

# open browsers 3
* open_browsers: I'd like to [open the browsers](open_browsers)
  - action_open_browsers
* deny: No
  - utter_affirm
  - action_reset_slot_browsers

# close browsers 1
* close_browsers: [Close browsers](close_browsers) please
  - action_close_browsers

# close browsers 2
* close_browsers: Could you [close the browsers](close_browsers)
  - action_close_browsers
* affirm: Yes
  - action_close_browsers

# close browsers 3
* close_browsers: I'd like to [close the browsers](close_browsers)
  - action_close_browsers
* deny: No
  - utter_affirm
  - action_reset_slot_browsers

# refresh browsers 1
* refresh_browsers: [Reset browsers](reset_browsers) please
  - action_refresh_browsers

# refresh browsers 2
* refresh_browsers: Could you [reset the browsers](reset_browsers)
  - action_refresh_browsers
* affirm: Yes
  - action_refresh_browsers

# refresh browsers 3
* refresh_browsers: I'd like to [reset the browsers](reset_browsers)
  - action_refresh_browsers
* deny: No
  - utter_affirm
  - action_reset_slot_browsers

# ask repeat 1
* ask_repeat: Could you repeat please
  - action_repeat

# list of available demos 1
* list_available_demos: Could you show me the list of projects
  - action_list_demos

# list of available demos 2
* list_available_demos: Give me all available demos
  - action_list_demos

# list of available demos try again
* list_available_demos: Show me all the projects please
  - action_list_demos
* affirm: yes
  - action_list_demos

# list of available demos and cancel
* list_available_demos: Give me all demos
  - action_list_demos
* deny: No
  - utter_affirm

# zoom 1
* zoom: Could you zoom [in](zoom_action) please
  - action_zoom

# zoom and try again
* zoom: Zoom [out](zoom_action) [a lot](zoom_big_level)
  - action_zoom
* affirm: Yes
  - action_zoom

# zoom and cancel
* zoom: Can you zoom [in](zoom_action) [a bit](zoom_small_level)
  - action_zoom
* deny: No
  - utter_affirm
  - action_reset_slot_zoom

# zoom and ask action type
* zoom: Make a zoom
  - action_zoom
* zoom: Zoom [in](zoom_action)
  - action_zoom

# move
* move: Move [left](direction) please
  - action_move

# move and indicat direction
* move: Could you move into the map
  - action_move
* move: Go [up](direction)
  - action_move

# move and try again
* move: Show me what's on the [left](direction)
  - action_move
* affirm: Yes
  - action_move

# move and cancel
* move: I want you to go [down](direction)
  - action_move
* deny: No
  - utter_affirm
  - action_reset_slot_direction

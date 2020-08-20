## welcome and asking for help
* greet
  - utter_greet
* affirm
  - action_help

## welcome and no help needed
* greet
  - utter_greet
* deny
  - utter_goodbye

## quit
* goodbye
  - utter_goodbye

## help
* help
  - action_help

## open success
* open
  - action_open
  - slot{"demo": null,"read_list":false,"restart":false}

## open fail and list
* open
  - action_open
  - slot{"read_list": true,"restart":false}
* affirm
  - action_reset_slot_open
  - slot{"demo": null,"read_list":false,"restart":false}
  - action_list_demos

## open fail and not list
* open
  - action_open
  - slot{"read_list": true,"restart":false}
* deny
  - utter_affirm
  - action_reset_slot_open
  - slot{"demo": null,"read_list":false,"restart":false}

## open fail and restart
* open
  - action_open
  - slot{"read_list":false,"restart":true}
* affirm
  - action_open

## open fail and not restart
* open
  - action_open
  - slot{"read_list":false,"restart":true}
* deny
  - utter_affirm
  - action_reset_slot_open
  - slot{"demo": null,"read_list":false,"restart":false}

## open and find demo similar
* open
  - action_open
  - slot{"read_list":false,"restart":false}
* open
  - action_open
  - slot{"demo": null,"read_list":false,"restart":false}

## open and find demo similar but cancel or cancel restart
* open
  - action_open
* deny
  - utter_affirm
  - action_reset_slot_open
  - slot{"demo": null,"read_list":false}

## out_of_scope
* out_of_scope
  - utter_out_of_scope

## search
* search
 - action_search
 - slot{"demo": null,"tag":null,"search_mode":null}

## search and problem, new try
 * search
  - action_search
 * affirm
  - action_search

## search and give up
 * search
  - action_search
 * deny
  - utter_affirm
  - action_reset_slot_search
  - slot{"demo": null,"tag":null,"search_mode":null}

## shutdown confirm
* shutdown
  - utter_confirm_shutdown
* affirm
  - action_shutdown

## shutdown confirm and fail, restart
* shutdown
  - utter_confirm_shutdown
* affirm
  - action_shutdown
* affirm
  - action_shutdown

## shutdown confirm and fail, give up
* shutdown
  - utter_confirm_shutdown
* affirm
  - action_shutdown
* deny
  - utter_affirm

## shutdown cancel
* shutdown
  - utter_confirm_shutdown
* deny
  - utter_affirm

## turn on gdo, confirm
* turn_on_gdo
  - utter_confirm_turn_on_gdo
* affirm
  - action_turn_on_gdo

## turn on gdo, cancel
* turn_on_gdo
  - utter_confirm_turn_on_gdo
* deny
  - utter_affirm

## turn on gdo, confirm, restart
* turn_on_gdo
  - utter_confirm_turn_on_gdo
* affirm
  - action_turn_on_gdo
* affirm
  - action_turn_on_gdo

## turn on gdo, confirm, without restart
* turn_on_gdo
  - utter_confirm_turn_on_gdo
* affirm
  - action_turn_on_gdo
* deny

## control
* control
  - action_control
  - slot{"control_command":null}

# clear screens
* clear_space
  - action_clear_space

# switch modes
* switch_modes
  - action_switch_modes
  - slot{"mode":null,"switch_action":null}

# open environment
* open_environment
  - action_open_environment
  - slot{"work_environment":null}

# open browsers success
* open_browsers
  - action_open_browsers

# open browsers, fail, try again
* open_browsers
  - action_open_browsers
* affirm
  - action_open_browsers

# open browsers, fail
* open_browsers
  - action_open_browsers
* deny
  - utter_affirm

# close browsers success
* close_browsers
  - action_close_browsers

# close browsers, fail, try again
* close_browsers
  - action_close_browsers
* affirm
  - action_close_browsers

# close browsers, fail
* close_browsers
  - action_close_browsers
* deny
  - utter_affirm

# refresh browsers success
* refresh_browsers
  - action_refresh_browsers

# refresh browsers, fail, try again
* refresh_browsers
  - action_refresh_browsers
* affirm
  - action_refresh_browsers

# refresh browsers, fail
* refresh_browsers
  - action_refresh_browsers
* deny
  - utter_affirm

# ask repeat
* ask_repeat
  - action_repeat

# list of available projects
* list_available_demos
  - action_list_demos

# list of available projects and try again
* list_available_demos
  - action_list_demos
* affirm
  - action_list_demos

# list of available projects and cancel
* list_available_demos
  - action_list_demos
* deny
  - utter_affirm

# zoom
* zoom
  - action_zoom
  - slot{"zoom_action":null,"zoom_big_level":null,"zoom_small_level":null}

# zoom and try again
* zoom
  - action_zoom
* affirm
  - action_zoom

# zoom and cancel
* zoom
  - action_zoom
* deny
  - utter_affirm
  - action_reset_slot_zoom
  - slot{"zoom_action":null,"zoom_big_level":null,"zoom_small_level":null}

# zoom and ask action type
* zoom
  - action_zoom
  - slot{"zoom_action":null}
* zoom
  - action_zoom

# move
* move
  - action_move
  - slot{"direction":null}

# move and ask direction
* move
  - action_move
* move
  - action_move

# move and try again
* move
  - action_move
* affirm
  - action_move

# move and cancel
* move
  - action_move
* deny
  - utter_affirm
  - action_reset_slot_direction
  - slot{"direction":null}

<!-- # set reminder
* ask_remind_end_of_meeting
  - action_set_reminder

# reminder
* EXTERNAL_reminder
  - action_react_to_reminder -->

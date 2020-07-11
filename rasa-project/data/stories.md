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
  - slot{"demo": null,"demo_name": null}

## open fail and list
* open
  - action_open
  - slot{"demo": null,"demo_name": null}
* affirm
  - action_list_demos

## open fail
* open
  - action_open
  - slot{"demo": null,"demo_name": null}
* deny
  - utter_affirm
  - action_reset_slot
  - slot{"demo": null,"demo_name": null}

## open fail and restart
* open
  - action_open
  -  slot{"demo": null,"demo_name": null}
* new_try
  - action_open
  -  slot{"demo": null,"demo_name": null}

## open and find demo similar
* open
  - action_open
  - slot{"demo": null}
* open
  - action_open
  - slot{"demo": null,"demo_name": null}

## out_of_scope
* out_of_scope
  - utter_out_of_scope

## search
* search
 - action_search
 - slot{"demo": null}

## search and demo not found, new try
 * search
  - action_search
  - slot{"demo": null}
 * affirm
  - utter_ask_new_search

## search and give up
 * search
  - action_search
  - slot{"demo": null}
 * deny
  - utter_affirm

## search and issue to load available demos, new_try
 * search
  - action_search
  - slot{"demo": null}
 * new_try
  - action_search

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

## uniform screens
* uniform_background
  - action_uniform_screens

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
  - slot{"mode":null}

# open environment
* open_environment
  - action_open_environment
  - slot{"work_environment":null}

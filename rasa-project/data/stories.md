## welcome and asking for help
* greet
  - utter_greet
* affirm
  - utter_help

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
  - utter_help

## open success
* open
  - action_open
  - slot{"demo": null}

## open fail and list
* open
  - action_open
  - slot{"demo": null}
* affirm
  - action_list_demos

## open fail
* open
  - action_open
  - slot{"demo": null}
* deny
  - utter_affirm

## open fail and restart
* open
  - action_open
  - slot{"demo": null}
* new_try
  - action_open
  - slot{"demo": null}

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

## shutdown cancel
* shutdown
  - utter_confirm_shutdown
* deny
  - utter_affirm

## uniform screens
* uniform_background
  - action_uniform_screens
  - slot{"color":null}

## control
* control
  - action_control
  - slot{"control_command":null}

from utilities.utils_graphql import GraphQL
from utilities.actions_tools import *
from utilities.utils import demo_contains_word, find_string_in_other_string
import ast

def action_open_environment(graphql,environment_slot):
    "Function that manages the open environment rasa action"

    try:
        result = {'success':True}
        current_environment = graphql.get_current_environment()
        list_available_environments = graphql.get_available_environments()
        if environment_slot == None and graphql.environment_is_open():
            result.update({'message':'The current environment is {}'.format(current_environment)})
        elif environment_slot == None:
            result.update({'message':'No environment is open. The available environments are : '+', '.join(list_available_environments)})
        elif environment_slot == current_environment:
            result.update({'message':'The environment is already the '+str(environment_slot)+' one'})
        elif environment_slot not in list_available_environments:
            result.update({'message':"There's no such available environment. The available environments are : "+", ".join(list_available_environments)})
        else:
            result.update({'message':'The environment has been set to {}'.format(graphql.open_environment(environment_slot)["changeEnvironment"]["id"])})
    except Exception as exc:
        result = {'success':False,'message':str(exc)}
        result.update(ast.literal_eval(str(exc)))
    finally:
        return result

def action_switch_mode(graphql,mode_slot,switch_action_slot):
    "Function that manages ActionSwitchMode"
    try:
        result = {'success':True}
        current_mode = graphql.get_current_mode()
        if mode_slot!="cluster" and mode_slot!="section":
            mode_slot = None
        if mode_slot == None and current_mode == None:
            result.update({'message':'No mode has been selected. You can choose between cluster or section'})
        elif mode_slot == None and switch_action_slot!=None and current_mode=='section':
            result.update({'message':'The mode has been changed to {}'.format(graphql.choose_mode('cluster')['changeMode']['id'])})
        elif mode_slot == None and switch_action_slot!=None and current_mode=='cluster':
            result.update({'message':'The mode has been changed to {}'.format(graphql.choose_mode('section')['changeMode']['id'])})
        elif mode_slot == None:
            result.update({'message':'The current mode is {}'.format(current_mode)})
        elif current_mode == mode_slot:
            result.update({'message':'The mode is already {}'.format(current_mode)})
        else:
            result.update({'message':'The mode has been changed to {}'.format(graphql.choose_mode(mode_slot)['changeMode']['id'])})
    except Exception as exc:
        result = {'success':False,'message':str(exc)}
        result.update(ast.literal_eval(str(exc)))
    finally:
        return result

def action_list_demos(graphql,bot_last_messagae):
    "Function that displays the list of demos"

    try:
        result= {'success':True}
        if graphql.environment_is_open():
            list_demos = GraphQL.get_projects(graphql.config['url'])
            if list_demos == None:
                result.update({'message':'There are no demos available in the current environment {}'.format(graphql.get_current_environment())})
            elif len(list_demos)>10:
                if bot_last_messagae == "The list is pretty long ({} demos). Do you still want me to read it out ?".format(len(list_demos)):
                    result.update({'message':'Here are the available demos : '+', '.join(list_demos.values())})
                else:
                    result.update({'message':"The list is pretty long ({} demos). Do you still want me to read it out ?".format(len(list_demos))})
            else:
                result.update({'message':'Here are the available demos : '+', '.join(list_demos.values())})
        else:
            result.update({'message':"No environment is open so I can't load the list of demos. You can choose an environment between : "+" ,".join(graphql.get_available_environments())})
    except Exception as exc:
        result = {'success':False,'message':str(exc)}
        result.update(ast.literal_eval(str(exc)))
    finally:
        return result

def action_launch_project(graphql,name_project):
    "Function to launches a project"
    try:
        result = {'success':True}
        if not graphql.environment_is_open():
            result.update({'success':False,'message':'No environment is open'})
        elif name_project == None:
            result.update({'message':'There is no such demo available. Would you like to hear the list ?','list':True})
        else:
            map_projects = GraphQL.get_projects(graphql.config['url'])
            if name_project in map_projects.values():
                graphql.load_project(name_project)
                result.update({'message':'{} is open'.format(name_project),'project':None,'list':False})
            else:
                similar_project = find_string_in_other_string(name_project,list(map_projects.values()))
                if similar_project != None:
                    result.update({'message':"I've found this demo : {}. Do you want me to open it ?".format(similar_project),'project':similar_project,'list':False})
                else:
                    result.update({'message':'There is no such demo available. Would you like to hear the list ?','list':True})
    except Exception as exc:
        result = {'success':False,'message':str(exc)}
        result.update(ast.literal_eval(str(exc)))
    finally:
        return result

def action_browsers(graphql,id):
    "Function that executes action on browsers"
    try:
        if not graphql.environment_is_open() :
            result = {'success':False,'message':'No environment is open'}
        elif not graphql.mode_is_selected():
            result = {'success':False,'message':'No mode has been selected'}
        else:
            result = {'success':True}
            result.update(graphql.browser_actions(id))
    except Exception as exc:
        result = {'success':False,'message':str(exc)}
        result.update(ast.literal_eval(str(exc)))
    finally:
        return result

def action_controller(graphql,id_action,id_app,message):
    "Function that executes controller actions"

    try:
        result = {'success':True}
        list_video_actions = ['play','pause','stop','seekTo?time=0','play?loop=true']
        result.update(graphql.controller_actions(id_action,id_app))
        response = graphql.get_current_project()
        if response == None:
            result = {'success':False,'message':'No project is open'}
        elif (id_action in list_video_actions and not graphql.project_has_video_controller(response)) or (id_action == 'refresh' and not graphql.project_has_html_controller(response)):
            result =  {'success':False,'message':message}
    except Exception as exc:
        result = {'success':False,'message':str(exc)}
        result.update(ast.literal_eval(str(exc)))
    finally:
        return result

def action_play(graphql):
    "Function that executes play action"
    return action_controller(graphql,'play','OVE_APP_VIDEOS','There is no video controller for this project')

def action_pause(graphql):
    "Function that executes pause action"
    return action_controller(graphql,'pause','OVE_APP_VIDEOS','There is no video controller for this project')

def action_stop(graphql):
    "Function that executes stop action"
    return action_controller(graphql,'stop','OVE_APP_VIDEOS','There is no video controller for this project')

def action_reset(graphql):
    "Function that executes reset action"
    return action_controller(graphql,'seekTo?time=0','OVE_APP_VIDEOS','There is no video controller for this project')

def action_play_loop(graphql):
    "Function that executes play_loop action"
    return action_controller(graphql,'play?loop=true','OVE_APP_VIDEOS','There is no video controller for this project')

def action_refresh(graphql):
    "Function that executes refresh action"
    return action_controller(graphql,'refresh','OVE_APP_HTML','There is no html controller for this project')

def action_search(graphql,name,tag,search_mode):
    "Funtion that executes search action"
    try:
        result = {'success':True,'message':'Do you want to search by tag or by keyword ? Please choose one of the both options'}
        if not graphql.environment_is_open():
            result.update({'success':False,'message':"I can't access to any demo if no environment is open. Please, open one of these environments before : "+" ,".join(graphql.get_available_environments())})
        elif 'tag' in search_mode and tag == None:
            result.update({'message':'Fine, please say "search" or "look for" and your tag. If you already did and got no answer for that request that means that no demo contains this tag'})
        elif tag != None:
            result.update(search_process_tag(graphql,tag))
        elif 'key' in search_mode and name == None:
            result.update({'message':'Fine, please say "search" or "look for" and your keyword. If you already did and got no answer for that request that means that no demo contains this keyword'})
        elif name != None:
            result.update(search_process_name(graphql,name))
    except Exception as exc:
        result = {'success':False,'message':str(exc)}
        result.update(ast.literal_eval(str(exc)))
    finally:
        return result

def action_clear_space(graphql):
    "Function that executes clear space action"
    try:
        result = {"success":True}
        result.update(graphql.clear_screen())
    except Exception as exc:
        result = {'success':False,'message':str(exc)}
        result.update(ast.literal_eval(str(exc)))
    finally:
        return result

def action_turn_off_gdo(graphql):
    "Function that executes gdo shutdown action"
    try:
        result = {"success":True}
        result.update(graphql.turn_off_gdo())
    except Exception as exc:
        result = {'success':False,'message':str(exc)}
        result.update(ast.literal_eval(str(exc)))
    finally:
        return result

def action_turn_on_gdo(graphql):
    "Function that executes gdo turn on action"
    try:
        result = {"success":True}
        result.update(graphql.turn_on_gdo())
    except Exception as exc:
        result = {'success':False,'message':str(exc)}
        result.update(ast.literal_eval(str(exc)))
    finally:
        return result

def action_zoom(graphql,zoom_action_slot,zoom_level_slot=None):
    "Function that executes zoom-in or zoom_out actions"
    try:
        result = {'success':True}
        zoom = 'Nothing has been done yet'
        if not graphql.environment_is_open():
            result.update({'success':False})
            zoom = 'No environment is open. Please, open one of these environments before : '+' ,'.join(graphql.get_available_environments())
        elif graphql.get_current_project() == None:
            result.update({'success':False})
            zoom = 'No project is open'
        elif zoom_action_slot == None:
            zoom = 'Do you want to zoom in or zoom out ?'
        elif zoom_action_slot == 'in' and zoom_level_slot == None:
            zoom = graphql.zoom_maps(graphql.config['zoomin'][1]['medium'])
        elif zoom_action_slot == 'in' and zoom_level_slot == 'small':
            zoom = graphql.zoom_maps(graphql.config['zoomin'][0]['little'])
        elif zoom_action_slot == 'in' and zoom_level_slot == 'big':
            zoom = graphql.zoom_maps(graphql.config['zoomin'][2]['big'])
        elif zoom_action_slot == 'out' and zoom_level_slot == None:
            zoom = graphql.zoom_mpas(graphql.config['zoomout'][1]['medium'])
        elif zoom_action_slot == 'out' and zoom_level_slot == 'small':
            zoom = graphql.zoom_maps(graphql.config['zoomout'][0]['little'])
        elif zoom_action_slot == 'out' and zoom_level_slot == 'big':
            zoom = graphql.zoom_maps(graphql.config['zoomout'][2]['big'])
        result.update({'message':zoom})
    except Exception as exc:
        result = {'success':False,'message':str(exc)}
        result.update(ast.literal_eval(str(exc)))
    finally:
        return result

def action_move(graphql,direction_slot):
    "Function that executez move actions"

    try:
        result = {'success':True}
        if not graphql.environment_is_open():
            result.update({'success':False, 'message':'No environment is open. Please, open one of these environments before : '+' ,'.join(graphql.get_available_environments())})
        elif graphql.get_current_project() == None:
            result.update({'success':False, 'message':'No project is open'})
        elif direction_slot in ['top','up']:
            result.update({'message':graphql.move_maps(graphql.config['move'][2]['up'])})
        elif direction_slot in ['bottom','down']:
            result.update({'message':graphql.move_maps(graphql.config['move'][3]['down'])})
        elif direction_slot == 'left':
            result.update({'message':graphql.move_maps(graphql.config['move'][0]['left'])})
        elif direction_slot == 'right':
            result.update({'message':graphql.move_maps(graphql.config['move'][1]['right'])})
        else:
            result.update({'message':'Do you want to go down, up, left or right ?'})
    except Exception as exc:
        result = {'success':False,'message':str(exc)}
        result.update(ast.literal_eval(str(exc)))
    finally:
        return result

"""
LOGGING
"""
from logger import *

"""
PROJECT CLASSES
"""
from SoundDeviceManager import SoundDeviceManager
from device_list import DeviceList

"""
AUDIO
"""
import pycaw.pycaw as pycaw
"""
Couleur
"""
from colorama import Fore
"""
CLI Libraries
"""
import prompt_toolkit
# prompt_toolkit . print_formatted_text, HTML
from inquirer2 import prompt, Separator
# cool title
from pyfiglet import Figlet

from pprint import pprint
"""
OS RELATED
"""
import os
import platform
"""
PARAMETERS
"""
import json

"""
STYLE
"""
from style import *


def print_device(device : pycaw.AudioDevice, device_pointer_dict : dict):
    
    PLAYBACK_THOURGH_DEVICE_PROPERTY_KEY = "{24DBB0FC-9311-4B3D-9CF0-18FF155639D4} 0"
    
    if PLAYBACK_THOURGH_DEVICE_PROPERTY_KEY in device.properties:
            playback_device_name = device_pointer_dict[device.properties.get(PLAYBACK_THOURGH_DEVICE_PROPERTY_KEY)].FriendlyName
            add_on_str = playback_device_name
    else:
            add_on_str = ""
            html_str = prompt_toolkit.HTML(f"<aaa fg='ansired'>{device.FriendlyName}</aaa>  <bbb fg='#3e4754'><i>{device.id}</i></bbb>\n<ccc fg='ansigreen'>playback device :</ccc> <ddd fg='#faf766'> {add_on_str} </ddd> | <bbb fg='#3e4754'><i>{device.properties.get(PLAYBACK_THOURGH_DEVICE_PROPERTY_KEY)}</i></bbb>\n\n")
            prompt_toolkit.print_formatted_text(html_str)
            


def clear():
    """Clears the screen
    """
    program_log.debug("Clearing the Console...")
    running_system = platform.system()
    Posix_Systems = ["Linux",
                     "Darwin"   # MAC OS
                     ]
    if running_system in Posix_Systems:
        os.system('clear')
    elif running_system == "Windows":
        os.system('cls')

    return



# ! compléter la liste de ce qu'on peut configurer


program_log.debug("Instanciating DeviceList object...")
device_list = DeviceList()

def refresh_devices(case = None):
    """Returns a list of devices, depending on the action we want to perform
    
        --> recording
        --> playback
    
    Return :
        --> list of devices names
        --> with PyInquirer Separators
    
    """
    
    program_log.info(f"Refreshing devices list with case : {case}")
    
    SoundDeviceManager.update_devices()    

    if case == None :
        pass
    
    elif case == "checkbox-recording" :
        return device_list.get_checkbox_list(device_type=["recording"], disable_device_checkbox_if= DeviceList.ALL)
    
    elif case == "checkbox-playback" :
        return device_list.get_checkbox_list(device_type=["playback"], disable_device_checkbox_if= DeviceList.ALL)
    
    elif case == "list-all"  :
        return device_list.get_checkbox_list(device_type=["playback", "recording"], disable_device_checkbox_if= DeviceList.ALL)
    
    elif case == "list-enabled-playback":
        return device_list.get_list(device_type=["playback"], condition= DeviceList.ALREADY_ACTIVE)
    
    elif case == "enable" :
        return device_list.get_checkbox_list(device_type=["playback", "recording"], disable_device_checkbox_if= DeviceList.ALREADY_ACTIVE)
    
    
    elif case == "disable" :
        return device_list.get_checkbox_list(device_type=["playback", "recording"], disable_device_checkbox_if= DeviceList.ALREADY_DISABLED)

    elif case == "disable-recording" :
        return device_list.get_checkbox_list(device_type=["recording"], disable_device_checkbox_if= DeviceList.ALREADY_DISABLED)



def menu():
    
    program_log.debug("Getting user prompt...")
    
    program_log.debug("Creating the Questions...")
    questions = [

        {
            'type': 'list',
            'name': 'app_choice',
            'message': 'What do you want to do ?',
            'choices': ['enable', 'disable', 'restart', 'playback through', 'quit']
        },


        {
            'type' : 'checkbox',
            'name' : 'enable_device',
            'message' : 'Select the desired Devices',
            'choices' :  refresh_devices("enable"),
            'when' : lambda answer : answer['app_choice'] == 'enable'
        },
        
        {
            'type' : 'checkbox',
            'name' : 'disable_device',
            'message' : 'Select the desired Devices',
            'choices' :  refresh_devices("disable"),
            'when' : lambda answer : answer['app_choice'] == 'disable'
        },
        
        {
            'type' : 'checkbox',
            'name' : 'restart_device',
            'message' : 'Select the desired Devices',
            'choices' :  refresh_devices("disable"),
            'when' : lambda answer : answer['app_choice'] == 'restart'
        },
        
        
        
        {
            'type' : 'checkbox',
            'name' : 'playback_through_select_devices',
            'message' : 'Select the desired Recording Devices',
            'choices' : refresh_devices("disable-recording"),
            'when' : lambda answer : answer['app_choice'] == 'playback through'
        }, 

        {
            'type' : 'list',
            'name' : 'playback_through_select_device_playback',
            'message' : 'Select the desired Playback Devices',
            'choices' : refresh_devices("list-enabled-playback"),
            'when' : lambda answer : answer['app_choice'] == 'playback through' and answer['playback_through_select_devices']
        },
        # QUIT confirm
        {
            'type': 'confirm',
            'name': 'quit_confirm',
            'message': 'Do you want to Exit ?',
            'default': False,
            'when': lambda answers: answers['app_choice'] == 'quit'
        }

    ]
    
    program_log.debug("Prompting user...")
    answers = prompt.prompt(questions, style=style)
    return answers


def render_title():
    f = Figlet(font='slant')
    print(f.renderText('WINDAUBE SOUND TOOL'))
    print(Fore.CYAN + "un outil pour un OS de merde !\n\n " + Fore.WHITE)
    print("---   " + Fore.YELLOW + "Github/allemand-instable" +
          Fore.WHITE + "   ---\n\n\n")


def action():
    program_log.debug("Running action...")
    clear()
    render_title()

    # affiche le menu et retourne les résultats
    answer = menu()

    program_log.debug("Answers retrieved")
    
    program_log.debug(f"user's app choice is : {answer['app_choice']}")

    if answer['app_choice'] == "enable" :

        for device_name in answer['enable_device'] :
            SoundDeviceManager.enable( SoundDeviceManager.devices["by_name"][device_name] )
        
    elif answer['app_choice'] == "disable" :
        for device_name in answer['disable_device'] :
            SoundDeviceManager.disable( SoundDeviceManager.devices["by_name"][device_name] )
            
    elif answer['app_choice'] == "restart" :
        for device_name in answer['restart_device'] :
            SoundDeviceManager.restart( SoundDeviceManager.devices["by_name"][device_name] )
            
    elif answer['app_choice'] == 'playback through':
        for device_name in answer["playback_through_select_devices"] :
            recording_device = SoundDeviceManager.devices["by_name"][device_name]
            playback_work_device = SoundDeviceManager.devices["by_name"][answer["playback_through_select_device_playback"]]
            print(playback_work_device)
            SoundDeviceManager.set_playback_through(enable = True, record_device= recording_device, playback_device= playback_work_device)
    elif answer['app_choice'] == 'quit' and answer["quit_confirm"] == True:
        clear()
        return False

    program_log.info("No task to do, ending loop...")
    # si l'utilisateur ne veut pas
    return True


def run():
    """
    continue la boucle
    """
    program_log.info("Running Menu...")
    running = True
    program_log.debug(f"running variable is : {running}")
    while running:
        
        running = action()
    program_log.debug("End of Menu")
    return

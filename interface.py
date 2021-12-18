import pycaw.pycaw as pycaw
import prompt_toolkit
    
    
    
def print_device(device : pycaw.AudioDevice, device_pointer_dict : dict):
    
    PLAYBACK_THOURGH_DEVICE_PROPERTY_KEY = "{24DBB0FC-9311-4B3D-9CF0-18FF155639D4} 0"
    
    if PLAYBACK_THOURGH_DEVICE_PROPERTY_KEY in device.properties:
            playback_device_name = device_pointer_dict[device.properties.get(PLAYBACK_THOURGH_DEVICE_PROPERTY_KEY)].FriendlyName
            add_on_str = playback_device_name
    else:
            add_on_str = ""
            html_str = prompt_toolkit.HTML(f"<aaa fg='ansired'>{device.FriendlyName}</aaa>  <bbb fg='#3e4754'><i>{device.id}</i></bbb>\n<ccc fg='ansigreen'>playback device :</ccc> <ddd fg='#faf766'> {add_on_str} </ddd> | <bbb fg='#3e4754'><i>{device.properties.get(PLAYBACK_THOURGH_DEVICE_PROPERTY_KEY)}</i></bbb>\n\n")
            prompt_toolkit.print_formatted_text(html_str)
            

import platform
import logging
import json


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
CLEAR FUNCTION
"""
import os


from tools import SoundDeviceManager

def clear():
    running_system = platform.system()
    Posix_Systems = ["Linux",
                     "Darwin"   # MAC OS
                     ]
    if running_system in Posix_Systems:
        os.system('clear')
    elif running_system == "Windows":
        os.system('cls')

    return


"""
REQUETES
"""

import requests
import json
headers = {'accept': 'application/json'}
API_URL = 'http://127.0.0.1:8000/'


"""
STYLE
"""

red_color = "#E91E63"
blue_color = "#2196f3"
orange_color = "#ff8700"
cyan_color = "#00ffd7"
gray_color = "#474747"

style = prompt_toolkit.styles.Style([
    ('separator',    red_color),
    ('questionmark', red_color),
    ('focus',        blue_color),
    ('checked',      blue_color),
    ('pointer',      orange_color),
    ('instruction',  orange_color),
    ('answer',       cyan_color),
    ('question',     blue_color),
    ("disabled", gray_color)
])


# ! compléter la liste de ce qu'on peut configurer


def refresh_devices(case = None):
    
    SoundDeviceManager.update_devices()    

    if case == None :
        pass
    elif case == "checkbox-recording" :
        Recording_devices_checkboxes =  [   ]
        for device in SoundDeviceManager.list_devices("recording") :
            added = { 'name' : "[r]  " + device, 'checked' : False }
            if added not in Recording_devices_checkboxes :
                Recording_devices_checkboxes.append(added)
        sep_recording = [Separator("Recording devices")]
        return sep_recording + Recording_devices_checkboxes
    elif case == "checkbox-playback" :
        Playback_devices_checkboxes =  []
        for device in SoundDeviceManager.list_devices("playback") :
            added = { 'name' : "[p]  " + device, 'checked' : False }
            if added not in Playback_devices_checkboxes :
                Playback_devices_checkboxes.append(added)
        sep_playback = [Separator("Playback Devices")]
        return sep_playback + Playback_devices_checkboxes        
    
    elif case == "list-all"  :
        sep_recording = [Separator("Recording devices")]
        sep_playback = [Separator("Playback Devices")]
        list_all_devices =  sep_playback + ["[p]  " + device for device in list(dict.fromkeys(SoundDeviceManager.list_devices("playback")))] + sep_recording + [ "[r]  " + device for device in list(dict.fromkeys(SoundDeviceManager.list_devices("recording")))]
        return list_all_devices
    
    elif case == "list-enabled-playback":
        return list(dict.fromkeys(["[p]  " + device.FriendlyName for device in SoundDeviceManager.devices["playback"] if SoundDeviceManager.is_active(device)]))
    
    elif case == "enable" :
        Recording_devices_checkboxes =  [   ]
        for device in SoundDeviceManager.devices["recording"] :
            if SoundDeviceManager.is_active(device) :
                added = { 'name' : "[r]  " + device.FriendlyName, 'checked' : False, 'disabled' : ' active ' }
            else :
                added = { 'name' : "[r]  " + device.FriendlyName, 'checked' : False }
            if added not in Recording_devices_checkboxes :
                Recording_devices_checkboxes.append(added)
        
        Playback_devices_checkboxes =  []
        for device in SoundDeviceManager.devices["playback"] :
            if SoundDeviceManager.is_active(device) :
                added = { 'name' : "[p]  " + device.FriendlyName, 'checked' : False, 'disabled' : ' active ' }
            else :
                added = { 'name' : "[p]  " + device.FriendlyName, 'checked' : False }
            if added not in Playback_devices_checkboxes :
                Playback_devices_checkboxes.append(added)

        sep_playback = [Separator("Playback Devices")]
        sep_recording = [Separator("Recording devices")]
        all_devices_checkboxes = sep_playback + Playback_devices_checkboxes + sep_recording + Recording_devices_checkboxes

        return all_devices_checkboxes
    
    
    elif case == "disable" :
        Recording_devices_checkboxes =  [   ]
        for device in SoundDeviceManager.devices["recording"] :
            if not SoundDeviceManager.is_active(device) :
                added = { 'name' : "[r]  " + device.FriendlyName, 'checked' : False, 'disabled' : 'disabled' }
            else :
                added = { 'name' : "[r]  " + device.FriendlyName, 'checked' : False }
            if added not in Recording_devices_checkboxes :
                Recording_devices_checkboxes.append(added)
        
        Playback_devices_checkboxes =  []
        for device in SoundDeviceManager.devices["playback"] :
            if not SoundDeviceManager.is_active(device) :
                added = { 'name' : "[p]  " + device.FriendlyName, 'checked' : False, 'disabled' : 'disabled' }
            else :
                added = { 'name' : "[p]  " + device.FriendlyName, 'checked' : False }
            if added not in Playback_devices_checkboxes :
                Playback_devices_checkboxes.append(added)

        sep_playback = [Separator("Playback Devices")]
        sep_recording = [Separator("Recording devices")]
        all_devices_checkboxes = sep_playback + Playback_devices_checkboxes + sep_recording + Recording_devices_checkboxes
        return all_devices_checkboxes

    elif case == "disable-recording" :
        Recording_devices_checkboxes =  [   ]
        for device in SoundDeviceManager.devices["recording"] :
            if not SoundDeviceManager.is_active(device) :
                added = { 'name' : "[r]  " + device.FriendlyName, 'checked' : False, 'disabled' : 'disabled' }
            else :
                added = { 'name' : "[r]  " + device.FriendlyName, 'checked' : False }
            if added not in Recording_devices_checkboxes :
                Recording_devices_checkboxes.append(added)
        
        sep_recording = [Separator("Recording devices")]
        all_devices_checkboxes = sep_recording + Recording_devices_checkboxes


        return all_devices_checkboxes



def menu():
    
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
    
    answers = prompt.prompt(questions, style=style)
    return answers


def render_title():
    f = Figlet(font='slant')
    print(f.renderText('WINDAUBE SOUND TOOL'))
    print(Fore.CYAN + "un outil pour un OS de merde !\n\n " + Fore.WHITE)
    print("---   " + Fore.YELLOW + "Github/allemand-instable" +
          Fore.WHITE + "   ---\n\n\n")


def action():

    clear()
    render_title()

    # affiche le menu et retourne les résultats
    answer = menu()

    if answer['app_choice'] == "enable" :

        for device_name in answer['enable_device'] :
            SoundDeviceManager.enable( SoundDeviceManager.devices["by_name"][device_name] )
        
    elif answer['app_choice'] == "disable" :
        for device_name in answer['disable_device'] :
            SoundDeviceManager.disable( SoundDeviceManager.devices["by_name"][device_name] )
            
    elif answer['app_choice'] == "restart" :
        for device_name in answer['restart_device'] :
            SoundDeviceManager.restart( SoundDeviceManager.devices["by_name"][device_name] )
            
    elif answer['app_choice'] == 'playback_through_select_devices':
        for device_name in answer["playback_through_select_devices"] :
            print(device_name)
            SoundDeviceManager.set_playback_through(enable = True, record_device= SoundDeviceManager.devices["by_name"][device_name], playback_device= answer["playback_through_select_device_playback"])
    elif answer['app_choice'] == 'quit' and answer["quit_confirm"] == True:
        clear()
        return False

    # si l'utilisateur ne veut pas
    return True


def run():
    """
    continue la boucle
    """
    running = True
    while running:
        running = action()
        # ! replacer par un log

    return


def main():
    run()
    return


# Définie la main
if __name__ == "__main__":
    main()

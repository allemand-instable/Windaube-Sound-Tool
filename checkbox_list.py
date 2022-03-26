from SoundDeviceManager import SoundDeviceManager
from inquirer2 import Separator
from logger import *

#   Disable devices conditions

ALL = 0
ALREADY_ACTIVE = 1 
ALREADY_DISABLED = 2 

disabled_text_list = [ None, "Already active", "Already disabled" ]

#   device types

correct_device_types = [
    ["recording"],
    ["playback"],
    ["playback", "recording"],
    ["recording", "playback"]
]


def device_checkbox_list_with_separator(device_type : list[str], disable_device_checkbox_if : int = ENABLE_ALL, include_separator : bool = True) -> list:
    """Returns list of devices with a separator for the desired category for checkbox operation
    
    list returned :
    [
        separator,
        ---------
        dict[device name, checkbox status]
    ]
    """
    
    if device_type not in correct_device_types :
        raise TypeError(f"device_type must be one of {correct_device_types}")
    
    final_list = []
    
        
    for type in device_type :
        device_list = []
        # recording -> [r]
        # playback -> [p]
        device_prefix = f"[{type[0]}]  "
        for device in SoundDeviceManager.list_devices(type) : 
            
            # disables checkbox based on the condition
            
            if disable_checkbox_condition(device, disable_device_checkbox_if) :
                added = {   'name' : device_prefix  + device, 
                            'checked' : False, 
                            'disabled' : disabled_text_list[disable_device_checkbox_if] 
                        }
            else :
                added = {   'name' : device_prefix  + device, 
                            'checked' : False
                        }
            
            if added not in device_list :
                device_list.append(added)
        
        # if you don't want the separator
        if include_separator is True :
            sep = [Separator( type.capitalize() + " devices")]
            block = sep + device_list
        else :
            block = device_list
        
        final_list + block
    
    return final_list


def disable_checkbox_condition(device, disable_device_checkbox_if : int) -> bool:
    """Returns the condition checker for the disable checkbox"""
    if disable_device_checkbox_if == ENABLE_ALL :
        return False
    elif disable_device_checkbox_if == ALREADY_ACTIVE :
        return SoundDeviceManager.is_active(device)
    elif disable_device_checkbox_if == ALREADY_DISABLED :
        return not SoundDeviceManager.is_active(device)
    else :
        raise Exception(f"Unknown value for disable_device_checkbox_if : {disable_device_checkbox_if}")
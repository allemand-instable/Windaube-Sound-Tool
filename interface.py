import pycaw
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
            


from typing import Union
import pycaw.pycaw as pycaw
import operator
import subprocess
from pprint import pprint
import os
from logger import *

def get_devices() :
    program_log.info("Getting devices")
    """returns a dict with all devices :
    {
        Playback : list[Device]
        Recording : list[Device]
        pointer : dict{ id : device }      
    }
    """
    devices = pycaw.AudioUtilities.GetAllDevices()
    
    # pointers
    program_log.debug("Creating by name device dict...")

    device_pointer_dict = { device.id : device for device in devices }
    
    # recording devices
    program_log.debug("Creating recording devices list...")
    recording_devices = [device for device in devices if "0.0.1.00000000" in device.id.split("{")[1] ]
    recording_devices.sort(key=operator.attrgetter('FriendlyName'))
    program_log.debug("Successfully created recording devices list")
    
    # playback devices
    program_log.debug("Creating playback devices list...")
    playback_devices = [device for device in devices if "0.0.0.00000000" in device.id.split("{")[1]]
    playback_devices.sort(key=operator.attrgetter('FriendlyName'))
    program_log.debug("successfully created playback devices list")
    
    program_log.debug("Creating by name device dict...")
    by_name_dict = {"[p]  " + device.FriendlyName : [] for device in playback_devices  }
    by_name_dict.update( {"[r]  " + device.FriendlyName : [] for device in recording_devices  } )
    
    for device in playback_devices:
        by_name_dict["[p]  " + device.FriendlyName].append( device )
    for device in recording_devices :
        by_name_dict["[r]  " + device.FriendlyName].append( device )  
    program_log.debug("successfully created by name device dict")
    
    dict = {
        'playback' : playback_devices,
        'recording' : recording_devices,
        'pointer' : device_pointer_dict,
        "by_name" : by_name_dict
    }
    
    return dict

def get_device_playback_through(device):
    program_log.info("Getting playback through devices")
    PLAYBACK_THOURGH_DEVICE_PROPERTY_KEY = "{24DBB0FC-9311-4B3D-9CF0-18FF155639D4} 0"
    if PLAYBACK_THOURGH_DEVICE_PROPERTY_KEY in device.properties:
        program_log.debug(f"Found property : Playback Thourgh for {device.FriendlyName}")
        playback_device_id = device.properties.get(PLAYBACK_THOURGH_DEVICE_PROPERTY_KEY)
    else :
        program_log.debug(f"{device.FriendlyName} has not the playback through property key")
        playback_device_id = None
    return playback_device_id


def quiet_run_process(args):
    FNULL = open(os.devnull, 'w')    #use this if you want to suppress output to stdout from the subprocess
    subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)

def soundvolumeview(command : str, device : pycaw.AudioDevice, params : str = "" , soundvolumeview_path : str = "./bin/SoundVolumeView.exe"):
    command = soundvolumeview_path + f" /{command} {device.id} {params}"
    print(command)
    quiet_run_process(command)

def enable_device(device, soundvolumeview_path = "./bin/SoundVolumeView.exe"):
    program_log.info(f"Enabling device {device.FriendlyName}")
    soundvolumeview("enable", device, soundvolumeview_path= soundvolumeview_path)
    
def disable_device(device, soundvolumeview_path = "./bin/SoundVolumeView.exe"):
    program_log.info(f"Disabling device {device.FriendlyName}")
    soundvolumeview("disable", device, soundvolumeview_path = soundvolumeview_path)


def restart_device(device, soundvolumeview_path = "./bin/SoundVolumeView.exe"):
    program_log.info(f"Restarting device {device.FriendlyName}")
    disable_device(device, soundvolumeview_path)
    enable_device(device, soundvolumeview_path)
    


def set_playback_through(enable : bool, record_device = None, playback_device = None, soundvolumeview_path = "./bin/SoundVolumeView.exe"):
    if enable is True :
        soundvolumeview("SetListenToThisDevice", record_device, "1", soundvolumeview_path )
        # print("id")
        # pprint(playback_device)
        # pprint(record_device)
        soundvolumeview("SetPlaybackThroughDevice", record_device, playback_device.id, soundvolumeview_path)
        # input()
    else :
        soundvolumeview("SetListenToThisDevice", record_device, "0", soundvolumeview_path)
        


# D = get_devices()
# pprint( SoundDeviceManager.list_devices("recording") )
# pprint( SoundDeviceManager.list_devices("playback") )


# a = SoundDeviceManager.devices["playback"][0]
# b = SoundDeviceManager.devices["playback"][1]
# c = SoundDeviceManager.devices["playback"][3]
# d= SoundDeviceManager.devices["playback"][4]


# u = [a, b, [c,d]]

# SoundDeviceManager.enable(a)
# SoundDeviceManager.enable(u)

# pprint([ device.id for device in SoundDeviceManager.devices["by_name"]["2460G4 (NVIDIA High Definition Audio)"]])
# SoundDeviceManager.update_devices()

# SoundDeviceManager.enable(SoundDeviceManager.devices["by_name"]["[p]  2460G4 (NVIDIA High Definition Audio)"])

# pprint([device.state.value for device in SoundDeviceManager.devices["by_name"]["[r]  Mic 4 (Virtual Audio Cable)"]])


# SoundDeviceManager.enable(SoundDeviceManager.devices["by_name"]["[r]  Mic 4 (Virtual Audio Cable)"])

# SoundDeviceManager.update_devices()
# pprint([device.state.value for device in SoundDeviceManager.devices["by_name"]["[r]  Mic 4 (Virtual Audio Cable)"]])

# SoundDeviceManager.disable(SoundDeviceManager.devices["by_name"]["[r]  Mic 4 (Virtual Audio Cable)"])

# SoundDeviceManager.update_devices()

# pprint([device.state.value for device in SoundDeviceManager.devices["by_name"]["[r]  Mic 4 (Virtual Audio Cable)"]])


# SoundDeviceManager.enable(SoundDeviceManager.devices["by_name"]["[r]  Mic 4 (Virtual Audio Cable)"])
# SoundDeviceManager.update_devices()

# pprint([device.state.value for device in SoundDeviceManager.devices["by_name"]["[r]  Mic 4 (Virtual Audio Cable)"]])


# 0 -> 2
# 1 -> 1
# 8 -> unplugged



# SoundDeviceManager.set_playback_through(True, [device for device in SoundDeviceManager.devices["recording"] if "Line" in device.FriendlyName], SoundDeviceManager.devices["by_name"]["[p]  Speakers (Yeti Stereo Microphone)"] )
# SoundDeviceManager.set_playback_through(True, [device for device in SoundDeviceManager.devices["recording"] if "Line" in device.FriendlyName], SoundDeviceManager.devices["by_name"]["[p]  Headphones (WiBUDS Pocket Stereo)"] )
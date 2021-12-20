from typing import Union
import pycaw.pycaw as pycaw
import operator
import subprocess
from pprint import pprint
import os

def get_devices() :
    """returns a dict with all devices :
    {
        Playback : list[Device]
        Recording : list[Device]
        pointer : dict{ id : device }      
    }
    """
    devices = pycaw.AudioUtilities.GetAllDevices()
    
    # pointers
    device_pointer_dict = { device.id : device for device in devices }
    
    # recording devices
    recording_devices = [device for device in devices if "0.0.1.00000000" in device.id.split("{")[1] ]
    recording_devices.sort(key=operator.attrgetter('FriendlyName'))
    
    # playback devices
    playback_devices = [device for device in devices if "0.0.0.00000000" in device.id.split("{")[1]]
    playback_devices.sort(key=operator.attrgetter('FriendlyName'))
    
    
    by_name_dict = {"[p]  " + device.FriendlyName : [] for device in playback_devices  }
    by_name_dict.update( {"[r]  " + device.FriendlyName : [] for device in recording_devices  } )
    
    for device in playback_devices:
        by_name_dict["[p]  " + device.FriendlyName].append( device )
    for device in recording_devices :
        by_name_dict["[r]  " + device.FriendlyName].append( device )
    
    
    dict = {
        'playback' : playback_devices,
        'recording' : recording_devices,
        'pointer' : device_pointer_dict,
        "by_name" : by_name_dict
    }
    
    return dict

def get_device_playback_through(device):
    PLAYBACK_THOURGH_DEVICE_PROPERTY_KEY = "{24DBB0FC-9311-4B3D-9CF0-18FF155639D4} 0"
    if PLAYBACK_THOURGH_DEVICE_PROPERTY_KEY in device.properties:
        playback_device_id = device.properties.get(PLAYBACK_THOURGH_DEVICE_PROPERTY_KEY)
    else :
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
    soundvolumeview("enable", device, soundvolumeview_path= soundvolumeview_path)
    
def disable_device(device, soundvolumeview_path = "./bin/SoundVolumeView.exe"):
    soundvolumeview("disable", device, soundvolumeview_path = soundvolumeview_path)


def restart_device(device, soundvolumeview_path = "./bin/SoundVolumeView.exe"):
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
        



class SoundDeviceManager():
    
    SoundVolumeView_path = "./bin/SoundVolumeView.exe"
    
    PLAYBACK_THOURGH_DEVICE_PROPERTY_KEY = "{24DBB0FC-9311-4B3D-9CF0-18FF155639D4} 0"
    
    devices = get_devices()
    # 3 keys :
    #   playback
    #   recording
    #   pointer
    #   by_name
    
    def __init__(self) -> None:
        pass
    
    @classmethod
    def get_device_playback_though(cls, device):
        device_id = get_device_playback_through(device)
        device_name = cls.devices["pointer"][device_id].FriendlyName
        return { "id" : device_id, 'name' : device_name}

    @classmethod
    def update_devices(cls):
        cls.devices = get_devices()
        
    @classmethod
    def enable(cls, device : Union[pycaw.AudioDevice, list]):
        if type( device ) == list :
            for d in device :
                cls.enable(d)
        else :
            enable_device(device, cls.SoundVolumeView_path)
            print(f"> {device.id} | {device.FriendlyName} enabled")
    
    @classmethod
    def disable(cls, device : Union[pycaw.AudioDevice, list]):
        if type( device ) == list :
            for d in device :
                cls.disable(d)
        else :
            disable_device(device, cls.SoundVolumeView_path)
            print(f"> {device.id} | {device.FriendlyName} disabled")
    
    @classmethod
    def restart(cls, device : Union[pycaw.AudioDevice, list]):
        if type( device ) == list :
            for d in device :
                cls.restart(d)
        else :
            restart_device(device, cls.SoundVolumeView_path)
            print(f"> {device.id} | {device.FriendlyName} restarted")
    
    @classmethod
    def set_playback_through(cls, enable, record_device, playback_device):
        print("playback device")
        pprint(playback_device)
        print(type(playback_device))
        print("record device")
        pprint(record_device)
        print(type(record_device))
        if type( record_device ) == list :
            for d in record_device :
                cls.set_playback_through(enable, d, playback_device)
        else :
            if type(playback_device) == list :
                if len(playback_device) == 1 :
                    playback_work_device = playback_device[0]
                else :
                    raise Exception("you entered a list of playback devices with several playback devices, can't assign")
            else :
                playback_work_device = playback_device
            # print("type ==============================")
            # print(type(playback_work_device))
            # print(type(record_device))
            set_playback_through(enable, record_device, playback_work_device, cls.SoundVolumeView_path)
            print(f"{record_device.id} | {record_device.FriendlyName} will playback through {playback_work_device.FriendlyName}")
    
    @classmethod
    def list_devices(cls, key):
        available_keys = ["playback", "recording", "pointer"]
        if key not in available_keys :
            raise Exception(f"la clé doit être une des suivantes : {elem for elem in available_keys}")
        return [elem.FriendlyName for elem in cls.devices[key]]

    @staticmethod
    def is_active(device):
        # https://docs.microsoft.com/en-us/windows/win32/coreaudio/device-state-xxx-constants
        if device.state.value in [1,4, 8] :
            # if device.state.value == 8 :
            #     print(f"{device.FriendlyName} : Warning ! device is unplugged.")
            # elif device.state.value == 4 :
            #     print(f"{device.FriendlyName} : The audio endpoint device is not present")
            return True
        
        if device.state.value == 2 :
            return False
        else :
            raise Exception(f"unkown state value : {device.state.value}")

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
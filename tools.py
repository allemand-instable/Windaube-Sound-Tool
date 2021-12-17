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
    
    dict = {
        'playback' : playback_devices,
        'recording' : recording_devices,
        'pointer' : device_pointer_dict
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
    quiet_run_process(soundvolumeview_path + f" /{command} {device.id} {params}")

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
        soundvolumeview("SetPlaybackThroughDevice", record_device, playback_device.id, soundvolumeview_path)
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
    def enable(cls, device):
        enable_device(device, cls.SoundVolumeView_path)
    
    @classmethod
    def disable(cls, device):
        disable_device(device, cls.SoundVolumeView_path)
    
    @classmethod
    def restart(cls, device):
        restart_device(device, cls.SoundVolumeView_path)
    
    @classmethod
    def set_playback_through(cls, enable, record_device, playback_device):
        set_playback_through(enable, record_device, playback_device, cls.SoundVolumeView_path)


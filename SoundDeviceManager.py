from tools import *
from logger import *

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
        
        program_log.info(f"setting playback through for {record_device['name']} to {playback_device['name']}")
        
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
            set_playback_through(enable, record_device, playback_work_device, cls.SoundVolumeView_path)
            print(f"{record_device.id} | {record_device.FriendlyName} will playback through {playback_work_device.FriendlyName}")
    
    @classmethod
    def list_devices(cls, key):
        program_log.debug(f"Listing devices with key {key}")
        available_keys = ["playback", "recording", "pointer"]
        if key not in available_keys :
            raise Exception(f"la clé doit être une des suivantes : {elem for elem in available_keys}")
        return [elem.FriendlyName for elem in cls.devices[key]]

    @staticmethod
    def is_active(device):
        program_log.info(f"checking if {device.FriendlyName} --- {device.id} --- is active")
        # https://docs.microsoft.com/en-us/windows/win32/coreaudio/device-state-xxx-constants
        
        program_log.debug(f"device state : {device.state.value}")
        
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

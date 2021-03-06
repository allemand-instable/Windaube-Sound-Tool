from windaube_sound_tool.SoundDeviceManager import SoundDeviceManager
from inquirer2 import Separator        
from windaube_sound_tool.logger import *

class DeviceList():
    
    ALL = 0
    ALREADY_ACTIVE = 1 
    ALREADY_DISABLED = 2 
    
    disabled_text_list = [ None, "Already active", "Already disabled" ]

    correct_device_types = [
        ["recording"],
        ["playback"],
        ["playback", "recording"],
        ["recording", "playback"]
    ]
    
    USAGE_NORMAL = 0
    USAGE_CHECKBOX = 1
    
    def __init__(self) -> None:
        pass
    
    @classmethod
    def get_list(cls, device_type, condition : int) -> list:
        program_log.info("Getting device list [DeviceList.get_list]")
        final_list = []
        
        for type in device_type :
            
            if device_type not in cls.correct_device_types :
                raise TypeError(f"device_type must be one of {cls.correct_device_types}")
        
            device_prefix = f"[{type[0]}]  "

            block = list(dict.fromkeys([device_prefix + device.FriendlyName for device in SoundDeviceManager.devices[type] if cls.device_condition(device, condition)]))
            
            final_list += block
            
        return final_list





    @classmethod
    def get_checkbox_list(cls, device_type : list[str], disable_device_checkbox_if : int = ALL, include_separator : bool = True) -> list:
        """Returns list of devices with a separator for the desired category for checkbox operation
        
        list returned :
        [
            separator,
            ---------
            dict[device name, checkbox status]
        ]
        """
        program_log.info("Getting device list for checkboxed [DeviceList.get_checkbox_list]")
        if device_type not in cls.correct_device_types :
            raise TypeError(f"device_type must be one of {cls.correct_device_types}")
        
        final_list = []
        
            
        
        for type in device_type :
            device_list : list = []
            program_log.debug( f"device_list est une list : {isinstance(device_list, list)}")
            program_log.debug(f"\n\n\nType : {type}")
            # recording -> [r]
            # playback -> [p]
            device_prefix = f"[{type[0]}]  "
            program_log.debug(f"setting device prefix to : \"{device_prefix}\"")
            program_log.debug("\n\nCreating the device list...")
            
            for device in SoundDeviceManager.list_devices(type) : 
                
                # disables checkbox based on the condition
                
                device_name = device_prefix + device
                program_log.debug(f"\n\ndevice_name : \"{device_name}\"")
                device_obj = SoundDeviceManager.devices["by_name"][device_name]
                
                program_log.debug(f"getting device object from name, using SDM.devices[by_name][name] : {device_obj}")
             
                condition_check = cls.device_condition( device_obj , disable_device_checkbox_if, cls.USAGE_CHECKBOX)
             
                program_log.debug(f"condition_check : {condition_check}")
             
                if condition_check is None :
                    program_log.debug("The device list's devices are not in the same state, skipping it...")
                    pass
                
                else :
                    if condition_check is True :
                        added = {   'name' : device_prefix  + device, 
                                    'checked' : False, 
                                    'disabled' : cls.disabled_text_list[disable_device_checkbox_if] 
                                }
                    elif condition_check is False :
                        added = {   'name' : device_prefix  + device, 
                                    'checked' : False
                                }
                
                    program_log.debug(f"added : {added}")
                
                    program_log.debug("Checking if the device is already in the list...")
                    if added not in device_list :
                        program_log.debug(f"{device} is not in the list, adding it...")
                        program_log.debug( f"device_list est une list : {isinstance(device_list, list)}")
                        device_list.append(added)
            
            
            # if you don't want the separator
            program_log.debug("Adding the separator...")
            if include_separator is True :
                sep = [Separator( type.capitalize() + " devices")]
                block = sep + device_list
            else :
                block = device_list
            
            program_log.debug(f"block [final] : {pformat(block)}")
            
            program_log.debug("Adding the block to the final list...")
            final_list += block
        
        program_log.debug("Result list :")
        program_log.debug(pformat(final_list))
        
        return final_list



    @staticmethod
    def device_list_same_state(device_list):
        program_log.debug("Checking if all devices inside the list are in the same state")
        if type(device_list) is list :
            program_log.debug(f"device argument is a list, of length {len(device_list)}")
            for device in device_list :
                program_log.debug( f"device state value of {device.id} : {device.state.value}"  )
            program_log.debug(f"device list : {device_list}")
            program_log.debug(f"Checking if all state values of the device {device_list[0].FriendlyName} are the same...")
            
            if len(device_list) > 1 :
                all_same_cond_list = [device_list[k].state.value == device_list[k+1].state.value  for k in range(len(device_list) - 1 )]
                all_same_state = all( all_same_cond_list )
                program_log.debug(f"condition list : {all_same_cond_list}")
            else :
                all_same_state = True

            program_log.debug(f"AND operator on list : {all_same_state}")
        else :
            program_log.debug(f"device argument's type is {type(device_list)}")
            return True
        return all_same_state


    @classmethod
    def device_condition(cls, device_list : list, condition : int, usage : int = USAGE_NORMAL) -> bool:
        program_log.debug(f"Checking device list condition [DeviceList.device_condition]")
        if not isinstance(device_list, list):
            program_log.debug(f"device_list is not a list, passing it to device_condition_single directly...")
            value = cls.device_condition_single(device_list, condition, usage)
        else :
            # ifall devices are in the same state, check for condition
            if DeviceList.device_list_same_state(device_list) :
                program_log.debug("All devices in the list are in the same state, checking condition...")
                value = cls.device_condition_single(device_list[0], condition, usage)
            # if not all the devices are in the same state, we discard the list : None
            else :
                value = None
        program_log.debug(f"Returning value : {value}")
        return value
    
    @classmethod
    def device_condition_single(cls, device, condition : int, usage : int = USAGE_NORMAL) -> bool:
        """Returns the condition checker for the disable checkbox"""
        program_log.debug(f"Checking device condition : {usage} [DeviceList.device_condition_single] for device {device.FriendlyName}")
        if condition == cls.ALL :
            # for normal usage we want to return True for all devices, to include them all
            if usage == cls.USAGE_NORMAL :
                return True
            # for checkboxes, we want don't want to disable the checkbox when we look for all devices
            elif usage == cls.USAGE_CHECKBOX :
                return False
            else :
                raise TypeError(f"usage must be one of {cls.USAGE_NORMAL} or {cls.USAGE_CHECKBOX}")
        elif condition == cls.ALREADY_ACTIVE :
            return SoundDeviceManager.is_active(device)
        elif condition == cls.ALREADY_DISABLED :
            return not SoundDeviceManager.is_active(device)
        else :
            raise Exception(f"Unknown value for disable_device_checkbox_if : {condition}")
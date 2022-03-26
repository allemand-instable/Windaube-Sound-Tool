from tools import SoundDeviceManager
from pprint import pprint

device_list = SoundDeviceManager.devices
SoundDeviceManager.update_devices()

print("recording")

pprint(
    [ (k, device_list["recording"][k].FriendlyName) for k in range(len(device_list["recording"]))]
)

print("playback")

pprint(
    [ (k, device_list["playback"][k].FriendlyName) for k in range(len(device_list["playback"]))]
)

working_devices = [elem for elem in device_list["recording"] if "Line" in elem.FriendlyName and "(Virtual Audio Cable)" in elem.FriendlyName]

for device in working_devices :
    SoundDeviceManager.set_playback_through(enable = True, record_device= device, playback_device=device_list["playback"][15])
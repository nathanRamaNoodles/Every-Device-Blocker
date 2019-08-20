from Netgear_access_control import NetgearRouter

my_router = NetgearRouter(username="admin", password="", headless=False)
my_router.connect_to_website()
print("Un-blocking Everyone :)")
my_router.allow_block_devices(device_array=None, select_all_except=True, topic=None, block=False) # allow all devices
my_router.allow_block_devices(device_array=None, select_all_except=True, topic=None, block=False) # finally, if any device managed to change online state during the previous command, allow it again

my_router.close()

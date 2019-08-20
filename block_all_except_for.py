from Netgear_access_control import NetgearRouter

my_router = NetgearRouter(username="admin", password="", headless=False)
my_router.connect_to_website()

# this is a list of devices that will be allowed internet.  Everyone else who doesn't match will be blocked.
devices_to_select = ["chromecast", "192.168.0.26"
                                   "Nathans-s7-phone", "raspberrypi",
                     "30:b5:c2:69:1f:c7", "Galaxy-Note8"]

# This "topics" list tells the script whether your "devices_to_select" list contains hostnames, IP addresses,
# and mac addresses. In this case, we have all of them.
topics = [my_router.topic_name, my_router.topic_ip, my_router.topic_mac_address]
print("Blocking Everyone except:", devices_to_select)

my_router.allow_block_devices(device_array=devices_to_select, topic=topics, block=False)  # first allow devices in list
my_router.allow_block_devices(device_array=devices_to_select, select_all_except=True,
                              topic=topics,
                              block=True)  # now block all devices that are online and offline that don't match our list
my_router.allow_block_devices(device_array=devices_to_select, topic=topics,
                              block=False)  # finally, if any device managed to change online state during the previous command, allow it again
my_router.close()

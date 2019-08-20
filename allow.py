from Netgear_access_control import NetgearRouter

my_router = NetgearRouter(username="admin", password="", headless=False)
my_router.connect_to_website()

# this is a list of devices that will be allowed.
devices_to_select = ["192.168.0.11", "raspberrypi", "innocent-dude"]

# This "topics" list tells the script whether your "devices_to_select" list contains hostnames, IP addresses,
# and mac addresses. In this case, we have 2 of them.
topics = [my_router.topic_name, my_router.topic_ip]
print("Allowing:", devices_to_select)

my_router.allow_block_devices(device_array=devices_to_select, topic=topics,
                              block=False)  # now allow all devices that are online and offline that match our list
my_router.close()

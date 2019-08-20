from Netgear_access_control import NetgearRouter

my_router = NetgearRouter(username="admin", password="")
my_router.connect_to_website()
# print(my_router.get_offline_white_list())
# print(my_router.get_offline_white_list())
print(my_router.get_online_list())


devices_to_test = ["--"]
topics = [my_router.topic_name, my_router.topic_ip, my_router.topic_mac_address]
subtract_entry = my_router.get_online_list()
entry = {}
print("Finding matches")
row_len = len(subtract_entry)
increment = 0
while increment < row_len:
    for j in devices_to_test:
        for ext_topic in topics:
            try:
                value = subtract_entry[increment][ext_topic]
                if j in value.lower():
                    entry[increment] = subtract_entry[increment]
                    subtract_entry.pop(increment)
                    # row_len -= 1
                    # increment -= 1
            except KeyError:
                pass
    increment += 1
print(entry)
print("Finding differences")
print(subtract_entry)

my_router.close()

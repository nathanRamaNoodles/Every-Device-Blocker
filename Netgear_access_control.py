import threading
import socket
import re
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException, StaleElementReferenceException, NoSuchElementException, \
    TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import platform

timeout = 4
# path to Chrome self.driver
if platform.system() == "Linux":
    pathToDriver = "/usr/bin/chromedriver"
else:
    pathToDriver = "C:\Windows\chromedriver.exe"
# chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--test-type")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=660,1080")
ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)

table_array = [
    {
        'id': "online_list_table",
        'structure': ['checkbox', 'status', 'name', 'ip', 'mac', 'connection_type']
    },
    {
        'id': "offline_white_list_table",
        'structure': ['checkbox', 'name', 'mac', 'connection_type']
    },
    {
        'id': "offline_black_list_table",
        'structure': ['checkbox', 'name', 'mac', 'connection_type']
    }
]


class NetgearRouter:
    def __init__(self, username, password, path="/AccessControl.htm", ip=None, domain="routerlogin.net",
                 headless=True):
        self.headless_mode = headless
        self.netgear_chrome_options = chrome_options
        if self.headless_mode:
            self.netgear_chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path=pathToDriver, chrome_options=self.netgear_chrome_options)
        self.url = "http://" + username + ":" + password + "@" + (ip if ip is not None else domain)
        self.path = path
        self.topic_ip = "ip"
        self.topic_connection_type = "connection_type"
        self.topic_name = "name"
        self.topic_status = "status"
        self.topic_mac_address = "mac"

    def connect_to_website(self):
        self.driver.get(str(self.url + self.path))
        if "MultiLogin.htm" in self.driver.current_url:
            print("Trying to avoid login screen")
            self.driver.execute_script("yesClick(); setTimeout(function () {window.location.replace(\"" + str(
                self.url + self.path) + "\");}, 10);")
            self.avoid_stale_exception()
        self.toggle_collapsibles()

    def close(self):
        self.driver.quit()

    def run_allow_block_devices(self, device_array, select_all=False, topic=None, block=True):
        if topic is None:
            topic = ["name"]
        thread = threading.Thread(target=self.allow_block_devices, args=(device_array, select_all, topic, block))
        thread.start()  # Start the execution

    def run_connect_to_website(self):
        thread = threading.Thread(target=self.connect_to_website(), args=())
        thread.start()  # Start the execution

    @staticmethod
    def get_ip_addresses():
        addrList = socket.getaddrinfo(socket.gethostname(), None)

        ipList = []
        for item in addrList:
            if ':' not in item[4][0] and item[4][0] not in ipList:
                ipList.append(item[4][0])
        ipList.append(socket.gethostname())

        return ipList

    def allow_block_devices(self, device_array, select_all_except=False, topic=None, block=True):
        if topic is None:
            topic = ["name", "ip"]
        else:
            if "name" not in topic:
                topic.append("name")
            if "ip" not in topic:
                topic.append("ip")
        if not select_all_except:
            if block:
                subtract_entry = [e for e in device_array for i in self.get_ip_addresses() if e in i]
                new_entry = list(set(device_array) - set(subtract_entry))
                self.select_devices(device_names=new_entry, topic=topic, table=0)
            else:
                self.select_devices(device_names=device_array + self.get_ip_addresses(), topic=topic, table=0)
        else:
            self.select_all(table=0)
            if block:
                self.select_devices(device_array + self.get_ip_addresses(), topic=topic, check=False, table=0)

        self.update_online_allow_block_status(block=block)
        if block:
            if not select_all_except:
                subtract_entry = [e for e in device_array for i in self.get_ip_addresses() if e in i]
                new_entry = list(set(device_array) - set(subtract_entry))
                # print("blocking these devices:", new_entry)
            else:
                new_entry = device_array + self.get_ip_addresses()
                # print("avoiding these devices:", new_entry)
            self.select_devices(device_names=new_entry, topic=topic, table=1, invert=select_all_except)
        else:
            self.select_devices(device_names=device_array, topic=topic, table=2, invert=select_all_except)

    def _get_list(self, table):
        self.toggle_collapsibles()

        result = defaultdict(dict)
        parentElement = self.driver.find_element_by_id(table_array[table]['id'])
        childElement = parentElement.find_element_by_tag_name("tbody")
        # rowList = childElement.find_elements_by_tag_name("tr")
        newline_list_array = str(childElement.text).splitlines()
        for index, i in enumerate(newline_list_array):
            if table == 0:
                p = re.search('^(\w*)\s*(.*?(?=\s))\s*(\d+\.\d+\.\d+\.\d+)\s*(.*?(?=\s))\s*(\w*)', i)
            else:
                p = re.search('^(.*?(?=\s))\s*(\w+\:\w+\:\w+\:\S*)\s*(\S*)', i)
            for col in range(1, len(table_array[table]['structure'])):
                result[index][table_array[table]['structure'][col]] = p.group(col)
        return dict(result)

    def get_online_list(self):
        return self._get_list(table=0)

    def get_offline_white_list(self):
        return self._get_list(table=1)

    def get_offline_black_list(self):
        return self._get_list(table=2)

    def toggle_collapsibles(self, open_collapsible=True):
        collapsible = self.driver.find_element_by_id("white_list_body")
        if (collapsible.value_of_css_property('display') == "block") != open_collapsible:
            self.driver.execute_script("handle_white_list_table();")
        collapsible = self.driver.find_element_by_id("black_list_body")
        if (collapsible.value_of_css_property('display') == "block") != open_collapsible:
            self.driver.execute_script("handle_black_list_table();")

    def select_all(self, table=0, check=True):
        parentElement = self.driver.find_element_by_id(table_array[table]['id'])
        childElement = parentElement.find_element_by_tag_name("thead")
        rowList = childElement.find_elements_by_tag_name("tr")
        columnList = rowList[0].find_elements_by_tag_name("td")
        checkbox = columnList[0].find_element_by_tag_name("input")
        if check != checkbox.is_selected():
            checkbox.click()

    def select_devices(self, device_names, topic=None, table=0, check=True, invert=False):
        if topic is None:
            topic = ["name"]
        try:
            device_names_lowercase = [x.lower() for x in device_names]
        except TypeError:
            device_names_lowercase = None

        subtract_entry = {}

        def get_live_list():
            nonlocal subtract_entry
            subtract_entry = self._get_list(table)
            entry = {}
            row_len = len(subtract_entry)
            increment = 0
            if device_names_lowercase is not None:
                while increment < row_len:
                    for j in device_names_lowercase:
                        for ext_topic in topic:
                            try:
                                value = subtract_entry[increment][ext_topic]
                                if j in value.lower():
                                    entry[increment] = subtract_entry[increment]
                                    subtract_entry.pop(increment)
                            except KeyError:
                                pass
                    increment += 1
            # print("Matches")
            # print(entry)
            # print("Finding differences")
            # print(subtract_entry)
            return entry

        def checkbox_clicker(device_array):
            if table in {1, 2}:
                if "ip" in topic:
                    topic.remove("ip")

            if device_array:
                for i in range(0, len(device_array)):
                    checkbox = self.driver.find_element_by_xpath(
                        '//*[@id="' + table_array[table]['id'] + '"]/tbody/tr[' + str(
                            list(device_array)[i] + 1) + ']/td[1]/input')
                    if check != checkbox.is_selected():
                        checkbox.click()
                    if checkbox.is_selected():
                        if table != 0:
                            self.edit_device(table)
                            new_en = get_live_list()
                            return checkbox_clicker(
                                device_array=new_en if not invert else subtract_entry)

        new_entry = get_live_list()
        try:
            checkbox_clicker(device_array=new_entry if not invert else subtract_entry)
        except NoSuchElementException:
            pass

    def edit_device(self, table):
        if table in {1, 2}:
            # print("Editing device")
            edit_btn = self.driver.find_element_by_id("edit_white" if table == 1 else "edit_black")
            edit_btn.click()
            select = Select(WebDriverWait(self.driver, timeout, ignored_exceptions=ignored_exceptions).until(
                expected_conditions.presence_of_element_located((By.ID, "access_control_option"))))

            select.select_by_visible_text('Allow' if table == 2 else 'Block')
            apply_btn = self.driver.find_element_by_xpath('//*[@id="target"]/table/tbody/tr[1]/td/button[1]')
            apply_btn.click()

            try:
                WebDriverWait(self.driver, 6.0).until(
                    expected_conditions.visibility_of_element_located((By.ID, table_array[0]['id'])))
                # print("Found Element")
            except TimeoutException:
                print("Refreshing")
                self.driver.refresh()
            self.toggle_collapsibles()

    def avoid_stale_exception(self):
        WebDriverWait(self.driver, timeout + 10, ignored_exceptions=ignored_exceptions).until(
            expected_conditions.visibility_of_element_located((By.ID, table_array[0]['id'])))
        self.toggle_collapsibles()

    def update_online_allow_block_status(self, block):
        allow_block_btn = self.driver.find_element_by_id("block" if block else "allow")
        allow_block_btn.click()
        try:
            self.driver.switch_to.alert.accept()
        except NoAlertPresentException:
            pass

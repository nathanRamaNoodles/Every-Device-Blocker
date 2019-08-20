# Every-Device-Blocker
Blocks internet for **every single** offline/online device on your network that you are skeptical about....Or use it to control your brother's Fornite/video-game playtime :D

[You can even block a **specific brand of devices**](#which-script-to-use), such as "android", "ubuntu" or "raspberrypi" if you don't know their IP address, hostname, or mac address!

**Scripts can take as fast as 10 seconds to 1.5 minutes depending on size of offline devices and your computer's specs**

## Table of Contents
- [Every-Device-Blocker](#every-device-blocker)
  - [Why?](#why)
    - [Reason](#reason)
    - [The real reason](#the-real-reason)
  - [Materials](#materials)
  - [Installation](#installation)
  - [Which script to use?](#which-script-to-use)
  - [License](#license)

### Why?
+ #### Reason
  + Because I want to control who has internet in my network,
and I want to prevent hackers from using my internet.

+ #### The real reason
  + My little brother plays this toxic game called "Fornite" for 8-10 hours a day, and I became worried about it becoming an addiction.  So I decided to make a script that would go into my router and block his Xbox.  However, my little brother also watched fortnite videos on his android tablet.  So I pulled out the big guns and revised my script to block every device that isn't mine.  I set it on an interval on a raspberrypi with crontab and it works nicely.

  + It's been a month since the script ran, and it works beautifully.  He now plays only 3-4 hours a day :)


### Materials
1. **A [Netgear Router that allows Mac filtering](https://kb.netgear.com/24686/Which-NETGEAR-home-router-models-can-I-manage-using-the-NETGEAR-genie-app)**
2. Router's password
3. Your device's IP/mac-address/hostname

### Installation
1. Make sure that you have a recent version of Python 3.x installed (preferably
  3.6 or greater)
2. Make sure that you have Google Chrome installed and that it is up to date
3. Install the chromedriver for Selenium. See [here](https://sites.google.com/a/chromium.org/chromedriver/home) for an explanation of what the chromedriver does.
   + For Windows, place your driver in `C:\Windows\chromedriver.exe`
   + For linux, place your driver in `/usr/bin/chromedriver`
   + For Mac...I don't know cause I don't have a Mac :\
4. Open project directory and type in terminal `pip3 install -r requirements.txt`
5. To run a script, call `python3 allow.py` or any other script depending on what you want.  Remember to set the password in the script before you run it.
6. For headless mode, simply remove `headless=False` in the script.

### Which script to use?
There are many scenarios where you can call these scripts:
1. Block all android/ubuntu/unknown devices
  1. run `block_all_except_for.py` and edit `devices_to_select` array to : `["ubuntu", "android", "--"]`
2. Your little brother is playing Fortnite for 8 hours straight.
So instead of unplugging the router and disconnecting everyone,
you can block just your brother:
   + Use `block.py` and `allow.py`, and edit the `devices_to_select` array
   to add your brother's hostname/IP/mac.
     + To block, simply call `block.py`
     + To allow, simply call `allow.py`

3. You have a neighbor who is using your internet without you knowing:
   1. Open `block_all_except_for.py` and edit `devices_to_select` array
   to add all devices you know you own, like "Nathans-s7-phone" and "raspberrypi".
   Though it is high recommened to use the mac address assigned to you device.
   You can check in your device's settings.
   2. Run `block_all_except_for.py`.  Now all devices will be blocked
   except the ones you specified.
4. Allow All
   1. run `allow_all.py` to give everyone internet


### License
```
GNU GENERAL PUBLIC LICENSE
   Version 3, 29 June 2007

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.

Rest of License found here: https://raw.githubusercontent.com/nathanRamaNoodles/Every-Device-Blocker/master/LICENSE
```

from __future__ import print_function
import time
import os
from activity import *
import json
import datetime
import sys
import win32gui
import uiautomation as auto
if sys.platform in ['linux', 'linux2']:
        import linux as l

active_window_name = ""
activity_name = ""
start_time = datetime.datetime.now()
activeList = AcitivyList([])
first_time = True
json_directory = r"C:\Users\asus\Desktop\Saving-time\analys_work\json"
json_filename = os.path.join(json_directory, 'activities.json')


def url_to_name(url):
    string_list = url.split('/')
    return string_list[2]


def get_active_window():
    _active_window_name = None
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        _active_window_name = win32gui.GetWindowText(window)
    else:
        print("sys.platform={platform} is not supported."
              .format(platform=sys.platform))
        print(sys.version)
    return _active_window_name


def get_chrome_url():
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        chromeControl = auto.ControlFromHandle(window)
        edit = chromeControl.EditControl()
        return 'https://' + edit.GetValuePattern().Value

def extract_app_name(window_title):
    separators = [' - ', ' | ', ' :: ', ' – ']
    for separator in separators:
        if separator in window_title:
            return window_title.split(separator)[-1].strip()
    return window_title

try:
    activeList.initialize_me()
except Exception:
    print('No json')

try:
    while True:
        previous_site = ""
        if sys.platform not in ['linux', 'linux2']:
            new_window_name = get_active_window()
            if 'Google Chrome' in new_window_name:
                new_window_name = url_to_name(get_chrome_url())
        if sys.platform in ['linux', 'linux2']:
            new_window_name = l.get_active_window_x()
            if 'Google Chrome' in new_window_name:
                new_window_name = l.get_chrome_url_x()

        if active_window_name != new_window_name:
            end_time = datetime.datetime.now()
            time_entry = TimeEntry(start_time, end_time, 0, 0, 0)  # Remove 'days' field
            time_entry._get_specific_times()

            activity_found = False
            for activity in activeList.activities:
                if activity.name == activity_name:
                    activity_found = True
                    # Update existing activity's time entries
                    activity.time_entries.append(time_entry)
                    break

            if not activity_found:
                activity = Activity(activity_name, [time_entry])
                activeList.activities.append(activity)

            active_window_name = new_window_name
            activity_name = extract_app_name(active_window_name)  # Assign the correct activity name

            with open(json_filename, 'w') as json_file:
                json.dump(activeList.serialize(), json_file,
                          indent=4, sort_keys=True)
                start_time = datetime.datetime.now()

            first_time = False

        time.sleep(1)
except KeyboardInterrupt:
    with open(json_filename, 'w') as json_file:
        json.dump(activeList.serialize(), json_file, indent=4, sort_keys=True)
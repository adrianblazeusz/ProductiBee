from __future__ import print_function
import time
import os
from activity import *
import json
import datetime
import sys
import win32gui
import uiautomation as auto

active_window_name = ""
activity_name = ""
start_time = datetime.datetime.now()
activeList = AcitivyList([])
first_time = True
json_file_path = json_file_path = r"C:\Users\asus\Desktop\Saving-time\analys_work\json\activities.json"


def url_to_name(url):
    string_list = url.split('/')
    return string_list[2]


def get_active_window():
    window = win32gui.GetForegroundWindow()
    _active_window_name = win32gui.GetWindowText(window)
    return _active_window_name


def get_chrome_url():
    window = win32gui.GetForegroundWindow()
    chromeControl = auto.ControlFromHandle(window)
    edit = chromeControl.EditControl()
    return 'https://' + edit.GetValuePattern().Value

def extract_app_name(window_title):
    separators = [' - ', ' | ', ' :: ', ' – ']  # Add other possible separators
    for separator in separators:
        if separator in window_title:
            return window_title.split(separator)[-1].strip()
    return window_title

try:
    activeList.initialize_me()
except Exception:
    print('No json')

existing_data = {"activities": []}
if os.path.exists(json_file_path):
    with open(json_file_path, 'r') as json_file:
        existing_data = json.load(json_file)

try:
    while True:
        new_window_name = get_active_window()
        if 'Google Chrome' in new_window_name:
            new_window_name = url_to_name(get_chrome_url())

        app_name = extract_app_name(new_window_name)

        if active_window_name != app_name:
            if not first_time:
                end_time = datetime.datetime.now()
                time_spent = (end_time - start_time).seconds

                exists = False
                for activity in activeList.activities:
                    if activity.name == app_name:
                        exists = True
                        if time_spent >= 60:
                            activity.time_entries[-1].end_time = end_time
                            activity.time_entries[-1]._get_specific_times()

                if not exists:
                    activity = Activity(app_name, [TimeEntry(start_time, end_time, 0, 0, 0, 0)])
                    activeList.activities.append(activity)

            # Update existing JSON data with new entries
            existing_data['activities'].extend(activeList.activities_to_json())

            # Write the updated data back to the JSON file
            with open(json_file_path, 'w') as json_file:
                json.dump(existing_data, json_file, indent=4, sort_keys=True)

            first_time = False
            active_window_name = app_name
            start_time = datetime.datetime.now()

        time.sleep(1)

except KeyboardInterrupt:
    # Zmiana ścieżki zapisu pliku JSON
    json_file_path = r"C:\Users\asus\Desktop\Saving-time\analys_work\json\activities.json"
    with open(json_file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4, sort_keys=True)
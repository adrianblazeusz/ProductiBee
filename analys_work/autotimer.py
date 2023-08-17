from __future__ import print_function
import time
import os
import analys_work.activity as an
import json
import datetime
import sys
import win32gui
import uiautomation as auto
from utils import get_base_path


class Autotimer:

    def __init__(self):
        
        self.active_window_name = ""
        self.activity_name = ""
        self.start_time = datetime.datetime.now()
        self.activeList = an.AcitivyList([])
        self.first_time = True
        self.json_filename = os.path.join(get_base_path(), 'analys_work\\json\\activities.json')
        
        self.analys_running = True


    def load_existing_data(self):
        try:
            with open(self.json_filename, 'r') as json_file:
                existing_data = json.load(json_file)
                self.activeList.activities = existing_data.get('activities', [])
        except FileNotFoundError:
            pass 

    def url_to_name(self, url):
        string_list = url.split('/')
        return string_list[2]


    def get_active_window(self):
        _active_window_name = None
        if sys.platform in ['Windows', 'win32', 'cygwin']:
            window = win32gui.GetForegroundWindow()
            _active_window_name = win32gui.GetWindowText(window)
        else:
            print("sys.platform={platform} is not supported."
                .format(platform=sys.platform))
            print(sys.version)
        return _active_window_name

    def delete_data(self):

        with open(self.json_filename, 'w') as json_file:
                json.dump(self.activeList.serialize(), json_file, indent=4, sort_keys=True)


    def get_chrome_url(self):
        if sys.platform in ['Windows', 'win32', 'cygwin']:
            window = win32gui.GetForegroundWindow()
            chromeControl = auto.ControlFromHandle(window)
            edit = chromeControl.EditControl()
            return 'https://' + edit.GetValuePattern().Value

    def extract_app_name(self, window_title):  
        separators = [' - ', ' | ', ' :: ', ' – ']
        for separator in separators:
            if separator in window_title:
                return window_title.split(separator)[-1].strip()
        return window_title

    def start_analys(self):
        self.analys_running = True
        self.activeList = an.AcitivyList([])  # Tworzenie nowej pustej listy aktywności
        self.delete_data()  # Czyszczenie pliku JSON

        try:
            active_window_name = "" 
            activity_name = ""  
            start_time = datetime.datetime.now()  

            while self.analys_running:
                    self.previous_site = ""
                    new_window_name = self.get_active_window()

                    if sys.platform in ['Windows', 'win32', 'cygwin']:
                        if 'Google Chrome' in new_window_name:
                            new_window_name = self.get_chrome_url()

                    if active_window_name != new_window_name:
                        end_time = datetime.datetime.now()
                        time_entry = an.TimeEntry(start_time, end_time, 0, 0, 0)  
                        time_entry._get_specific_times()

                        activity_found = False
                        for activity in self.activeList.activities:
                            if activity.name == activity_name:
                                activity_found = True
                                # Update existing activity's time entries
                                activity.time_entries.append(time_entry)
                                break

                        if not activity_found:
                            activity = an.Activity(activity_name, [time_entry])
                            self.activeList.activities.append(activity)

                        active_window_name = new_window_name
                        activity_name = self.extract_app_name(active_window_name) 

                        with open(self.json_filename, 'w') as json_file:
                            json.dump(self.activeList.serialize(), json_file,
                                    indent=4, sort_keys=True)
                            start_time = datetime.datetime.now()

                        self.first_time = False

                        time.sleep(1)
        except KeyboardInterrupt:
            with open(self.json_filename, 'w') as json_file:
                json.dump(self.activeList.serialize(), json_file, indent=4, sort_keys=True)

    def stop_analys(self):
        self.analys_running = False

        with open(self.json_filename, 'w') as json_file:
            json.dump(self.activeList.serialize(), json_file, indent=4, sort_keys=True)
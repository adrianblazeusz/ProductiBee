import time
import os
import json
import datetime
import threading
import win32gui
import analys_work.activity as an

class Autotimer:
    def __init__(self):
        self.active_window_name = ""
        self.activity_name = ""
        self.start_time = datetime.datetime.now()
        self.activeList = an.AcitivyList([])
        self.first_time = True
        self.json_file_path = r"C:\Users\asus\Desktop\Saving-time\analys_work\json\activities.json"
        self.stop_auto_timer_event = threading.Event()
        self.auto_timer_thread = None

    def url_to_name(self, url):
        string_list = url.split('/')
        return string_list[2]

    def get_active_window(self):
        window = win32gui.GetForegroundWindow()
        _active_window_name = win32gui.GetWindowText(window)
        return _active_window_name

    def extract_app_name(self, window_title):
        separators = [' - ', ' | ', ' :: ', ' – ']
        for separator in separators:
            if separator in window_title:
                return window_title.split(separator)[-1].strip()
        return window_title

    def start_auto_timer(self):
        def auto_timer_loop():
            existing_data = {"activities": []}

            if os.path.exists(self.json_file_path):
                with open(self.json_file_path, 'r') as json_file:
                    existing_data = json.load(json_file)

            unique_app_names = set()
            active_window_name = ""
            start_time = datetime.datetime.now()
            activeList = an.AcitivyList([])

            try:
                activeList.initialize_me()
            except Exception:
                print('No json')

            while not self.stop_auto_timer_event.is_set():
                new_window_name = self.get_active_window()
                app_name = self.extract_app_name(new_window_name)

                if app_name not in unique_app_names:
                    unique_app_names.add(app_name)

                    if active_window_name != app_name:
                        if not self.first_time:
                            end_time = datetime.datetime.now()
                            time_spent = (end_time - start_time).seconds

                            exists = False
                            for activity in activeList.activities:
                                if activity.name == app_name:
                                    exists = True
                                    if time_spent >= 60:
                                        activity.time_entries[-1].end_time = end_time
                                        activity.time_entries[-1]._get_specific_times()

                            if not exists and time_spent >= 60:
                                activity = an.Activity(app_name, [an.TimeEntry(start_time, end_time, 0, 0, 0, 0)])
                                activeList.activities.append(activity)

                            existing_data['activities'].extend(activeList.activities_to_json())

                            try:
                                with open(self.json_file_path, 'w') as json_file:
                                    json.dump(existing_data, json_file, indent=4, sort_keys=True)
                                    print("Data saved:", existing_data)
                            except Exception as e:
                                print("Error while saving data:", e)

                            self.first_time = False
                            active_window_name = app_name
                            start_time = datetime.datetime.now()

                time.sleep(1)

                try:
                    activeList.initialize_me()
                except Exception:
                    print('No json')

        self.auto_timer_thread = threading.Thread(target=auto_timer_loop)
        self.auto_timer_thread.start()

    def stop_auto_timer(self):
        self.stop_auto_timer_event.set()
        self.auto_timer_thread.join()
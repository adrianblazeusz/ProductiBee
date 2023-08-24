import json
from datetime import timedelta
import os
import analys_work.activity


class Report:
     
    def __init__(self, json_filename=None):
            self.json_directory = "analys_work/json"
            self.json_filename = os.path.join(self.json_directory, 'activities.json')
            self.activity_times = {}

    def load_data(self):
        with open(self.json_filename, 'r') as json_file:
            self.data = json.load(json_file)

    def report(self):
        self.load_data()  # Load the latest data from the JSON file
        activity_times = {}

        for activity in self.data['activities']:
            activity_name = activity['name']

            if activity_name == "" or "\\" in activity_name or activity_name == "ProductiBee":
                continue

            total_time = timedelta()

            for entry in activity['time_entries']:
                time_entry = timedelta(
                    hours=entry['hours'],
                    minutes=entry['minutes'],
                    seconds=entry['seconds']
                )
                total_time += time_entry

            if total_time.total_seconds() >= 3:
                activity_times[activity_name] = total_time

        return activity_times
    
    def display_report(self, activity_times):
        separator = "\n-----------------------------------------------\n"


        for activity, time in activity_times.items():
            total_time_str = str(time)
            print("end", f"{activity}: {total_time_str}{separator}")

    def save_to_database(activity_data, session_id):

        db = activity.DatabaseManager()  # Initialize the database connection

        for activity in activity_data:
            app_name = activity.get('app_name')
            time_spent = activity.get('time_spent')
            
            # Insert the data into the database
            db.insert_activity(session_id, app_name, time_spent)

        db.close()

class ModifiedReport:
     
    def __init__(self, json_filename=None):
        self.json_directory = "analys_work/json"
        self.json_filename = os.path.join(self.json_directory, 'activities.json')
        self.activity_times = {}
        # Assuming you'll pass session_id when initializing the Report class
        self.session_id = None  # This should be passed when initializing the Report instance

    def load_data(self):
        with open(self.json_filename, 'r') as json_file:
            self.data = json.load(json_file)

    def report(self):
        self.load_data()  # Load the latest data from the JSON file
        activity_times = {}

        for activity in self.data['activities']:
            activity_name = activity['name']

            if activity_name == "" or "\\" in activity_name or activity_name == "ProductiBee":
                continue

            total_time = timedelta()

            for entry in activity['time_entries']:
                time_entry = timedelta(
                    hours=entry['hours'],
                    minutes=entry['minutes'],
                    seconds=entry['seconds']
                )
                total_time += time_entry

            if total_time.total_seconds() >= 3:
                activity_times[activity_name] = total_time

        # After generating the report, save the data to the database
        self.save_to_database(activity_times, self.session_id)

        # Clear the JSON file (or remove the data of the specific session)
        with open(self.json_filename, 'w') as json_file:
            json.dump({"activities": []}, json_file)

        return activity_times

    def display_report(self, activity_times):
        separator = "\n-----------------------------------------------\n"

        for activity, time in activity_times.items():
            total_time_str = str(time)
            print("end", f"{activity}: {total_time_str}{separator}")

    def save_to_database(self, activity_data, session_id):
        db = analys_work.activity.DatabaseManager()  # Initialize the database connection

        for activity_name, time in activity_data.items():
            time_spent = int(time.total_seconds())  # Convert time to seconds

            # Insert the data into the database
            db.insert_activity(session_id, activity_name, time_spent)

        db.close()

if __name__ == "__main__":
    repo = ModifiedReport()
    activity_times = repo.report()
    print(activity_times)
    disp = repo.display_report(activity_times)
    print(disp)
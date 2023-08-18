import json
from datetime import timedelta

class Report:

    def __init__(self, json_filename='analys_work/json/activities.json'):
        self.json_filename = json_filename
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

            if total_time.total_seconds() >= 15:
                activity_times[activity_name] = total_time

        return activity_times
    
    def display_report(self, activity_times):
        separator = "\n-----------------------------------------------\n"


        for activity, time in activity_times.items():
            total_time_str = str(time)
            print("end", f"{activity}: {total_time_str}{separator}")

if __name__ == "__main__":
    repo = Report()
    activity_times = repo.report()
    print(activity_times)
    disp = repo.display_report(activity_times)
    print(disp)
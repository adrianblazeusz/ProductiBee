import json
from datetime import timedelta

class Report:

    def __init__(self):
    # Wczytaj dane z pliku JSON
        self.json_filename = r'C:\Users\asus\Desktop\Saving-time\analys_work\json\activities.json'
        self.activity_times = {}

        with open(self.json_filename, 'r') as json_file:
                        self.data = json.load(json_file)

    def report(self):
        activity_times = {}

        for activity in self.data['activities']:
            activity_name = activity['name']

            if activity_name == "" or "\\"  in activity_name:
                continue

            total_time = timedelta()

            for entry in activity['time_entries']:
                time_entry = timedelta(
                    hours=entry['hours'],
                    minutes=entry['minutes'],
                    seconds=entry['seconds']
                )
                total_time += time_entry

            if total_time.total_seconds() >= 60:
                activity_times[activity_name] = total_time

        return activity_times

if __name__ == "__main__":
    repo = Report()    
    activity_times = repo.report()
    print(activity_times)

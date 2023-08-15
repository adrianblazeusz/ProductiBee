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
        # Przetwarzaj dane i sumuj czasy dla każdej aktywności
        for activity in self.data['activities']:
            activity_name = activity['name']

            # Pomijaj aktywności bez nazwy, aktywności związane z ścieżkami i aktywności o czasie mniejszym niż 1 minuta
            if activity_name == "" or "\\" in activity_name:
                continue

            total_time = timedelta()

            for entry in activity['time_entries']:
                time_entry = timedelta(
                    hours=entry['hours'],
                    minutes=entry['minutes'],
                    seconds=entry['seconds']
                )
                total_time += time_entry

            # Pomijaj aktywności o czasie mniejszym niż 1 minuta
            if total_time.total_seconds() >= 10:
                self.activity_times[activity_name] = total_time

        # Wyświetl raport
        print("Your last session went like this:")
        for activity_name, total_time in self.activity_times.items():
            formatted_time = str(total_time).split('.')[0]  # Format czasu: HH:MM:SS
            print(f"{activity_name}: {formatted_time}")


if __name__ == "__main__":
     repo = Report()
     test = repo.report()
     print(test)
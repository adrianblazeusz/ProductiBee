import json
from datetime import timedelta
import mysql.connector

class Report:"""
class create for convering .json in to report for app
"""

     
    def __init__(self, json_filename="analys_work/json/activities.json"):
        self.json_filename = json_filename

    def load_data(self):
        with open(self.json_filename, 'r') as json_file:
            return json.load(json_file)

    def report(self):
        data = self.load_data()
        activity_times = {}
        for activity in data['activities']:
            activity_name = activity['name']
            if activity_name in ["", "ProductiBee"] or "\\\\" in activity_name:
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
        id_timera = data.get('id_timera', None)
        return id_timera, activity_times

    def insert_into_database(self, id_timera, activity_times):
        config = {
            'user': 'root',
            'password': '',
            'host': 'localhost',
            'database': 'productibeeadvanced',
            'raise_on_warnings': True
        }

        try:
            with mysql.connector.connect(**config) as cnx:
                cursor = cnx.cursor()

                for app_name, time_duration in activity_times.items():
                    # Convert time duration to total seconds
                    total_seconds = time_duration.total_seconds()

                    add_data = ("INSERT INTO sessionactivities "
                                "(id_timera, app_name, time) "
                                "VALUES (%s, %s, %s)")
                    data = (id_timera, app_name, total_seconds)
                    cursor.execute(add_data, data)

                # Commit the transaction
                cnx.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

        return True

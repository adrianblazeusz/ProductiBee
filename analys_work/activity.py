#this code was based on https://github.com/KalleHallden/AutoTimer
import json
from dateutil import parser
import mysql.connector

class AcitivyList:
    def __init__(self, activities=[]):
        self.activities = activities
        self.db = DatabaseManager()
    
    def initialize_me(self):
        self.activities = self.db.fetch_all_activities()
        with open('activities.json', 'r') as f:
            data = json.load(f)
            for activity in data['activities']:
                self.activities.append(
                    Activity(
                        name=activity['name'],
                        time_entries=self.get_time_entires_from_json(activity)
                    )
                )
        return self.activities
    
    def get_activities_from_json(self, data):
        activities_list = []
        for activity in data['activities']:
            activities_list.append(
                Activity(
                    name=activity['name'],
                    time_entries=self.get_time_entires_from_json(activity),
                )
            )
        return activities_list
    
    def get_time_entires_from_json(self, data):
        time_entries_list = []
        for entry in data['time_entries']:
            time_entries_list.append(
                TimeEntry(
                    start_time=parser.parse(entry['start_time']),
                    end_time=parser.parse(entry['end_time']),
                    hours=entry['hours'],
                    minutes=entry['minutes'],
                    seconds=entry['seconds'],
                )
            )
        return time_entries_list
    
    def serialize(self):
        return {
            'activities': self.activities_to_json()
        }
    
    def activities_to_json(self):
        activities_ = []
        for activity in self.activities:
            activities_.append(activity.serialize())
        return activities_

class DatabaseManager:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",          # Assuming no password for XAMPP's MySQL root user
            database="productibeeadvanced"
        )
        self.cursor = self.conn.cursor()

    def fetch_all_activities(self):
        self.cursor.execute("SELECT * FROM sessionactivities")
        return self.cursor.fetchall()

    def insert_activity(self, user_id, session_id, app_name, time_spent):
        sql = """
        INSERT INTO sessionactivities (user_id, session_id, app_name, time_spent) 
        VALUES (%s, %s, %s, %s)
        """
        values = (user_id, session_id, app_name, time_spent)
        self.cursor.execute(sql, values)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

class Activity:
    def __init__(self, name, time_entries=[]):
        self.name = name
        self.time_entries = time_entries

    def serialize(self):
        return {
            'name': self.name,
            'time_entries': self.make_time_entires_to_json()
        }
    
    def make_time_entires_to_json(self):
        time_list = []
        for time in self.time_entries:
            time_list.append(time.serialize())
        return time_list

class TimeEntry:
    def __init__(self, start_time, end_time, hours, minutes, seconds):
        self.start_time = start_time
        self.end_time = end_time
        self.total_time = end_time - start_time
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
    
    def _get_specific_times(self):
        self.hours = self.total_time.seconds // 3600
        self.minutes = (self.total_time.seconds % 3600) // 60
        self.seconds = self.total_time.seconds % 60

    def serialize(self):
        return {
            'start_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'hours': self.hours,
            'minutes': self.minutes,
            'seconds': self.seconds
        }

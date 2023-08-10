import json
import os

# Zmiana ścieżki do pliku JSON na względną
json_file_path = os.path.join(os.path.dirname(__file__), 'json', 'activities.json')

try:
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        # Twój kod przetwarzania danych
except FileNotFoundError:
    print('No json')

# Funkcja do sprawdzania, czy aktywność to aplikacja lub strona internetowa
def is_application_or_website(name):
    return any(keyword in name.lower() for keyword in ['chrome', 'firefox', 'opera', 'explorer'])

# Filtruj aktywności, pozostawiając tylko aplikacje i strony internetowe
filtered_activities = []
for activity in data['activities']:
    if is_application_or_website(activity['name']):
        filtered_activities.append(activity)

# Ścieżka do folderu, w którym chcesz zapisać plik filtered_data.json
output_folder = r'C:\Users\asus\Desktop\Saving-time\analys_work\json'

# Utwórz folder, jeśli nie istnieje
os.makedirs(output_folder, exist_ok=True)

# Ścieżka do pliku filtered_data.json w podanej lokalizacji
output_path = os.path.join(output_folder, 'filtered_data.json')

# Zapisz przefiltrowane aktywności do pliku filtered_data.json
filtered_data = {'activities': filtered_activities}
with open(output_path, 'w') as json_file:
    json.dump(filtered_data, json_file, indent=4, sort_keys=True)
import plotly.express as px
import pandas as pd
import json 
json_path = r'C:\Users\asus\Desktop\Saving-time\analys_work\json\activities.json'

with open(json_path, 'r') as json_file:
    data = json.load(json_file)

activity_data = []
for activity in data["activities"]:
    total_time_minutes = sum(
        entry["days"] * 24 * 60 + entry["hours"] * 60 + entry["minutes"] + entry["seconds"] / 60
        for entry in activity["time_entries"]
    )
    if total_time_minutes > 5:  # Add this condition to filter activities with more than 5 minutes
        activity_data.append({"name": activity["name"], "total_time_minutes": total_time_minutes})

df = pd.DataFrame(activity_data)
df_sorted = df.sort_values(by="total_time_minutes", ascending=False)

# Tworzenie wykresu słupkowego
fig = px.bar(df_sorted, x="name", y="total_time_minutes", title="Czas spędzony na poszczególnych aktywnościach")
fig.update_xaxes(title_text="Aktywność", showticklabels=False, categoryorder="total descending")
fig.update_yaxes(title_text="Czas (minuty)", showticklabels=False)  # Ukrycie etykiet na osi Y
fig.update_layout(showlegend=False)  # Usunięcie legendy
fig.show()
import csv
import requests

# Replace 'YOUR_API_KEY' with your actual Google Maps API key
API_KEY = 'AIzaSyBUVW8eJLVVGkqU3wEiV17tOduPAaFnOxo'
BASE_URL = "https://maps.googleapis.com/maps/api/distancematrix/json"

# Step 1: Read the CSV file containing latitudes and longitudes
locations = []
try:
    with open('updated_locations.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            location = {
                'name': row[0],
                'lat': row[2],
                'lng': row[3]
            }
            locations.append(location)
except FileNotFoundError:
    print("Error: The file 'updated_locations.csv' was not found.")
    exit()

# Step 2: Calculate the driving distance and time between consecutive locations
results = []  # List to store the driving distances and times
for i in range(len(locations) - 1):
    origin = locations[i]
    destination = locations[i + 1]
    
    # Prepare the parameters for the Distance Matrix API
    params = {
        'origins': f"{origin['lat']},{origin['lng']}",
        'destinations': f"{destination['lat']},{destination['lng']}",
        'key': API_KEY,
        'mode': 'driving'
    }
    
    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        print(f"Error: Failed to fetch data for {origin['name']} to {destination['name']} (HTTP {response.status_code})")
        results.append([origin['name'], destination['name'], "Error: API Request Failed", "N/A"])
        continue

    data = response.json()
    if data['status'] == 'OK' and data['rows'][0]['elements'][0]['status'] == 'OK':
        distance = data['rows'][0]['elements'][0]['distance']['text']
        duration = data['rows'][0]['elements'][0]['duration']['text']
        print(f"From {origin['name']} to {destination['name']}: {distance}, {duration}")
        results.append([origin['name'], destination['name'], distance, duration])
    else:
        print(f"From {origin['name']} to {destination['name']}: Distance not found (Status: {data['status']})")
        results.append([origin['name'], destination['name'], "Distance not found", "N/A"])

with open('driving_distances.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Origin', 'Destination', 'Distance', 'Duration'])  # Write header
    for row in results:
        if any(row):  # Only write non-empty rows
            writer.writerow(row)
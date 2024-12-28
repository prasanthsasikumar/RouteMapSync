import csv
import requests

# Replace with your actual Google Maps API key
API_KEY = 'AIzaSyBUVW8eJLVVGkqU3wEiV17tOduPAaFnOxo'
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
DISTANCE_URL = "https://maps.googleapis.com/maps/api/distancematrix/json"

# Step 1: Read the raw_locations.csv file and get coordinates
locations = []
try:
    with open('Locations_List.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            location_name = row[0]
            
            # Geocode each location
            params = {'address': location_name, 'key': API_KEY}
            response = requests.get(GEOCODE_URL, params=params)
            
            if response.status_code != 200:
                print(f"Error: Failed to fetch data for {location_name} (HTTP {response.status_code})")
                continue
                
            data = response.json()
            if data['status'] == 'OK':
                full_address = data['results'][0]['formatted_address']
                lat = data['results'][0]['geometry']['location']['lat']
                lng = data['results'][0]['geometry']['location']['lng']
                locations.append({
                    'name': location_name,
                    'address': full_address,
                    'lat': lat,
                    'lng': lng
                })
                print(full_address, lat, lng)
            else:
                print(f"{location_name}: Address not found (Status: {data['status']})")
                
except FileNotFoundError:
    print("Error: The file 'raw_locations.csv' was not found.")
    exit()

# Step 2: Calculate driving distances and times between consecutive locations
results = []
for i in range(len(locations) - 1):
    origin = locations[i]
    destination = locations[i + 1]
    
    # Prepare parameters for the Distance Matrix API
    params = {
        'origins': f"{origin['lat']},{origin['lng']}",
        'destinations': f"{destination['lat']},{destination['lng']}",
        'key': API_KEY,
        'mode': 'driving'
    }
    
    response = requests.get(DISTANCE_URL, params=params)

    if response.status_code != 200:
        print(f"Error: Failed to fetch data for {origin['name']} to {destination['name']} (HTTP {response.status_code})")
        results.append([
            origin['name'], destination['name'],
            origin['lat'], origin['lng'],
            destination['lat'], destination['lng'],
            "Error: API Request Failed", "N/A",
            origin['address'], destination['address']

        ])
        continue

    data = response.json()
    if data['status'] == 'OK' and data['rows'][0]['elements'][0]['status'] == 'OK':
        distance = data['rows'][0]['elements'][0]['distance']['text']
        duration = data['rows'][0]['elements'][0]['duration']['text']
        print(f"From {origin['name']} to {destination['name']}: {distance}, {duration}")
        results.append([
            origin['name'], destination['name'],
            distance, duration,
            origin['lat'], origin['lng'],
            destination['lat'], destination['lng'],
            origin['address'], destination['address']
        ])
    else:
        print(f"From {origin['name']} to {destination['name']}: Distance not found (Status: {data['status']})")
        results.append([
            origin['name'], destination['name'],
            "Distance not found", "N/A",
            origin['lat'], origin['lng'],
            destination['lat'], destination['lng'],
            origin['address'], destination['address']
        ])

# Write results to CSV with coordinates included
with open('Route_Details.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow([
        'Origin', 'Destination',
        'Distance', 'Duration',
        'Origin_Latitude', 'Origin_Longitude',
        'Destination_Latitude', 'Destination_Longitude',
        'Origin_Address', 'Destination_Address'
    ])
    for row in results:
        if any(row):
            writer.writerow(row)
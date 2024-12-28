import csv
import requests

# Replace 'YOUR_API_KEY' with your actual Google Maps API key
API_KEY = 'AIzaSyBUVW8eJLVVGkqU3wEiV17tOduPAaFnOxo'
BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

# Step 1: Read the raw_locations.csv file
locations = []
try:
    with open('raw_locations.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            locations.append(row[0])
except FileNotFoundError:
    print("Error: The file 'raw_locations.csv' was not found.")
    exit()

# Step 2: Look up the locations using the Google Maps API
results = []  # List to store location, full address, latitude, and longitude
for location in locations:
    params = {'address': location, 'key': API_KEY}
    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        print(f"Error: Failed to fetch data for {location} (HTTP {response.status_code})")
        results.append([location, "Error: API Request Failed", "N/A", "N/A"])
        continue

    data = response.json()
    if data['status'] == 'OK':
        full_address = data['results'][0]['formatted_address']
        latitude = data['results'][0]['geometry']['location']['lat']  # Correctly extracting latitude
        longitude = data['results'][0]['geometry']['location']['lng']  # Correctly extracting longitude
        results.append([location, full_address, latitude, longitude])
    else:
        print(f"{location}: Address not found (Status: {data['status']})")
        results.append([location, f"Address not found (Status: {data['status']})", "N/A", "N/A"])

print("Length of results:", len(results))

with open('updated_locations.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Original Location', 'Full Address', 'Latitude', 'Longitude'])  # Write header
    for row in results:
        if any(row):  # Only write non-empty rows
            writer.writerow(row)

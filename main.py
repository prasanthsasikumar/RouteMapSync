import csv
import requests
from datetime import datetime, timedelta

# Replace with your actual Google Maps API key
API_KEY = 'AIzaSyBUVW8eJLVVGkqU3wEiV17tOduPAaFnOxo'
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
DISTANCE_URL = "https://maps.googleapis.com/maps/api/distancematrix/json"

def parse_time(time_str):
    hours = 0
    minutes = 0
    if 'days' in time_str or 'day' in time_str:
        parts = time_str.split('days') if 'days' in time_str else time_str.split('day')
        days = float(parts[0].strip())
        hours = days * 24
        time_str = parts[1]
    if 'hours' in time_str or 'hour' in time_str:
        parts = time_str.split('hours') if 'hours' in time_str else time_str.split('hour')
        hours += float(parts[0].strip())
        if 'mins' in parts[1] or 'min' in parts[1]:
            minutes = float(parts[1].split('mins')[0].strip() if 'mins' in parts[1] else parts[1].split('min')[0].strip())
    else:
        minutes = float(time_str.split('mins')[0].strip() if 'mins' in time_str else time_str.split('min')[0].strip())
    return hours, minutes

def parse_distance(distance_str):
    if ',' in distance_str:
        distance_str = distance_str.replace(',', '')
    return float(distance_str.split('km')[0].strip())

def read_locations(filename):
    locations = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                locations.append(row[0])
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        exit()
    return locations

def geocode_location(location_name):
    params = {'address': location_name, 'key': API_KEY}
    response = requests.get(GEOCODE_URL, params=params)
    if response.status_code != 200:
        print(f"Error: Failed to fetch data for {location_name} (HTTP {response.status_code})")
        return None
    data = response.json()
    print(data['results'][0]['formatted_address'])


    if data['status'] == 'OK':
        result = data['results'][0]
        return {
            'name': location_name,
            'address': result['formatted_address'],
            'lat': result['geometry']['location']['lat'],
            'lng': result['geometry']['location']['lng']
        }
    else:
        print(f"{location_name}: Address not found (Status: {data['status']})")
        return None

def calculate_distances(locations):
    results = []
    for i in range(len(locations) - 1):
        origin = locations[i]
        destination = locations[i + 1]
        params = {
            'origins': f"{origin['lat']},{origin['lng']}",
            'destinations': f"{destination['lat']},{destination['lng']}",
            'key': API_KEY,
            'mode': 'driving'
        }
        response = requests.get(DISTANCE_URL, params=params)
        if response.status_code != 200:
            print(f"Error: Failed to fetch data for {origin['name']} to {destination['name']} (HTTP {response.status_code})")
            results.append([origin['name'], destination['name'], origin['lat'], origin['lng'], destination['lat'], destination['lng'], "Error: API Request Failed", "N/A", origin['address'], destination['address']])
            continue
        data = response.json()
        if data['status'] == 'OK':
            element = data['rows'][0]['elements'][0]
            distance = element['distance']['text']
            duration = element['duration']['text']
            results.append([origin['name'], destination['name'], origin['lat'], origin['lng'], destination['lat'], destination['lng'], distance, duration, origin['address'], destination['address']])
            print(f"{origin['name']} to {destination['name']}: {distance}, {duration}")
        else:
            print(f"Error: {data['status']} for {origin['name']} to {destination['name']}")
    return results

def calculate_totals(results):
    total_distance = 0
    total_hours = 0
    total_minutes = 0
    for row in results:
        if len(row) >= 3 and row[0] not in ['Total']:
            distance = parse_distance(row[6])
            hours, minutes = parse_time(row[7])
            total_distance += distance
            total_hours += hours
            total_minutes += minutes
    additional_hours = total_minutes // 60
    total_hours += additional_hours
    total_minutes = total_minutes % 60
    total_time = f"{int(total_hours)} hours {int(total_minutes)} mins"
    total_distance_str = f"{total_distance:.1f} km"
    return total_distance_str, total_time

def main():
    locations_list = read_locations('Locations_List.csv')
    locations = [geocode_location(location) for location in locations_list if geocode_location(location)]
    results = calculate_distances(locations)
    total_distance, total_time = calculate_totals(results)
    print(f"Total Distance: {total_distance}")
    print(f"Total Time: {total_time}")

if __name__ == "__main__":
    main()
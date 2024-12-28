from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import csv
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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

def geocode_location(location_name):
    params = {'address': location_name, 'key': API_KEY}
    response = requests.get(GEOCODE_URL, params=params)
    if response.status_code != 200:
        return None
    data = response.json()
    if data['status'] == 'OK':
        result = data['results'][0]
        return {
            'name': location_name,
            'address': result['formatted_address'],
            'lat': result['geometry']['location']['lat'],
            'lng': result['geometry']['location']['lng']
        }
    else:
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
            results.append({
                'origin_name': origin['name'],
                'destination_name': destination['name'],
                'origin_lat': origin['lat'],
                'origin_lng': origin['lng'],
                'destination_lat': destination['lat'],
                'destination_lng': destination['lng'],
                'distance': "Error: API Request Failed",
                'duration': "N/A",
                'origin_address': origin['address'],
                'destination_address': destination['address']
            })
            continue
        data = response.json()
        if data['status'] == 'OK':
            element = data['rows'][0]['elements'][0]
            distance = element['distance']['text']
            duration = element['duration']['text']
            results.append({
                'origin_name': origin['name'],
                'destination_name': destination['name'],
                'origin_lat': origin['lat'],
                'origin_lng': origin['lng'],
                'destination_lat': destination['lat'],
                'destination_lng': destination['lng'],
                'distance': distance,
                'duration': duration,
                'origin_address': origin['address'],
                'destination_address': destination['address']
            })
        else:
            results.append({
                'origin_name': origin['name'],
                'destination_name': destination['name'],
                'origin_lat': origin['lat'],
                'origin_lng': origin['lng'],
                'destination_lat': destination['lat'],
                'destination_lng': destination['lng'],
                'distance': "Error: API Request Failed",
                'duration': "N/A",
                'origin_address': origin['address'],
                'destination_address': destination['address']
            })
    return results

def calculate_totals(results):
    total_distance = 0
    total_hours = 0
    total_minutes = 0
    for row in results:
        if len(row) >= 3 and row['distance'] not in ['Error: API Request Failed']:
            distance = parse_distance(row['distance'])
            hours, minutes = parse_time(row['duration'])
            total_distance += distance
            total_hours += hours
            total_minutes += minutes
    additional_hours = total_minutes // 60
    total_hours += additional_hours
    total_minutes = total_minutes % 60
    total_time = f"{int(total_hours)} hours {int(total_minutes)} mins"
    total_distance_str = f"{total_distance:.1f} km"
    return total_distance_str, total_time

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    locations_list = request.form['locations'].split('\n')
    locations = [geocode_location(location.strip()) for location in locations_list if geocode_location(location.strip())]
    results = calculate_distances(locations)
    total_distance, total_time = calculate_totals(results)
    return render_template('results.html', results=results, total_distance=total_distance, total_time=total_time)

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    data = request.get_json()
    locations_list = data['locations']
    locations = [geocode_location(location.strip()) for location in locations_list if geocode_location(location.strip())]
    print(locations)
    results = calculate_distances(locations)
    total_distance, total_time = calculate_totals(results)
    return jsonify({
        'results': results,
        'total_distance': total_distance,
        'total_time': total_time
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
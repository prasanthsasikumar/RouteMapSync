import csv
from datetime import datetime, timedelta

def parse_time(time_str):
    # Initialize hours and minutes
    hours = 0
    minutes = 0

    # Check if 'days' or 'day' is in the string
    if 'days' in time_str or 'day' in time_str:
        parts = time_str.split('days') if 'days' in time_str else time_str.split('day')
        days = float(parts[0].strip())
        hours = days * 24
        time_str = parts[1]

    # Check if 'hours' or 'hour' is in the string
    if 'hours' in time_str or 'hour' in time_str:
        parts = time_str.split('hours') if 'hours' in time_str else time_str.split('hour')
        hours += float(parts[0].strip())
        # Check if there are minutes after hours
        if 'mins' in parts[1] or 'min' in parts[1]:
            minutes = float(parts[1].split('mins')[0].strip() if 'mins' in parts[1] 
                          else parts[1].split('min')[0].strip())
    else:
        # If only minutes are present
        minutes = float(time_str.split('mins')[0].strip() if 'mins' in time_str 
                       else time_str.split('min')[0].strip())

    return hours, minutes

def parse_distance(distance_str):
    if ',' in distance_str:
        distance_str = distance_str.replace(',', '')
    return float(distance_str.split('km')[0].strip())

def calculate_totals(filename):
    total_distance = 0
    total_hours = 0
    total_minutes = 0

    # Read the existing data
    rows = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            rows.append(row)
            if len(row) >= 3 and row[0] not in ['Total']:  # Exclude summary rows
                distance = parse_distance(row[2])
                hours, minutes = parse_time(row[3])

                total_distance += distance
                total_hours += hours
                total_minutes += minutes

    # Convert excess minutes to hours
    additional_hours = total_minutes // 60
    total_hours += additional_hours
    total_minutes = total_minutes % 60

    # Format the totals
    total_time = f"{int(total_hours)} hours {int(total_minutes)} mins"
    total_distance_str = f"{total_distance:.1f} km"

    # Check if totals already exist and update them
    updated = False
    for row in rows:
        if row[0] == 'Total':
            row[1] = total_distance_str
            updated = True

    if not updated:
        # Add totals if they don't already exist
        rows.append(['Total', ' ', total_distance_str, total_time, ' ',' ',' ',' ',' ',' '])

    # Write the updated data back to the file
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)

# Usage
calculate_totals('Route_Details.csv')

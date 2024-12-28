import googlemaps
from gmplot import gmplot
import pandas as pd

# Your Google Maps API key
API_KEY = "AIzaSyBUVW8eJLVVGkqU3wEiV17tOduPAaFnOxo"

# Initialize the Google Maps client
gmaps = googlemaps.Client(key=API_KEY)

# Load the CSV file
csv_file = "Route_Details.csv"
df = pd.read_csv(csv_file)

# Extract relevant columns: Origin_Latitude, Origin_Longitude, Destination_Latitude, Destination_Longitude
coordinates = []
for index, row in df.iterrows():
    try:
        # Ensure the latitudes and longitudes are valid floats
        origin_lat = float(row['Origin_Latitude'])
        origin_lng = float(row['Origin_Longitude'])
        destination_lat = float(row['Destination_Latitude'])
        destination_lng = float(row['Destination_Longitude'])

        # Append origin and destination coordinates as tuples
        coordinates.append((origin_lat, origin_lng))
        coordinates.append((destination_lat, destination_lng))
    except ValueError:
        print(f"Skipping row {index} due to invalid latitude or longitude.")

# Check if there are valid coordinates to plot
if coordinates:
    # Create a Google Map plotter object using the first point (Origin of the first entry)
    gmap = gmplot.GoogleMapPlotter(coordinates[0][0], coordinates[0][1], zoom=6)

    # Extract latitudes and longitudes for plotting
    latitudes, longitudes = zip(*coordinates)

    # Plot the points
    gmap.plot(latitudes, longitudes, color='red', edge_width=2)

    # Optional: Create a marker for each location
    for lat, lng in coordinates:
        gmap.marker(lat, lng)

    # Save the map as an HTML file
    gmap.draw("route_map.html")

    print("Route map saved as 'route_map.html'")

    # Open the map in a web browser
    import webbrowser
    webbrowser.open("route_map.html")
else:
    print("No valid coordinates to plot.")

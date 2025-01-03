# Route Map Sync 
Backend for [Route Map View](https://github.com/prasanthsasikumar/RouteMapView)

## Overview
Route Map Sync is a Python-based application designed to help users calculate and visualize travel routes, distances, and times between multiple locations. The application integrates with Google Maps to provide accurate distance calculations and route visualizations. It also generates detailed HTML reports and allows users to upload the results to Google Sheets for further analysis and sharing.

## Features
- Calculate total distance and travel time between multiple locations
- Generate detailed HTML reports with route visualizations
- Upload results to Google Sheets
- User-friendly web interface for easy interaction

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/route-map-sync.git
    cd route-map-sync
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up your Google Maps API key:
    - Obtain an API key from the [Google Cloud Console](https://console.cloud.google.com/).
    - Create a file named `config.py` and add your API key:
        ```python
        GOOGLE_MAPS_API_KEY = 'your_api_key_here'
        ```
5. [Optional] Docker image of this repo can be found here - 
    - https://hub.docker.com/repository/docker/impsk/routemap/builds


## Usage
1. Run the main to do everything including updating the excel sheet:
    ```sh
    python main.py
    ```
    app.py to serve the webpage and also host the POST endpoint
   ```sh
    python app.py
    ```

3. Open your web browser and navigate to `http://localhost:5000`.

4. Enter the locations in the provided textarea and click "Calculate" to generate the route details.

5. View the generated HTML report and optionally upload the results to Google Sheets.

![Screenshot](screenshot.png)

## SSL
1. We are using NGINX to simplify SSL,
2. Certbot to get a SSL certificate for the domain [https://theconsciousriderbackend.prasanthsasikumar.com/](https://theconsciousriderbackend.prasanthsasikumar.com/),
3. We serve the page with Gunicorn -
   ```sh
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
4. Also our nginx config(to route traffic) and systemmd.service(for automatic restart on boot) are in the root folder.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](http://_vscodecontentref_/14) file for details.

## Acknowledgements
- [Google Maps API](https://developers.google.com/maps/documentation)
- [Flask](https://flask.palletsprojects.com/)
- [Pandas](https://pandas.pydata.org/)

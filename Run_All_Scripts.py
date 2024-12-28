import subprocess
import sys
import os

# Path to the Python executable within your virtual environment
venv_python = 'C:\\Users\\vrmss\\OneDrive\\Documents\\GitHub\\Wanderlog-Scrapper\\venv\\Scripts\\python.exe'

def run_script(script_name):
    try:
        subprocess.run([venv_python, script_name], check=True)
        print(f"Successfully ran {script_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")

def main():
    # Run scripts in sequence using the Python executable from the virtual environment
    print("Running Step 1: Get address, lat, long, and calculate distance/time")
    run_script('Get_Address_LatLong_Distance.py')

    print("Running Step 2: Calculate total distance and time")
    run_script('Calculate_Total_Distance_Time.py')

    print("Running Step 3: Upload to Sheets and apply formatting")
    run_script('Upload_To_Sheets_And_Format.py')

    print("Running Step 4: Generate HTML for the route")
    run_script('Generate_Route_HTML.py')

if __name__ == '__main__':
    main()

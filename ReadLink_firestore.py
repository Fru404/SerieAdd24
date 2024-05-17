import firebase_admin
from firebase_admin import credentials, db
import json

def ReadLink():
    # Path to your service account key file
    service_account_key_file = "serviceAccountKey.json"

    # Initialize the app with a service account, granting admin privileges
    cred = credentials.Certificate(service_account_key_file)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://webseries-phroustechnology-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

    # Reference to the specific location in the database
    ref = db.reference('/')

    # Retrieve the data at the specified reference
    data = ref.get()

    # Function to recursively search for the "name" and "link" keys
    def find_name_and_link(data):
        results = []  # List to accumulate name and link values
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    if "name" in value and "link" in value:
                        results.append({"name": value["name"], "link": value["link"]})
                    else:
                        results.extend(find_name_and_link(value))
        elif isinstance(data, list):
            for item in data:
                results.extend(find_name_and_link(item))
        return results

    # Retrieve and parse data from Firebase
    parsed_data = find_name_and_link(data)

    # Convert the parsed data to JSON format
    json_data = json.dumps(parsed_data)

    return json_data


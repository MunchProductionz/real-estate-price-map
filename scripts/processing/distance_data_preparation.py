import os
import json
import math
from tqdm import tqdm
from datetime import datetime
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()

def get_postcodes_from_geojson() -> dict:
    """Get  postcodes from GeoJSON file.

    Args:
        None

    Returns:
        list: List of postcodes.
    """
    path = os.path.join(os.getcwd(), "../../frontend/public/data/postcodes.json")
    with open(path, "r") as f:
        postcodes_data = json.load(f)
    postcodes = [feature["properties"]["postnummer"] for feature in postcodes_data["features"]]
    return postcodes

def get_distance_postcodes_destinations() -> dict:
    """Get distance data for postcodes and destinations.

    Args:
        None

    Returns:
        dict: Distance data for postcodes and destinations.
    """
    path = os.path.join(os.getcwd(), "../../frontend/public/data/distance_postcodes_destinations.json")
    with open(path, "r") as f:
        distance_postcodes_destinations = json.load(f)
    return distance_postcodes_destinations

def get_nearest_location_for_postcode(postcode: str, distance_postcodes_destinations: dict) -> dict:
    """Get the nearest location for each category for a given postcode.

    Args:
        postcode (str): Postcode.
        distance_postcodes_destinations (dict): Distance data for postcodes and destinations.

    Returns:
        dict: Nearest location dictionary with nearest location for each category.
    """
    nearest_location = {}
    nearest_location_per_category = {}
    travel_types = ["walking", "bicycling", "transit", "driving"]
    categories = ["vinmonopolet", "shopping_mall"]
    
    # Find the nearest location for each category for the given postcode
    for category in categories:
        
        # Initialize the category in the nearest location dictionary
        nearest_location[category] = {}
        
        # Initialize the minimum duration in seconds
        min_duration_seconds = math.inf
    
        # Find the nearest location for each category and store the data in a new format
        for destination_address in distance_postcodes_destinations[postcode].keys():
            
            # Check if destination is not available (empty)
            if distance_postcodes_destinations[postcode][destination_address].__len__() == 0:
                continue
            
            # Check if category is not available (no data on category)
            if category not in list(distance_postcodes_destinations[postcode][destination_address].keys()):
                continue
            
            # Check if destination is not available (no available travel routes)
            if distance_postcodes_destinations[postcode][destination_address][category]["travel_data"]["walking"]["status"] == "ZERO_RESULTS":
                continue
            
            # Add variable to make code more readable
            destination = distance_postcodes_destinations[postcode][destination_address][category]
            
            # Find the nearest location in terms of walking duration in seconds
            if destination["travel_data"]["walking"]["duration"]["seconds"] < min_duration_seconds:
                nearest_location_per_category[category] = destination
                min_duration_seconds = destination["travel_data"]["walking"]["duration"]["seconds"]
    
    # Find the nearest location for each category
    for category in nearest_location_per_category.keys():
    
        # Define foromat of the "travel_data" key in the nearest_location dictionary
        travel_data = {}
        for travel_type in travel_types:
            try:
                travel_data[travel_type] = {
                    "distance": {
                        "text": nearest_location_per_category[category]["travel_data"][travel_type]["distance"]["text"],
                        "meters": nearest_location_per_category[category]["travel_data"][travel_type]["distance"]["meters"],
                        "kilometers": nearest_location_per_category[category]["travel_data"][travel_type]["distance"]["kilometers"]
                    },
                    "duration": {
                        "text": nearest_location_per_category[category]["travel_data"][travel_type]["duration"]["text"],
                        "seconds": nearest_location_per_category[category]["travel_data"][travel_type]["duration"]["seconds"],
                        "minutes": nearest_location_per_category[category]["travel_data"][travel_type]["duration"]["minutes"],
                        "hours": nearest_location_per_category[category]["travel_data"][travel_type]["duration"]["hours"],
                        "hours_and_minutes": nearest_location_per_category[category]["travel_data"][travel_type]["duration"]["hours_and_minutes"]
                    }
                }
            except:     # If no travel data for 'driving' is available (status='ZERO_RESULTS')
                travel_data[travel_type] = {
                    "distance": {
                        "text": "N/A",
                        "meters": "N/A",
                        "kilometers": "N/A"
                    },
                    "duration": {
                        "text": "N/A",
                        "seconds": "N/A",
                        "minutes": "N/A",
                        "hours": "N/A",
                        "hours_and_minutes": "N/A"   
                    }
                }
                
        
        # Store the nearest location data for the current category
        nearest_location[category]["destination_name"] = nearest_location_per_category[category]["destination_name"]
        nearest_location[category]["destination_address"] = nearest_location_per_category[category]["destination_address"]
        nearest_location[category]["travel_data"] = travel_data
                 
    return nearest_location
    
def store_distance_data(distance_data: dict) -> None:
    """Store distance data in a JSON file.

    Args:
        distance_data (dict): Distance data.
        
    Returns:
        None
    """
    output_path = os.path.join(os.getcwd(), "../../frontend/public/data/distance_data.json")
    with open(output_path, "w") as f:
        json.dump(distance_data, f, indent=2)
    
    
def format_and_store_data():
    """Format and store distance data in a JSON file.
    
    Args:
        None
        
    Returns:
        None
    """
    
    distance_data = {}
    
    print("Getting data...")
    postcodes = get_postcodes_from_geojson()
    distance_postcodes_destinations = get_distance_postcodes_destinations()
    print("Data retrieved successfully.\n")
    
    print("Formatting data...")
    for postcode in tqdm(postcodes):
        nearest_location = get_nearest_location_for_postcode(postcode, distance_postcodes_destinations)
        distance_data[postcode] = {
            "nearest_location": nearest_location
        }
    print("Data formatted successfully.\n")
    
    print("Storing data...")
    store_distance_data(distance_data)
    print("Data stored successfully.")
    
    
def main():
    print("Running distance data preparation script...")
    format_and_store_data()
    print("Script executed successfully.")
    
main()
import os
import json
import math
import requests
import googlemaps
from datetime import datetime
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()

# Load environment variables
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Initialize Google Maps API client
def get_google_maps_client():
    """Initialize Google Maps API client using Google Maps API key from environment variables.

    Returns:
        googlemaps.Client: Google Maps API client.
    """
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    return gmaps

# Get postcodes from GeoJSON
def get_postcodes_from_geojson(geojson_path):
    """Get postcodes from GeoJSON file.

    Args:
        geojson_path (str): Path to GeoJSON file.

    Returns:
        list: List of postcodes.
    """
    with open(geojson_path, "r") as file:
        postcodes_data = json.load(file)
    postcodes = [feature["properties"]["postnummer"] for feature in postcodes_data["features"]]
    return postcodes

# Get distance matrix
def get_distance_matrix(gmaps, origins, destinations, mode="driving"):
    """Get distance matrix from Google Maps API.

    Args:
        gmaps (googlemaps.Client): Google Maps API client.
        origins (list): List of origins.
        destinations (list): List of destinations.
        mode (str, optional): Travel mode. Defaults to "driving".

    Returns:
        dict: Distance matrix results.
    """
    results = gmaps.distance_matrix(
        origins=origins,
        destinations=destinations,
        mode=mode,
        units="metric",
        departure_time=datetime.now()
        )
    return results

def add_granularity_to_results(results_walking, results_bicycling, results_transit, results_driving):
    """Add granularity to distance matrix results by adding meters, kilometers, seconds, minutes, hours, and hours and minutes to each result.

    Args:
        results_walking (dict): Distance matrix results for walking mode.
        results_bicycling (dict): Distance matrix results for bicycling mode.
        results_transit (dict): Distance matrix results for transit mode.
        results_driving (dict): Distance matrix results for driving mode.

    Returns:
        tuple: Distance matrix results for walking, bicycling, transit, and driving modes with added granularity.
    """
    
    # Add granularity to results
    for origin_index, origin in enumerate(results_walking["origin_addresses"]):
        for destination_index, destination in enumerate(results_walking["destination_addresses"]):
            
            
            # Walking
            if results_walking["rows"][origin_index]["elements"][destination_index]["status"] == "OK":      # Check if status is "OK", otherwise skip.  If status is "ZERO_RESULTS", results are not available, and response looks like: {'status': 'ZERO_RESULTS'}
                meters_walking = results_walking["rows"][origin_index]["elements"][destination_index]["distance"]["value"]
                kilometers_walking = math.ceil(results_walking["rows"][origin_index]["elements"][destination_index]["distance"]["value"] / 1000)
                seconds_walking = results_walking["rows"][origin_index]["elements"][destination_index]["duration"]["value"]
                minutes_walking = math.ceil(results_walking["rows"][origin_index]["elements"][destination_index]["duration"]["value"] / 60)
                hours_walking = round(results_walking["rows"][origin_index]["elements"][destination_index]["duration"]["value"] / 3600, 2)
                hrs_walking = math.floor(results_walking["rows"][origin_index]["elements"][destination_index]["duration"]["value"] / 3600)
                min_walking = math.ceil((results_walking["rows"][origin_index]["elements"][destination_index]["duration"]["value"] - (hrs_walking * 3600)) / 60)
                hours_and_minutes_walking = [hrs_walking, min_walking]
                
                results_walking["rows"][origin_index]["elements"][destination_index]["distance"]["meters"] = meters_walking
                results_walking["rows"][origin_index]["elements"][destination_index]["distance"]["kilometers"] = kilometers_walking
                results_walking["rows"][origin_index]["elements"][destination_index]["duration"]["seconds"] = seconds_walking
                results_walking["rows"][origin_index]["elements"][destination_index]["duration"]["minutes"] = minutes_walking
                results_walking["rows"][origin_index]["elements"][destination_index]["duration"]["hours"] = hours_walking
                results_walking["rows"][origin_index]["elements"][destination_index]["duration"]["hours_and_minutes"] = hours_and_minutes_walking
            
            
            # Bicycling
            if results_bicycling["rows"][origin_index]["elements"][destination_index]["status"] == "OK":    # Check if status is "OK", otherwise skip.  If status is "ZERO_RESULTS", results are not available, and response looks like: {'status': 'ZERO_RESULTS'}
                meters_bicycling = results_bicycling["rows"][origin_index]["elements"][destination_index]["distance"]["value"]
                kilometers_bicycling = math.ceil(results_bicycling["rows"][origin_index]["elements"][destination_index]["distance"]["value"] / 1000)
                seconds_bicycling = results_bicycling["rows"][origin_index]["elements"][destination_index]["duration"]["value"]
                minutes_bicycling = math.ceil(results_bicycling["rows"][origin_index]["elements"][destination_index]["duration"]["value"] / 60)
                hours_bicycling = round(results_bicycling["rows"][origin_index]["elements"][destination_index]["duration"]["value"] / 3600, 2)
                hrs_bicycling = math.floor(results_bicycling["rows"][origin_index]["elements"][destination_index]["duration"]["value"] / 3600)
                min_bicycling = math.ceil((results_bicycling["rows"][origin_index]["elements"][destination_index]["duration"]["value"] - (hrs_bicycling * 3600)) / 60)
                hours_and_minutes_bicycling = [hrs_bicycling, min_bicycling]
                
                results_bicycling["rows"][origin_index]["elements"][destination_index]["distance"]["meters"] = meters_bicycling
                results_bicycling["rows"][origin_index]["elements"][destination_index]["distance"]["kilometers"] = kilometers_bicycling
                results_bicycling["rows"][origin_index]["elements"][destination_index]["duration"]["seconds"] = seconds_bicycling
                results_bicycling["rows"][origin_index]["elements"][destination_index]["duration"]["minutes"] = minutes_bicycling
                results_bicycling["rows"][origin_index]["elements"][destination_index]["duration"]["hours"] = hours_bicycling
                results_bicycling["rows"][origin_index]["elements"][destination_index]["duration"]["hours_and_minutes"] = hours_and_minutes_bicycling
            
            
            # Transit   -   TODO NOTE: Remember to check if the status is "OK" in frontend before displaying results
            if results_transit["rows"][origin_index]["elements"][destination_index]["status"] == "OK":      # Check if status is "OK", otherwise skip.  If status is "ZERO_RESULTS", results are not available, and response looks like: {'status': 'ZERO_RESULTS'}
                meters_transit = results_transit["rows"][origin_index]["elements"][destination_index]["distance"]["value"]
                kilometers_transit = math.ceil(results_transit["rows"][origin_index]["elements"][destination_index]["distance"]["value"] / 1000)
                seconds_transit = results_transit["rows"][origin_index]["elements"][destination_index]["duration"]["value"]
                minutes_transit = math.ceil(results_transit["rows"][origin_index]["elements"][destination_index]["duration"]["value"] / 60)
                hours_transit = round(results_transit["rows"][origin_index]["elements"][destination_index]["duration"]["value"] / 3600, 2)
                hrs_transit = math.floor(results_transit["rows"][origin_index]["elements"][destination_index]["duration"]["value"] / 3600)
                min_transit = math.ceil((results_transit["rows"][origin_index]["elements"][destination_index]["duration"]["value"] - (hrs_transit * 3600)) / 60)
                hours_and_minutes_transit = [hrs_transit, min_transit]
                
                results_transit["rows"][origin_index]["elements"][destination_index]["distance"]["meters"] = meters_transit
                results_transit["rows"][origin_index]["elements"][destination_index]["distance"]["kilometers"] = kilometers_transit
                results_transit["rows"][origin_index]["elements"][destination_index]["duration"]["seconds"] = seconds_transit
                results_transit["rows"][origin_index]["elements"][destination_index]["duration"]["minutes"] = minutes_transit
                results_transit["rows"][origin_index]["elements"][destination_index]["duration"]["hours"] = hours_transit
                results_transit["rows"][origin_index]["elements"][destination_index]["duration"]["hours_and_minutes"] = hours_and_minutes_transit

            
            # Driving
            if results_driving["rows"][origin_index]["elements"][destination_index]["status"] == "OK":      # Check if status is "OK", otherwise skip.  If status is "ZERO_RESULTS", results are not available, and response looks like: {'status': 'ZERO_RESULTS'}
                meters_driving = results_driving["rows"][origin_index]["elements"][destination_index]["distance"]["value"]
                kilometers_driving = math.ceil(results_driving["rows"][origin_index]["elements"][destination_index]["distance"]["value"] / 1000)
                seconds_driving = results_driving["rows"][origin_index]["elements"][destination_index]["duration"]["value"]
                minutes_driving = math.ceil(results_driving["rows"][origin_index]["elements"][destination_index]["duration"]["value"] / 60)
                hours_driving = round(results_driving["rows"][origin_index]["elements"][destination_index]["duration"]["value"] / 3600, 2)
                hrs_driving = math.floor(results_driving["rows"][origin_index]["elements"][destination_index]["duration"]["value"] / 3600)
                min_driving = math.ceil((results_driving["rows"][origin_index]["elements"][destination_index]["duration"]["value"] - (hrs_driving * 3600)) / 60)
                hours_and_minutes_driving = [hrs_driving, min_driving]
                
                results_driving["rows"][origin_index]["elements"][destination_index]["distance"]["meters"] = meters_driving
                results_driving["rows"][origin_index]["elements"][destination_index]["distance"]["kilometers"] = kilometers_driving
                results_driving["rows"][origin_index]["elements"][destination_index]["duration"]["seconds"] = seconds_driving
                results_driving["rows"][origin_index]["elements"][destination_index]["duration"]["minutes"] = minutes_driving
                results_driving["rows"][origin_index]["elements"][destination_index]["duration"]["hours"] = hours_driving
                results_driving["rows"][origin_index]["elements"][destination_index]["duration"]["hours_and_minutes"] = hours_and_minutes_driving
 
    return results_walking, results_bicycling, results_transit, results_driving

def get_results(results_walking, results_bicycling, results_transit, results_driving):
    """Get results from distance matrix results with postcodes as keys, and destinations as subkeys.

    Args:
        results_walking (dict): Distance matrix results for walking mode.
        results_bicycling (dict): Distance matrix results for bicycling mode.
        results_transit (dict): Distance matrix results for transit mode.
        results_driving (dict): Distance matrix results for driving mode.

    Returns:
        tuple: Distance matrix results with postcodes as keys, and destinations as subkeys, and distance matrix results with destinations as keys, and postcodes as subkeys.
    """
    
    # Initialize results dictionaries
    results_postcodes_destinations = {}
    results_destinations_postcodes = {}
    
    # Store results in dictionaries using postcodes as keys
    for origin_index, origin in enumerate(results_walking["origin_addresses"]):
        
        # Get postcode
        postcode = origin.split(" ")[0]
        
        # Initialize destination dictionary
        if postcode not in results_postcodes_destinations.keys():
            results_postcodes_destinations[postcode] = {}
        
        # Store results in destination dictionary
        for destination_index, destination in enumerate(results_walking["destination_addresses"]):
            results_postcodes_destinations[postcode][destination] = {
                "walking": results_walking["rows"][origin_index]["elements"][destination_index],
                "bicycling": results_bicycling["rows"][origin_index]["elements"][destination_index],
                "transit": results_transit["rows"][origin_index]["elements"][destination_index],
                "driving": results_driving["rows"][origin_index]["elements"][destination_index]
            }
    
    # Store results in dictionaries using destinations as keys
    for destination_index, destination in enumerate(results_walking["destination_addresses"]):
        
        # Initialize origin dictionary
        if destination not in results_destinations_postcodes.keys():
            results_destinations_postcodes[destination] = {}
        
        # Store results in origin dictionary
        for origin_index, origin in enumerate(results_walking["origin_addresses"]):
            postcode = origin.split(" ")[0]
            results_destinations_postcodes[destination][postcode] = {
                "walking": results_walking["rows"][origin_index]["elements"][destination_index],
                "bicycling": results_bicycling["rows"][origin_index]["elements"][destination_index],
                "transit": results_transit["rows"][origin_index]["elements"][destination_index],
                "driving": results_driving["rows"][origin_index]["elements"][destination_index]
            }
            
    return results_postcodes_destinations, results_destinations_postcodes
    
# Store distance matrix results - Postcodes to Destinations
def store_results_postcodes_destinations(results_postcodes_destinations, output_path):
    """Store distance matrix results in JSON format with postcodes as keys, and destinations as subkeys.

    Args:
        results_postcodes_destinations (dict): Distance matrix results with postcodes as keys, and destinations as subkeys.
        output_path (str): Output path for storing results.
        
    Returns:
        None
    """
    
    # Load existing results
    with open(output_path, "r") as file:
        existing_results = json.load(file)
        
    # Update existing results with new results
    for postcode_extra in results_postcodes_destinations.keys():
        postcode = postcode_extra.split(" ")[0]
        if postcode not in existing_results.keys():
            existing_results[postcode] = results_postcodes_destinations[postcode]
        
        for destination in results_postcodes_destinations[postcode].keys():
            if destination not in existing_results[postcode].keys():
                existing_results[postcode][destination] = results_postcodes_destinations[postcode][destination]
    
    # Update existing results with new results
    with open(output_path, "w") as file:
        file.write(json.dumps(existing_results, indent=4))
        file.write("\n")
    print(f"Stored results with {len(results_postcodes_destinations.keys())} keys to {output_path}")
    
# Store distance matrix results - Destinations to Postcodes
def store_results_destinations_postcodes(results_destinations_postcodes, output_path):
    """Store distance matrix results in JSON format with destinations as keys, and postcodes as subkeys.

    Args:
        results_destinations_postcodes (dict): Distance matrix results with destinations as keys, and postcodes as subkeys.
        output_path (str): Output path for storing results.
        
    Returns:
        None
    """
    
    # Load existing results
    with open(output_path, "r") as file:
        existing_results = json.load(file)
        
    # Update existing results with new results
    for destination in results_destinations_postcodes.keys():
        if destination not in existing_results.keys():
            existing_results[destination] = results_destinations_postcodes[destination]
        
        for postcode_extra in results_destinations_postcodes[destination].keys():
            postcode = postcode_extra.split(" ")[0]
            if postcode not in existing_results[destination].keys():
                existing_results[destination][postcode] = results_destinations_postcodes[destination][postcode]
    
    # Update existing results with new results
    with open(output_path, "w") as file:
        file.write(json.dumps(existing_results, indent=4))
        file.write("\n")
    print(f"Stored results with {len(results_destinations_postcodes.keys())} keys to {output_path}")
    
def get_and_append_results(gmaps, origins, destinations):
    """Update JSON files with distances between postcodes and destinations for one batch.

    Args:
        gmaps (googlemaps.Client): Google Maps API client.
        origins (list): List of origins.
        destinations (list): List of destinations.
    
    Returns:
        None
    """
    
    # Get distance matrix results
    results_walking = get_distance_matrix(
        gmaps=gmaps,
        origins=origins[:3],                    # TODO: Remove [:3] when ready
        destinations=destinations,
        mode="walking"
        )
    results_bicycling = get_distance_matrix(
        gmaps=gmaps,
        origins=origins[:3],
        destinations=destinations,
        mode="bicycling"
        )
    results_transit = get_distance_matrix(
        gmaps=gmaps,
        origins=origins[:3],
        destinations=destinations,
        mode="transit"
        )
    results_driving = get_distance_matrix(
        gmaps=gmaps,
        origins=origins[:3],
        destinations=destinations,
        mode="driving"
        )
    
    # Add granularity to results
    results_walking, results_bicycling, results_transit, results_driving = add_granularity_to_results(
        results_walking=results_walking,
        results_bicycling=results_bicycling,
        results_transit=results_transit,
        results_driving=results_driving
    )
    
    # Get results
    results_postcodes_destinations, results_destinations_postcodes = get_results(
        results_walking=results_walking,
        results_bicycling=results_bicycling,
        results_transit=results_transit,
        results_driving=results_driving
        )
    
    # Store distance matrix results
    output_path_postcodes_destinations = os.path.join(os.getcwd(), "../frontend/public/data/distance_postcodes_destinations.json")
    output_path_destinations_postcodes = os.path.join(os.getcwd(), "../frontend/public/data/distance_destinations_postcodes.json")
    store_results_postcodes_destinations(results_postcodes_destinations, output_path_postcodes_destinations)
    store_results_destinations_postcodes(results_destinations_postcodes, output_path_destinations_postcodes)
    
    return None
    
    
# Main function
def update_distances(destinations):
    """Update JSON files with distances between postcodes and destinations.

    Args:
        destinations (list): List of destinations. (ex. ["{postcode}, Norway", {coordinates}] etc.)

    Returns:
        None
    """
    
    # Initialize Google Maps API client
    gmaps = get_google_maps_client()
    
    # Get postcodes from GeoJSON
    geojson_path = os.path.join(os.getcwd(), "../frontend/public/data/postcodes.json")
    postcodes = get_postcodes_from_geojson(geojson_path)
    
    # Get origins and destinations
    origins = [f"{postcode}, Norway" for postcode in postcodes]
    
    # Get and append results to avoid exceeding Google Maps API rate limits
    for i in range(0, len(origins[:3]), 25):                # TODO: Remove [:3] when ready
        get_and_append_results(gmaps, origins[i:i+25], destinations)
    
    print(f"Done updating distances between {len(origins)} origins and {len(destinations)} destinations!")
    
    return None

def main():
    destinations = ["7010, Norway", "7030, Norway"]
    update_distances(destinations=destinations)
    

if __name__ == "__main__":
    main()



# ### Test single origin and destination - Postcode ###
# results = gmaps.distance_matrix(
#     origins="0274, Norway",
#     destinations="7030, Norway",
#     mode="driving",
#     units="metric",
#     departure_time=datetime.now()
#     )

## Output - Driving ##
# {'destination_addresses': ['7030 Trondheim, Norway'],
#  'origin_addresses': ['0274 Oslo, Norway'],
#  'rows': [{'elements': [{'distance': {'text': '496 km', 'value': 496498},
#                          'duration': {'text': '6 hours 16 mins',
#                                       'value': 22531},
#                          'duration_in_traffic': {'text': '6 hours 10 mins',
#                                                  'value': 22220},
#                          'status': 'OK'}]}],
#  'status': 'OK'}

## Output - Walking ##
# {'destination_addresses': ['7030 Trondheim, Norway'],
#  'origin_addresses': ['0274 Oslo, Norway'],
#  'rows': [{'elements': [{'distance': {'text': '493 km', 'value': 492813},
#                          'duration': {'text': '4 days 16 hours',
#                                       'value': 402941},
#                          'status': 'OK'}]}],
#  'status': 'OK'}


# ### Test single origin and destination ###
# results = gmaps.distance_matrix(
#     origins="Oslo",
#     destinations="Trondheim",
#     mode="driving",
#     units="metric",
#     departure_time=datetime.now()
#     )

## Output ##
# {'destination_addresses': ['Trondheim, Norway'],
#  'origin_addresses': ['Oslo, Norway'],
#  'rows': [{'elements': [{'distance': {'text': '492 km', 'value': 492194},                     # Oslo to Trondheim
#                          'duration': {'text': '6 hours 14 mins',
#                                       'value': 22461},
#                          'duration_in_traffic': {'text': '6 hours 12 mins',
#                                                  'value': 22296},
#                          'status': 'OK'}]}],
#  'status': 'OK'}


# ### Test multiple origins and single destination ###
# results = gmaps.distance_matrix(
#     origins=["Oslo", "Bergen"],
#     destinations="Trondheim",
#     mode="driving",
#     units="metric",
#     departure_time=datetime.now()
#     )

## Output ##
# {'destination_addresses': ['Trondheim, Norway'],
#  'origin_addresses': ['Oslo, Norway', 'Bergen, Norway'],
#  'rows': [{'elements': [{'distance': {'text': '492 km', 'value': 492194},                     # Oslo to Trondheim
#                          'duration': {'text': '6 hours 14 mins',
#                                       'value': 22461},
#                          'duration_in_traffic': {'text': '6 hours 11 mins',
#                                                  'value': 22285},
#                          'status': 'OK'}]},
#           {'elements': [{'distance': {'text': '628 km', 'value': 627552},                     # Bergen to Trondheim
#                          'duration': {'text': '9 hours 37 mins',
#                                       'value': 34635},
#                          'duration_in_traffic': {'text': '9 hours 38 mins',
#                                                  'value': 34659},
#                          'status': 'OK'}]}],
#  'status': 'OK'}





### Test single origin and multiple destinations ###
# results = gmaps.distance_matrix(
#     origins="Oslo",
#     destinations=["Trondheim", "Bergen"],
#     mode="driving",
#     units="metric",
#     departure_time=datetime.now()
#     )

## Output ##
# {'destination_addresses': ['Trondheim, Norway', 'Bergen, Norway'],
#  'origin_addresses': ['Oslo, Norway'],
#  'rows': [{'elements': [{'distance': {'text': '492 km', 'value': 492194},                     # Oslo to Trondheim
#                          'duration': {'text': '6 hours 14 mins',
#                                       'value': 22461},
#                          'duration_in_traffic': {'text': '6 hours 11 mins',
#                                                  'value': 22250},
#                          'status': 'OK'},
#                         {'distance': {'text': '464 km', 'value': 463555},                     # Oslo to Bergen
#                          'duration': {'text': '7 hours 3 mins', 'value': 25402},
#                          'duration_in_traffic': {'text': '7 hours 7 mins',
#                                                  'value': 25626},
#                          'status': 'OK'}]}],
#  'status': 'OK'}


# ### Multiple origins and multiple destinations ###
# results = gmaps.distance_matrix(
#     origins=["Oslo", "Stavanger"],
#     destinations=["Trondheim", "Bergen"],
#     mode="driving",
#     units="metric",
#     departure_time=datetime.now()
#     )

## Output ##
# {'destination_addresses': ['Trondheim, Norway', 'Bergen, Norway'],
#  'origin_addresses': ['Oslo, Norway', 'Stavanger, Norway'],
#  'rows': [{'elements': [{'distance': {'text': '492 km', 'value': 492194},                   # Oslo to Trondheim
#                          'duration': {'text': '6 hours 14 mins',
#                                       'value': 22461},
#                          'duration_in_traffic': {'text': '6 hours 11 mins',
#                                                  'value': 22241},
#                          'status': 'OK'},
#                         {'distance': {'text': '464 km', 'value': 463555},                   # Oslo to Bergen
#                          'duration': {'text': '7 hours 3 mins', 'value': 25402},
#                          'duration_in_traffic': {'text': '7 hours 9 mins',
#                                                  'value': 25736},
#                          'status': 'OK'}]},
#           {'elements': [{'distance': {'text': '934 km', 'value': 934098},                   # Stavanger to Trondheim
#                          'duration': {'text': '12 hours 53 mins',
#                                       'value': 46350},
#                          'duration_in_traffic': {'text': '12 hours 53 mins',
#                                                  'value': 46389},
#                          'status': 'OK'},
#                         {'distance': {'text': '208 km', 'value': 207539},                   # Stavanger to Bergen
#                          'duration': {'text': '4 hours 38 mins',
#                                       'value': 16670},
#                          'duration_in_traffic': {'text': '4 hours 35 mins',
#                                                  'value': 16525},
#                          'status': 'OK'}]}],
#  'status': 'OK'}


# for i, origin in enumerate(results["origin_addresses"]):
#     for j, destination in enumerate(results["destination_addresses"]):
#         print(f"Distance from {origin} to {destination}:")
#         print(f"Distance: {results['rows'][i]['elements'][j]['distance']['text']}")
#         print(f"Duration: {results['rows'][i]['elements'][j]['duration']['text']}")
#         print(f"Duration in traffic: {results['rows'][i]['elements'][j]['duration_in_traffic']['text']}")
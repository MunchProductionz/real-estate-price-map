import os
import json
import math
import requests
import googlemaps
from tqdm import tqdm
from datetime import datetime
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()

# Load environment variables
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_destinations(is_vinmonopolet=False, is_shopping_mall=False):
    """Get destinations for which distances need to be calculated. Destinations can be Vinmonopolet stores, shopping malls, etc.

    Args:
        is_vinmonopolet (bool, optional): Flags whether to get vinmonopolet destinations. Defaults to False.
        is_shopping_mall (bool, optional): Flags whether to get shopping mall destinations. Defaults to False.

    Returns:
        tuple: List of destinations and dictionary with destination categories as keys, and destination addresses as values. The dictionary should look like: {"vinmonopolet": {"{address}, {postcode}, Norway": "{destination_name}", ...}, ...}
    """
    
    
    destinations = []
    destinations_metadata = {}
    
    if is_vinmonopolet:
        destinations_vinmonopolet = {
            # "Lilleakerveien 16, 0283 Oslo, Norway": "Vinmonopolet CC Vest",
            # "Elisenbergveien 37, 0265 Oslo, Norway": "Vinmonopolet Frogner",
            # "Slemdalsveien 70a, 0370 Oslo, Norway": "Vinmonopolet Slemdal",
            # "Sørkedalsveien 10, 0369 Oslo, Norway": "Vinmonopolet Majorstuen",
            # "Briskebyveien 48, 0259 Oslo, Norway": "Vinmonopolet Briskeby",
            # "Bryggegata 9, 0250 Oslo, Norway": "Vinmonopolet Aker Brygge",
            # "Karl Johans gt. 37, 0162 Oslo, Norway": "Vinmonopolet Karl Johan",
            # "Kongens gate 23, 0153 Oslo, Norway": "Vinmonopolet Stortinget",
            # "Waldemar Thranes gate 72, 0175 Oslo, Norway": "Vinmonopolet St. Hanshaugen",
            # "Nordre gate 16, 0551 Oslo, Norway": "Vinmonopolet Nordre Gate",
            # "1-3, Stenersgata, 0050 Oslo, Norway": "Vinmonopolet Oslo City",
            # "Jernbanetorget 1, 0154 Oslo, Norway": "Vinmonopolet Jernbanetorget",
            # "Dronning Eufemias gate 11, 0191 Oslo, Norway": "Vinmonopolet Operahuset",
            # "Rostockgata 130, Oslo kommune, Norway": "Vinmonopolet Bjørvika",
            # "Tøyengata 2, 0190 Oslo, Norway": "Vinmonopolet Tøyen",
            # "Nydalsveien 33, 0484 Oslo, Norway": "Vinmonopolet Nydalen",
            # "Vitaminveien 7, 0485 Oslo, Norway": "Vinmonopolet Storo",
            # "Sandakerveien 59, 0477 Oslo, Norway": "Vinmonopolet Torshov",
            # "Hasleveien 10, 0571 Oslo, Norway": "Vinmonopolet Grünerløkka",
            # "Grenseveien 50, 0579 Oslo, Norway": "Vinmonopolet Hovin",
            # "Cecilie Thoresens vei 17, 1153 Oslo, Norway": "Vinmonopolet Lambertseter",
            # "Utmarkveien 1, 0689 Oslo, Norway": "Vinmonopolet Bøler",
        }
        for destination in destinations_vinmonopolet.keys():
            if not destination in destinations:
                destinations.append(destination)
        destinations_metadata["vinmonopolet"] = destinations_vinmonopolet
    
    if is_shopping_mall:
        destinations_shopping_mall = {
            # "1-3, Stenersgata, 0050 Oslo, Norway": "Oslo City",                         # NOTE: This is same address as Vinmonopolet Oslo City
            # "St. Hanshaugen senter, Waldemar Thranes gate 25, 0171 Oslo, Norway": "St. Hanshaugen Senter",
            # "Tøyengata 2, 0190 Oslo, Norway": "Grønland Basar",                         # NOTE: This is same address as Vinmonopolet Tøyen
            # "Vitaminveien 7, 9 0485, 0485 Oslo, Norway": "Storo Storsenter",
            # "Sandakerveien 59, 0477 Oslo, Norway": "Sandaker Senter",                   # NOTE: This is same address as Vinmonopolet Torshov
        }
        for destination in destinations_shopping_mall.keys():
            if not destination in destinations:
                destinations.append(destination)
        destinations_metadata["shopping_mall"] = destinations_shopping_mall
        
    
    return destinations, destinations_metadata
    
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

# Manually update destination names in destinations and destinations_metadata dictionaries
def update_destination_names(destinations, destinations_metadata):
    """Manually update destination names in destinations and destinations_metadata dictionaries.

    Args:
        destinations (list): List of destinations.
        destinations_metadata (dict): Dictionary with destination categories as keys, and destination addresses as values. The dictionary should look like: {"vinmonopolet": {"{address}, {postcode}, Norway": "{destination_name}", ...}, ...}

    Returns:
        tuple: Updated destinations (list) and destinations_metadata (dict).
    """
    
    destinations_copy = destinations.copy()
    destinations_metadata_copy = destinations_metadata.copy()
    
    for destinations_index, destination in enumerate(destinations_copy):
        
        # St. Hanshaugen Senter
        if destination == "St. Hanshaugen senter, Waldemar Thranes gate 25, 0171 Oslo, Norway":
            destinations_copy[destinations_index] = "Waldemar Thranes gate 25, 0171 Oslo, Norway"
            
        # Vinmonopolet Oslo City
        if destination == "1-3, Stenersgata, 0050 Oslo, Norway":
            destinations_copy[destinations_index] = "Stenersgata 1, 0050 Oslo, Norway"
            
        
    for category in destinations_metadata_copy.keys():
        temp_destinations_metadata_keys = list(destinations_metadata_copy[category].keys())
        for destination in temp_destinations_metadata_keys:
            
            # St. Hanshaugen Senter
            if destination == "St. Hanshaugen senter, Waldemar Thranes gate 25, 0171 Oslo, Norway":
                if "St. Hanshaugen senter, Waldemar Thranes gate 25, 0171 Oslo, Norway" in temp_destinations_metadata_keys:
                    destinations_metadata_copy[category]["Waldemar Thranes gate 25, 0171 Oslo, Norway"] = destinations_metadata_copy[category].pop(destination)
                    
            # Vinmonopolet Oslo City
            if destination == "1-3, Stenersgata, 0050 Oslo, Norway":
                if "1-3, Stenersgata, 0050 Oslo, Norway" in temp_destinations_metadata_keys:
                    destinations_metadata_copy[category]["Stenersgata 1, 0050 Oslo, Norway"] = destinations_metadata_copy[category].pop(destination)
    
    return destinations_copy, destinations_metadata_copy
    
# Add granularity to distance matrix results
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
    
    results_list = [results_walking, results_bicycling, results_transit, results_driving]
    
    # Add granularity to results
    for results in results_list:
        for origin_index, origin in enumerate(results["origin_addresses"]):
            for destination_index, destination in enumerate(results["destination_addresses"]):
                if results["rows"][origin_index]["elements"][destination_index]["status"] == "OK":      # Check if status is "OK", otherwise skip.  If status is "ZERO_RESULTS", results are not available, and response looks like: {'status': 'ZERO_RESULTS'}
                    meters = results["rows"][origin_index]["elements"][destination_index]["distance"]["value"]
                    kilometers = math.ceil(results["rows"][origin_index]["elements"][destination_index]["distance"]["value"] / 1000)
                    seconds = results["rows"][origin_index]["elements"][destination_index]["duration"]["value"]
                    minutes = math.ceil(results["rows"][origin_index]["elements"][destination_index]["duration"]["value"] / 60)
                    hours = round(results["rows"][origin_index]["elements"][destination_index]["duration"]["value"] / 3600, 2)
                    hrs = math.floor(results["rows"][origin_index]["elements"][destination_index]["duration"]["value"] / 3600)
                    min = math.ceil((results["rows"][origin_index]["elements"][destination_index]["duration"]["value"] - (hrs * 3600)) / 60)
                    hours_and_minutes = [hrs, min]
                    
                    results["rows"][origin_index]["elements"][destination_index]["distance"]["meters"] = meters
                    results["rows"][origin_index]["elements"][destination_index]["distance"]["kilometers"] = kilometers
                    results["rows"][origin_index]["elements"][destination_index]["duration"]["seconds"] = seconds
                    results["rows"][origin_index]["elements"][destination_index]["duration"]["minutes"] = minutes
                    results["rows"][origin_index]["elements"][destination_index]["duration"]["hours"] = hours
                    results["rows"][origin_index]["elements"][destination_index]["duration"]["hours_and_minutes"] = hours_and_minutes
                
    return results_walking, results_bicycling, results_transit, results_driving     # Return updated results, remember that dictionaries are mutable in Python, so they are updated when looping through "results_list"

# Get results
def get_results(results_walking, results_bicycling, results_transit, results_driving, destinations_metadata):
    """Get results from distance matrix results with postcodes as keys, and destinations as subkeys.

    Args:
        results_walking (dict): Distance matrix results for walking mode.
        results_bicycling (dict): Distance matrix results for bicycling mode.
        results_transit (dict): Distance matrix results for transit mode.
        results_driving (dict): Distance matrix results for driving mode.
        destinations_metadata (dict): Dictionary with destination categories as keys, and destination addresses as values. The dictionary should look like: {"vinmonopolet": {"{address}, {postcode}, Norway": "{destination_name}", ...}, ...}

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
            
            # Get destination address
            destination_address = destination
            
            # Get categories for the destination
            categories = []
            if destination in list(destinations_metadata["vinmonopolet"].keys()): categories.append("vinmonopolet")
            if destination in list(destinations_metadata["shopping_mall"].keys()): categories.append("shopping_mall")
            
            # Store results in destination dictionary
            results_postcodes_destinations[postcode][destination] = {}
            for category in categories:
                
                # Get destination name
                destination_name = destination.split(",")[0]
                if category == "vinmonopolet": destination_name = destinations_metadata["vinmonopolet"][destination]
                if category == "shopping_mall": destination_name = destinations_metadata["shopping_mall"][destination]
                
                results_postcodes_destinations[postcode][destination][category] = {
                    "travel_data": {
                        "walking": results_walking["rows"][origin_index]["elements"][destination_index],
                        "bicycling": results_bicycling["rows"][origin_index]["elements"][destination_index],
                        "transit": results_transit["rows"][origin_index]["elements"][destination_index],
                        "driving": results_driving["rows"][origin_index]["elements"][destination_index]
                    },
                    "destination_address": destination_address,
                    "category": category,
                    "destination_name": destination_name   
                }
    
    # Store results in dictionaries using destinations as keys
    for destination_index, destination in enumerate(results_walking["destination_addresses"]):
        
        # Initialize origin dictionary
        if destination not in results_destinations_postcodes.keys():
            results_destinations_postcodes[destination] = {}
        
        # Get destination address
        destination_address = destination
        
        # Get destination category
        categories = []
        if destination in list(destinations_metadata["vinmonopolet"].keys()): categories.append("vinmonopolet")
        if destination in list(destinations_metadata["shopping_mall"].keys()): categories.append("shopping_mall")
        
        # Store results in origin dictionary
        for origin_index, origin in enumerate(results_walking["origin_addresses"]):
            postcode = origin.split(" ")[0]
                
            # Store results in destination dictionary
            results_destinations_postcodes[destination][postcode] = {}
            for category in categories:
                
                # Get destination name
                destination_name = destination.split(",")[0]
                if category == "vinmonopolet": destination_name = destinations_metadata["vinmonopolet"][destination]
                if category == "shopping_mall": destination_name = destinations_metadata["shopping_mall"][destination]
                
                results_destinations_postcodes[destination][postcode][category] = {
                    "travel_data": {
                        "walking": results_walking["rows"][origin_index]["elements"][destination_index],
                        "bicycling": results_bicycling["rows"][origin_index]["elements"][destination_index],
                        "transit": results_transit["rows"][origin_index]["elements"][destination_index],
                        "driving": results_driving["rows"][origin_index]["elements"][destination_index]
                    },
                    "destination_address": destination_address,
                    "category": category,
                    "destination_name": destination_name
                }
            
    return results_postcodes_destinations, results_destinations_postcodes
    
# Store distance matrix results
def store_results(results, output_path):
    """Store distance matrix results in JSON format.

    Args:
        results (dict): Distance matrix results.
        output_path (str): Output path for storing results.
        
    Returns:
        None
    """
    with open(output_path, "w") as file:
        file.write(json.dumps(results, indent=4))
        file.write("\n")
    print(f"Stored results with {len(results.keys())} keys to {output_path}")

# Append distance matrix results - Postcodes to Destinations
def append_results_postcodes_destinations(results_postcodes_destinations, output_path):
    """Store distance matrix results in JSON format with postcodes as keys, and destinations as subkeys.

    Args:
        results_postcodes_destinations (dict): Distance matrix results with postcodes as keys, and destinations as subkeys.
        output_path (str): Output path for storing results.
        
    Returns:
        None
    """
    
    # Create new file if it does not exist
    if not os.path.exists(output_path):
        with open(output_path, "w") as file:
            file.write("{}")
            file.write("\n")
        print(f"Created new file at {output_path}")
    
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
    # print(f"Stored results with {len(results_postcodes_destinations.keys())} keys to {output_path}")
    
# Append distance matrix results - Destinations to Postcodes
def append_results_destinations_postcodes(results_destinations_postcodes, output_path):
    """Store distance matrix results in JSON format with destinations as keys, and postcodes as subkeys.

    Args:
        results_destinations_postcodes (dict): Distance matrix results with destinations as keys, and postcodes as subkeys.
        output_path (str): Output path for storing results.
        
    Returns:
        None
    """
    
    # Create new file if it does not exist
    if not os.path.exists(output_path):
        with open(output_path, "w") as file:
            file.write("{}")
            file.write("\n")
        print(f"Created new file at {output_path}")
    
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
    # print(f"Stored results with {len(results_destinations_postcodes.keys())} keys to {output_path}")

# Get and append results - Perform for each batch
def get_and_append_results(gmaps, origins, destinations, destinations_metadata, is_overwrite=False):
    """Update JSON files with distances between postcodes and destinations for one batch.

    Args:
        gmaps (googlemaps.Client): Google Maps API client.
        origins (list): List of origins.
        destinations (list): List of destinations.
        is_overwrite (bool, optional): Overwrite existing files. Defaults to False.
    
    Returns:
        None
    """
    
    # Get distance matrix results
    results_walking = get_distance_matrix(
        gmaps=gmaps,
        origins=origins,
        destinations=destinations,
        mode="walking"
        )
    results_bicycling = get_distance_matrix(
        gmaps=gmaps,
        origins=origins,
        destinations=destinations,
        mode="bicycling"
        )
    results_transit = get_distance_matrix(
        gmaps=gmaps,
        origins=origins,
        destinations=destinations,
        mode="transit"
        )
    results_driving = get_distance_matrix(
        gmaps=gmaps,
        origins=origins,
        destinations=destinations,
        mode="driving"
        )
    
    # Manually update destination names
    destinations, destinations_metadata = update_destination_names(destinations, destinations_metadata)
    
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
        results_driving=results_driving,
        destinations_metadata=destinations_metadata
    )
    
    # pprint(results_postcodes_destinations)
    
    # Store distance matrix results
    output_path_postcodes_destinations = os.path.join(os.getcwd(), "../../frontend/public/data/distance_postcodes_destinations.json")
    output_path_destinations_postcodes = os.path.join(os.getcwd(), "../../frontend/public/data/distance_destinations_postcodes.json")
    # output_path_postcodes_destinations = os.path.join(os.getcwd(), "../../frontend/public/data/distance_postcodes_destinations_extra_points.json")
    # output_path_destinations_postcodes = os.path.join(os.getcwd(), "../../frontend/public/data/distance_destinations_postcodes_extra_points.json")
    
    if is_overwrite:
        store_results(results_postcodes_destinations, output_path_postcodes_destinations)
        store_results(results_destinations_postcodes, output_path_destinations_postcodes)
    else:
        append_results_postcodes_destinations(results_postcodes_destinations, output_path_postcodes_destinations)
        append_results_destinations_postcodes(results_destinations_postcodes, output_path_destinations_postcodes)
    
    return None
    
# Main function
def update_distances(destinations, destinations_metadata, is_overwrite=False):
    """Update JSON files with distances between postcodes and destinations.

    Args:
        destinations (list): List of destinations. (ex. ["{postcode}, Norway", {coordinates}] etc.)
        destinations_metadata (dict): Dictionary with destination categories as keys, and destination addresses as values. The dictionary should look like: {"vinmonopolet": {"{address}, {postcode}, Norway": "{destination_name}", ...}, ...}
        is_overwrite (bool, optional): Overwrite existing files. Defaults to False.

    Returns:
        None
    """
    
    # Initialize Google Maps API client
    gmaps = get_google_maps_client()
    
    # Get postcodes from GeoJSON
    geojson_path = os.path.join(os.getcwd(), "../../frontend/public/data/postcodes.json")
    postcodes = get_postcodes_from_geojson(geojson_path)
    
    # Get origins and destinations
    origins = [f"{postcode}, Norway" for postcode in postcodes]
    
    # Get and append results to avoid exceeding Google Maps API rate limits             # TODO: Max 100 elements per request, max 25 origins OR 25 destinations per request
    for i in tqdm(range(0, len(origins))):
        get_and_append_results(gmaps, origins[i], destinations, destinations_metadata, is_overwrite)
    
    # print(f"Done updating distances between {len(origins)} origins and {len(destinations)} destinations!")
    
    return None

def main():
    
    # Get destinations
    destinations, destinations_metadata = get_destinations(
        is_vinmonopolet=True,
        is_shopping_mall=True,
        )
    
    # Set overwrite flag
    is_overwrite = False

    # Update distances
    update_distances(destinations=destinations, destinations_metadata=destinations_metadata, is_overwrite=is_overwrite)
    

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
import os
import json
from datetime import datetime
from pprint import pprint


# Append distance matrix results - Postcodes to Destinations
def append_extra_points_to_postcodes_destinations(extra_points_path, postcodes_destinations_path):
    
    
    # Create new file if it does not exist
    if not os.path.exists(extra_points_path): return FileNotFoundError(f"File {extra_points_path} does not exist")
    if not os.path.exists(postcodes_destinations_path): return FileNotFoundError(f"File {postcodes_destinations_path} does not exist")
    
    # Load extra points results
    with open(extra_points_path, "r") as file:
        extra_points_results = json.load(file)
    
    # Load existing results
    with open(postcodes_destinations_path, "r") as file:
        existing_results = json.load(file)
    
    print(f"Extra points: {len(extra_points_results.keys())}")
    print(f"Existing postcodes: {len(existing_results.keys())}")
    
    counter = 0
    for postcode in extra_points_results.keys():
        for destination in extra_points_results[postcode].keys():
            
            # Remove existing results with the wrong keys
            if destination == "Stenersgata 1, 0050 Oslo, Norway":
                if "1-3, Stenersgata, Oslo, Norway" in existing_results[postcode].keys():
                    del existing_results[postcode]["1-3, Stenersgata, Oslo, Norway"]               # TODO: Ensure these are removed
            if destination == "Waldemar Thranes gate 25, 0171 Oslo, Norway":
                if "St. Hanshaugen senter, Waldemar Thranes gate 25, 0171 Oslo, Norway" in existing_results[postcode].keys():
                    del existing_results[postcode]["St. Hanshaugen senter, Waldemar Thranes gate 25, 0171 Oslo, Norway"]
            
            if destination not in existing_results[postcode].keys():
                existing_results[postcode][destination] = extra_points_results[postcode][destination]
                counter += 1
            elif existing_results[postcode][destination] == {}:
                existing_results[postcode][destination] = extra_points_results[postcode][destination]
                counter += 1
    
    print(f"Updated {counter} results")
    
    
    
    # Update existing results with new results
    with open(postcodes_destinations_path, "w") as file:
        file.write(json.dumps(existing_results, indent=4))
        file.write("\n")
    print(f"Stored results with {len(existing_results.keys())} keys to {postcodes_destinations_path}")
    
    
def main():
    extra_points_path = "../frontend/public/data/distance_postcodes_destinations_extra_points.json"
    postcodes_destinations_path = "../frontend/public/data/distance_postcodes_destinations.json"
    
    # append_extra_points_to_postcodes_destinations(extra_points_path, postcodes_destinations_path)
    
if __name__ == "__main__":
    main()
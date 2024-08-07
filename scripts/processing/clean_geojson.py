import json
import os
import pandas as pd
from pprint import pprint


def clean_geojson(poststed: str, city: str) -> None:
    
    # Paths
    # geojson_path = f"../data/geojson/postcodes_{poststed}.geojson"
    # geojson_cleaned_path = f"../data/postcodes_cleaned/postcodes_{poststed}.json"
    geojson_path = f"data/geojson/postcodes_{poststed}.geojson"                         # Use when running script from prepare_postcodes.py
    geojson_cleaned_path = f"data/postcodes_cleaned/postcodes_{poststed}.json"          # Use when running script from prepare_postcodes.py

    # Load geojson
    with open(geojson_path, "r") as f:
        geojson_data = json.load(f)
    
    # Get only necessary data
    geojson_cleaned_data = {}
    geojson_cleaned_data["type"] = geojson_data["postnummeromrader.postnummeromrade"]["type"]
    geojson_cleaned_data["features"] = []
    for i, feature in enumerate(geojson_data["postnummeromrader.postnummeromrade"]["features"]):
        if feature["properties"]["poststed"] == city:       # Filter only features with "poststed" = city
            
            # Clean "poststed" names that are parsed incorrectly
            poststed = feature["properties"]["poststed"]
            if poststed == "KRISTIANSAND S": poststed = "KRISTIANSAND"
            if poststed == "BODÃ˜": poststed = "BODØ"
            if poststed == "TROMSÃ˜": poststed = "TROMSØ"
            
            # Append cleaned data
            geojson_cleaned_data["features"].append({
                "type": feature["type"],
                "geometry": feature["geometry"],
                "properties": {
                    "objtype": feature["properties"]["objtype"],
                    "postnummer": feature["properties"]["postnummer"],
                    "poststed": poststed, 
                }
            })
    
    # Save cleaned geojson
    with open(geojson_cleaned_path, "w") as f:
        json.dump(geojson_cleaned_data, f, indent=2)
        
    print(f"Geojson with {len(geojson_cleaned_data['features'])} cleaned for {city} and saved to {geojson_cleaned_path}!")

def main():
    
    # Poststeder
    poststed_cities_dict = {
        "oslo": "OSLO",
        "drammen": "DRAMMEN",
        "kristiansand": "KRISTIANSAND S", # "S" is added when parsing "poststed" from geojson
        "stavanger": "STAVANGER",
        "bergen": "BERGEN",
        "trondelag": "TRONDHEIM",
        "bodo": "BODÃ˜",                  # Special character when parsing "poststed" from geojson
        "tromso": "TROMSÃ˜",                # Special character when parsing "poststed" from geojson
    }
    
    # Clean geojson files
    for poststed, city in poststed_cities_dict.items():
        clean_geojson(poststed, city)
    
if __name__ == "__main__":
    main()
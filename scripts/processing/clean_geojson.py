import json
import os
import pandas as pd
from pprint import pprint


def clean_geojson(city: str) -> None:
    
    # Paths
    geojson_path = f"../data/geojson/postnummers_{city}.geojson"
    geojson_cleaned_path = f"../data/postcodes_cleaned/postnummers_{city}.json"

    # Load geojson
    with open(geojson_path, "r") as f:
        geojson_data = json.load(f)
    
    



def main():
    
    # Poststeder
    cities = ["oslo", "trondelag", "bergen", "stavanger", "tromso"]
    
    # Clean geojson files
    for city in cities:
        clean_geojson(city)
    
if __name__ == "__main__":
    main()
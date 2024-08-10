import json
import os
import asyncio
from pprint import pprint
from processing.clean_geojson import clean_geojson
from scraper.market_data_scraper import get_market_data_from_post_codes_from_geojson, print_estimated_time_of_retrieval


async def prepare_postcodes():
    
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
    
    # Cities
    cities = list(poststed_cities_dict.keys())
    
    # Clean geojson files
    for poststed, city in poststed_cities_dict.items():
        clean_geojson(poststed, city)
    
    print("All geojson files cleaned!\n")
    
    
    # Get estimated time of retrieval
    print_estimated_time_of_retrieval(cities, max_requests_per_second=5)
    
    # Get market data from postcodes
    for city in cities:
        print(f"Started getting market data for: {city}")
        await get_market_data_from_post_codes_from_geojson(city)
        print(f"Finished getting market data for: {city}\n\n")
    
    print("All market data retrieved!")
    print("All postcodes prepared!")
    

def main():
    asyncio.run(prepare_postcodes())

if __name__ == "__main__":
    main()
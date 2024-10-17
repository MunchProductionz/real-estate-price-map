import json
import os
import math
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from time import time
import aiometer
import httpx
import functools


def print_estimated_time_of_retrieval(cities: list, max_requests_per_second: int) -> None:
    """Prints the estimated time of retrieval for each city and the total estimated time of retrieval for all cities.

    Args:
        cities (list): List of cities.
        max_requests_per_second (int): Maximum number of requests per second. 
        
    Returns:
        None
    """
    
    # Estimated time of retrieval for each city
    total_number_of_postcodes = 0
    city_times = {}
    for city in cities:
        # postcodes_cleaned_path = os.path.join(os.getcwd(), f"../data/postcodes_cleaned/postcodes_{city}.json")
        postcodes_cleaned_path = os.path.join(os.getcwd(), f"data/postcodes_cleaned/postcodes_{city}.json")          # Use when running script from prepare_postcodes.py
        with open(postcodes_cleaned_path, "r") as file:
            postcodes_data = json.load(file)
        
        number_of_postcodes = len(postcodes_data["features"])
        number_of_seconds = number_of_postcodes / max_requests_per_second
        number_of_minutes = math.floor(number_of_seconds / 60)
        number_of_seconds = number_of_seconds % 60
        if number_of_minutes < 1:
            time_string = f"{number_of_seconds} seconds"
        else:
            time_string = f"{number_of_minutes} minutes and {number_of_seconds} seconds"

        # Save city times
        city_times[city] = {
            "number_of_postcodes": number_of_postcodes,
            "number_of_minutes": number_of_minutes,
            "number_of_seconds": number_of_seconds,
            "time_string": time_string
        }
        
        # Add to total number of postcodes
        total_number_of_postcodes += number_of_postcodes
        
    # Get total time
    number_of_seconds = total_number_of_postcodes / max_requests_per_second
    number_of_minutes = math.floor(number_of_seconds / 60)
    number_of_seconds = number_of_seconds % 60
    if number_of_minutes < 1:
        total_estimated_time_of_retrieval = f"{number_of_seconds} seconds"
    else:
        total_estimated_time_of_retrieval = f"{number_of_minutes} minutes and {number_of_seconds} seconds"
        
    # Print city times and total time
    for city, city_time in city_times.items():
        print(f"- City: {city}, Number of postcodes: {city_time['number_of_postcodes']}, Estimated time of retrieval: {city_time['time_string']}")
    print(f"Total number of postcodes: {total_number_of_postcodes}, Total estimated time of retrieval: {total_estimated_time_of_retrieval}")
    

async def fetch(session: httpx.AsyncClient, url: str) -> httpx.Response:
    response = await session.send(url)
    if response.status_code != 200:
        raise Exception(f"HTTP status code: {response.status_code}")
    return response


async def get_market_data_from_response(response: str, post_code: str) -> tuple:
    """Get market data from response.

    Args:
        response (str): Response from request.
        post_code (str): Post code.

    Returns:
        tuple: Tuple with market data.
    """

    # Get soup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Get data
    data = soup.find_all("div", class_="css-j9s53t")
    
    # Get price percentage change last year
    price_percentage_change_last_year = data[0].text.replace("Endring siste år", "").split(" ")[0].replace(",", ".")
    if price_percentage_change_last_year[0] == "+": price_percentage_change_last_year = float(price_percentage_change_last_year[1:-1])        # Remove "+" and "%" and convert to float
    elif price_percentage_change_last_year[0] == "-": price_percentage_change_last_year = float(price_percentage_change_last_year[1:-1]) * -1
    elif price_percentage_change_last_year[0] == "0": price_percentage_change_last_year = 0.0
    
    # Get square meter price
    square_meter_price = int(data[1].text.replace("Kvadratmeterpris", "").replace("kr", "").replace(" ", ""))
    
    # Get price percentage change last quarter
    price_percentage_change_last_quarter = None
    price_percentage_change_last_month = None
    if "Endring siste kvartal" in data[2].text:                 # Check if price percentage change last quarter is available
        price_percentage_change_last_quarter = data[2].text.replace("Endring siste kvartal", "").split(" ")[0].replace(",", ".")
        if price_percentage_change_last_quarter[0] == "+": price_percentage_change_last_quarter = float(price_percentage_change_last_quarter[1:-1])         # Remove "+" and "%" and convert to float
        elif price_percentage_change_last_quarter[0] == "-": price_percentage_change_last_quarter = float(price_percentage_change_last_quarter[1:-1]) * -1
        elif price_percentage_change_last_quarter[0] == "0": price_percentage_change_last_quarter = 0.0
    if "Endring siste måned" in data[2].text:                   # Check if price percentage change last month is available
        price_percentage_change_last_month = data[2].text.replace("Endring siste måned", "").split(" ")[0].replace(",", ".")
        if price_percentage_change_last_month[0] == "+": price_percentage_change_last_month = float(price_percentage_change_last_month[1:-1])               # Remove "+" and "%" and convert to float
        elif price_percentage_change_last_month[0] == "-": price_percentage_change_last_month = float(price_percentage_change_last_month[1:-1]) * -1
        elif price_percentage_change_last_month[0] == "0": price_percentage_change_last_month = 0.0
    
    # Get average sales time
    average_sales_time = int(data[3].text.replace("Salgstid", "").split("\xa0")[0])
    
    # Get number of estates sold last quarter
    number_of_estates_sold_last_quarter = None
    number_of_estates_sold_last_month = None
    if "Solgte boliger siste  kvartal" in data[4].text:         # Check if number of estates sold last quarter is available
        number_of_estates_sold_last_quarter_string = data[4].text.replace("Solgte boliger siste  kvartal", "").split("\xa0")[0]
        if " " in number_of_estates_sold_last_quarter_string:   # Check for thousands separator (" ")
            number_of_estates_sold_last_quarter = int(number_of_estates_sold_last_quarter_string.split(" ")[0] + number_of_estates_sold_last_quarter_string.split(" ")[1])
        else:
            number_of_estates_sold_last_quarter = int(number_of_estates_sold_last_quarter_string)
    if "Solgte boliger siste  måned" in data[4].text:           # Check if number of estates sold last month is available
        number_of_estates_sold_last_month_string = data[4].text.replace("Solgte boliger siste  måned", "").split("\xa0")[0]
        if " " in number_of_estates_sold_last_month_string:     # Check for thousands separator (" ")
            number_of_estates_sold_last_month = int(number_of_estates_sold_last_month_string.split(" ")[0] + number_of_estates_sold_last_month_string.split(" ")[1])
        else:
            number_of_estates_sold_last_month = int(number_of_estates_sold_last_month_string)
    
    if price_percentage_change_last_quarter is not None:
        print(f"Post code: {post_code}, Square meter price: {square_meter_price} --> Last Year ==> Price percentage change: {price_percentage_change_last_year}, --> Last Quarter ==> Price percentage change: {price_percentage_change_last_quarter}, Average sales time: {average_sales_time} Number of estates sold: {number_of_estates_sold_last_quarter}")
    if price_percentage_change_last_month is not None:
        print(f"Post code: {post_code}, Square meter price: {square_meter_price} --> Last Year ==> Price percentage change: {price_percentage_change_last_year}, --> Last Month ==> Price percentage change: {price_percentage_change_last_month}, Average sales time: {average_sales_time} Number of estates sold: {number_of_estates_sold_last_month}")
    return price_percentage_change_last_year, square_meter_price, price_percentage_change_last_quarter, price_percentage_change_last_month, average_sales_time, number_of_estates_sold_last_quarter, number_of_estates_sold_last_month



async def add_market_data_to_dicts(i: int, postcodes_data: dict, postcodes_market_data: dict, results: list) -> tuple:
    """Add market data to dictionaries.

    Args:
        i (int): Index.
        postcodes_data (dict): Data with postcodes.
        postcodes_market_data (dict): Market data for postcodes.
        results (list(httpx.Response)): List of responses.

    Returns:
        tuple: 
    """
    
    # Unpack results
    price_percentage_change_last_year, square_meter_price, price_percentage_change_last_quarter, price_percentage_change_last_month, average_sales_time, number_of_estates_sold_last_quarter, number_of_estates_sold_last_month = results[i]
    
    # Add extra info to postcodes data
    postcodes_data["features"][i]["properties"]["pricePercentageChangeLastYear"] = price_percentage_change_last_year
    postcodes_data["features"][i]["properties"]["pricePercentageChangeLastQuarter"] = price_percentage_change_last_quarter
    postcodes_data["features"][i]["properties"]["pricePercentageChangeLastMonth"] = price_percentage_change_last_month
    postcodes_data["features"][i]["properties"]["averageSalesTimeInDays"] = average_sales_time
    postcodes_data["features"][i]["properties"]["numberOfEstatesSoldLastQuarter"] = number_of_estates_sold_last_quarter
    postcodes_data["features"][i]["properties"]["numberOfEstatesSoldLastMonth"] = number_of_estates_sold_last_month
    
    # Update average square meter price in geojson
    postcodes_data["features"][i]["properties"]["averageSquareMeterPrice"] = square_meter_price
    
    # Update average price for 20m2, 30m2, ..., 200m2
    start_square_meter_size = 20
    end_square_meter_size = 200
    step_size = 10
    for j in range(start_square_meter_size, end_square_meter_size + 1, step_size):
        postcodes_data["features"][i]["properties"][f"averagePrice{j}m2"] = square_meter_price * j
    
    # Add market data to postcodes_market_data
    postcodes_market_data[postcodes_data["features"][i]["properties"]["postnummer"]] = {
        "averageSquareMeterPrice": square_meter_price,
        "pricePercentageChangeLastYear": price_percentage_change_last_year,
        "pricePercentageChangeLastQuarter": price_percentage_change_last_quarter,
        "pricePercentageChangeLastMonth": price_percentage_change_last_month,
        "averageSalesTimeInDays": average_sales_time,
        "numberOfEstatesSoldLastQuarter": number_of_estates_sold_last_quarter,
        "numberOfEstatesSoldLastMonth": number_of_estates_sold_last_month,
    }
    
    return postcodes_data, postcodes_market_data


async def get_market_data_from_post_codes_from_geojson(city: str) -> None:
    """Get market data from post codes from geojson.

    Args:
        city (str): City.

    Returns:
        None 
    """
    
    # Async parameters
    max_requests_at_once = 10
    max_requests_per_second = 5
    
    # Get postcodes data
    # postcodes_cleaned_path = os.path.join(os.getcwd(), f"../data/postcodes_cleaned/postcodes_{city}.json")
    postcodes_cleaned_path = os.path.join(os.getcwd(), f"data/postcodes_cleaned/postcodes_{city}.json")      # Use when running script from prepare_postcodes.py
    with open(postcodes_cleaned_path, "r") as file:
        postcodes_data = json.load(file)
    
    # Get pages with square meter prices asynchronously
    session = httpx.AsyncClient()
    requests = [httpx.Request("GET", f"https://www.krogsveen.no/prisstatistikk?zipCode={feature['properties']['postnummer']}") for feature in postcodes_data["features"]]
    responses = [functools.partial(fetch, session, request) for request in requests]
    results = await aiometer.run_all(
                        responses,
                        max_at_once=max_requests_at_once, # Limit maximum number of concurrently running tasks.
                        max_per_second=max_requests_per_second,  # Limit request rate to not overload the server.
                    )

    # Get market data from responses
    for i, response in enumerate(results):
        results[i] = await get_market_data_from_response(response, post_code=postcodes_data["features"][i]["properties"]["postnummer"])
    
    # Update postcodes data and market data to file
    postcodes_market_data = {}
    for i, feature in enumerate(postcodes_data["features"]):                                                                    # TODO: Check if it is necessary to assign new dictionaries to "postcodes_data" and "postcodes_market_data"
        postcodes_data, postcodes_market_data = await add_market_data_to_dicts(i, postcodes_data, postcodes_market_data, results)     # TODO: Check if "feature" is enough

    # Save updated post codes data
    # postcodes_finalized_path = os.path.join(os.getcwd(), f"../data/postcodes_finalized/postcodes_{city}.json")
    postcodes_finalized_path = os.path.join(os.getcwd(), f"data/postcodes_finalized/postcodes_{city}.json")      # Use when running script from prepare_postcodes.py
    with open(postcodes_finalized_path, "w") as file:
        json.dump(postcodes_data, file, indent=2)
    
    # Save market data to file
    # postcodes_market_data_path = os.path.join(os.getcwd(), f"../data/postcodes_market_data_finalized/postcodes_market_data_{city}.json")
    postcodes_market_data_path = os.path.join(os.getcwd(), f"data/postcodes_market_data_finalized/postcodes_market_data_{city}.json")        # Use when running script from prepare_postcodes.py
    with open(postcodes_market_data_path, "w") as file:
        file.write(json.dumps(postcodes_market_data, indent=2))
        file.write("\n")
    
    print(f"Updated {len(postcodes_data['features'])} post codes data in for city {city} successfully to {postcodes_finalized_path}")
    print(f"Saved {len(postcodes_market_data.keys())} square meter prices for city {city} to {postcodes_market_data_path}")
    return None



async def main():
    
    cities = [
        "oslo",
        "drammen",
        "kristiansand",
        "stavanger",
        "bergen",
        "trondelag",
        "bodo",
        "tromso",
    ]
    
    print_estimated_time_of_retrieval(cities, max_requests_per_second=5)
    
    for city in cities:
        print(f"Started getting market data for: {city}")
        await get_market_data_from_post_codes_from_geojson(city)
        print(f"Finished getting market data for: {city}\n\n")


if __name__ == "__main__":
    asyncio.run(main())
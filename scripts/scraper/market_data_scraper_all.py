import json
import os
import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def get_market_data_from_post_code(post_code):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"https://www.krogsveen.no/prisstatistikk?zipCode={post_code}") as response:
                response_text = await response.text()
                soup = BeautifulSoup(response_text, "html.parser")
                
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
        finally:
            await session.close()

async def get_market_data_from_post_codes_from_geojson():
    
    # Get postcodes data
    postcodes_path = os.path.join(os.getcwd(), "../data/with_names/postnummers_all_with_names.json")
    # postcodes_path = "../data/without_names/.json"
    with open(postcodes_path, "r") as file:
        postcodes_data = json.load(file)
    
    # Get square meter prices asynchronously
    tasks = [get_market_data_from_post_code(postcode_dict["Postnummer"]) for postcode_dict in postcodes_data]
    results = await asyncio.gather(*tasks)
    
    # Update postcodes data and save square meter prices to file
    square_meter_prices = {}
    for i, _ in enumerate(postcodes_data):
        
        # Unpack results
        price_percentage_change_last_year, square_meter_price, price_percentage_change_last_quarter, price_percentage_change_last_month, average_sales_time, number_of_estates_sold_last_quarter, number_of_estates_sold_last_month = results[i]
        
        # Rename "Postnummer" to "postnummer", and "Poststed" to "poststed"
        postcodes_data[i]["postnummer"] = postcodes_data[i].pop("Postnummer")
        postcodes_data[i]["poststed"] = postcodes_data[i].pop("Poststed")
        
        # Add extra info to postcodes data
        postcodes_data[i]["pricePercentageChangeLastYear"] = price_percentage_change_last_year
        postcodes_data[i]["pricePercentageChangeLastQuarter"] = price_percentage_change_last_quarter
        postcodes_data[i]["pricePercentageChangeLastQuarter"] = price_percentage_change_last_month
        postcodes_data[i]["averageSalesTimeInDays"] = average_sales_time
        postcodes_data[i]["numberOfEstatesSoldLastQuarter"] = number_of_estates_sold_last_quarter
        postcodes_data[i]["numberOfEstatesSoldLastMonth"] = number_of_estates_sold_last_month
        
        # Update average square meter price in geojson
        postcodes_data[i]["averageSquareMeterPrice"] = square_meter_price
        
        # Update average price for 20m2, 30m2, ..., 200m2
        start_square_meter_size = 20
        end_square_meter_size = 200
        step_size = 10
        for j in range(start_square_meter_size, end_square_meter_size + 1, step_size):
            postcodes_data[i][f"averagePrice{j}m2"] = square_meter_price * j
        
        # Add square meter price to dictionary for square meter prices json
        square_meter_prices[postcodes_data[i]["postnummer"]] = square_meter_price
    
    # Set final paths
    final_path_market_data = "../data/postnummers_all_with_market_data.json"
    final_path_square_meter_prices = "../data/postnummers_all_square_meter_prices.json"
    
    # Save post codes market data
    with open(final_path_market_data, "w") as file:
        json.dump(postcodes_data, file, indent=2)
    
    # Save square meter prices to file
    with open(final_path_square_meter_prices, "w") as file:
        file.write(json.dumps(square_meter_prices, indent=2))
        file.write("\n")
    
    print(f"Saved {len(postcodes_data)} post codes data successfully to {final_path_market_data}")
    print(f"Saved {len(square_meter_prices.keys())} square meter prices to {final_path_square_meter_prices}")
    return None


async def main():
    await get_market_data_from_post_codes_from_geojson()


if __name__ == "__main__":
    asyncio.run(main())
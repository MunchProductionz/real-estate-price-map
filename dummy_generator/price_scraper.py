import json
import os
import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def get_square_meter_prices_from_post_code(post_code):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"https://www.krogsveen.no/prisstatistikk?zipCode={post_code}") as response:
                response_text = await response.text()
                soup = BeautifulSoup(response_text, "html.parser")
                square_meter_price = soup.find_all("div", class_="css-j9s53t")
                square_meter_price = int(square_meter_price[1].text.replace("Kvadratmeterpris", "").replace("kr", "").replace(" ", ""))
                print(f"Post code: {post_code}, Square meter price: {square_meter_price}")
                return square_meter_price
        finally:
            await session.close()

async def get_square_meter_prices_from_post_codes_from_geojson():
    
    # Get postcodes data
    postcodes_path = os.path.join(os.getcwd(), "../frontend/public/data/postcodes.json")
    with open(postcodes_path, "r") as file:
        postcodes_data = json.load(file)
    
    # Get square meter prices asynchronously
    tasks = [get_square_meter_prices_from_post_code(feature["properties"]["postnummer"]) for feature in postcodes_data["features"]]
    square_meter_prices_results = await asyncio.gather(*tasks)
    
    # Update postcodes data and save square meter prices to file
    square_meter_prices = {}
    for i, feature in enumerate(postcodes_data["features"]):
        
        # Update average square meter price in geojson
        postcodes_data["features"][i]["properties"]["averageSquareMeterPrice"] = square_meter_prices_results[i]
        
        # Update average price for 20m2, 30m2, ..., 200m2
        for j in range(20, 201, 10):
            postcodes_data["features"][i]["properties"][f"averagePrice{j}m2"] = square_meter_prices_results[i] * j
        
        # Add square meter price to dictionary for square meter prices json
        square_meter_prices[feature["properties"]["postnummer"]] = square_meter_prices_results[i]
    
    # Save updated post codes data
    with open(postcodes_path, "w") as file:
        json.dump(postcodes_data, file, indent=2)
    
    # Save square meter prices to file
    with open("../frontend/public/data/square_meter_prices.json", "w") as file:
        file.write(json.dumps(square_meter_prices, indent=4))
        file.write("\n")
    
    print(f"Updated {len(postcodes_data['features'])} post codes data successfully to ../frontend/public/data/postcodes.json")
    print(f"Saved {len(square_meter_prices.keys())} square meter prices to ../frontend/public/data/square_meter_prices.json")
    return None


async def main():
    await get_square_meter_prices_from_post_codes_from_geojson()


if __name__ == "__main__":
    asyncio.run(main())
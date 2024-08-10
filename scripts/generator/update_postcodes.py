import json
import os
from tqdm import tqdm
from scripts import DummyGenerator

def update_postcodes():
    
    # Get paths
    dummy_data_path = os.path.join(os.getcwd(), "../../frontend/public/data/dummy_data.json")
    postcodes_path = os.path.join(os.getcwd(), "../../frontend/public/data/postcodes.geojson")
    
    # Generate dummy data
    dummy_generator = DummyGenerator(
        output_path=dummy_data_path,
        number_of_records=1300
        )
    dummy_generator.generate_dummy_data()
    
    # Load dummy data
    with open(dummy_data_path, "r") as file:
        dummy_data = json.load(file)
        
    # Load post codes data
    with open(postcodes_path, "r") as file:
        postcodes_data = json.load(file)
    
    # Update average prices to match dummy data
    for post_code in tqdm(dummy_data.keys()):

        # Find post code in postcodes data
        for i, feature in enumerate(postcodes_data["features"]):
            if feature["properties"]["postnummer"] == post_code:
                
                # Update average price
                postcodes_data["features"][i]["properties"]["averagePrice"] = dummy_data[post_code]["average_price"]
            
    # Save updated post codes data
    with open(postcodes_path, "w") as file:
        json.dump(postcodes_data, file, indent=2)
    
    # Print success message
    return print(f'Updated {len(postcodes_data["features"])} post codes data successfully')


## Helper Methods ##
def get_max_postcode(postcodes_path):
    with open(postcodes_path, "r") as file:
        postcodes_data = json.load(file)
        
    # Find max post code
    max_postcode = 0
    for feature in postcodes_data["features"]:
        if int(feature["properties"]["postnummer"]) > int(max_postcode):
            max_postcode = feature["properties"]["postnummer"]
    return max_postcode

def get_min_postcode(postcodes_path):
    with open(postcodes_path, "r") as file:
        postcodes_data = json.load(file)
        
    # Find min post code
    min_postcode = 9999
    for feature in postcodes_data["features"]:
        if int(feature["properties"]["postnummer"]) < int(min_postcode):
            min_postcode = feature["properties"]["postnummer"]
    return min_postcode

def get_postcode_stats():
    postcodes_path = os.path.join(os.getcwd(), "../../frontend/public/data/postcodes.geojson")
    min_post_code = get_min_postcode(postcodes_path)
    max_post_code = get_max_postcode(postcodes_path)
    
    print(f"Min post code: {min_post_code}")
    print(f"Max post code: {max_post_code}")

if __name__ == "__main__":
    
    update_postcodes()
    # get_postcode_stats()
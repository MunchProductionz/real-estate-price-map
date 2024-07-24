import json
import os
import random
from datetime import datetime, timedelta
from tqdm import tqdm

class DummyGenerator:
    
    def __init__(self, output_path: str, number_of_records: int) -> None:
        self.output_path = output_path
        self.number_of_records = number_of_records
        self.generator_settings = {
            "last_updated_min_date": datetime.strptime("2023-01-01", "%Y-%m-%d"),
            "last_updated_max_date": datetime.now(),
            "post_code_min": 0,                         # Oslo min: 0010,   Trondheim min: 7010
            "post_code_max": 1300,                       # Oslo max: 0582,   Trondheim max: 7068
            "average_price_min": 2000000,               # 2 million
            "average_price_max": 10000000,              # 10 million
        }
        self.generated_data_categorized = {
            "last_updated": [],
            "post_code": [],
            "average_price": []
        }
        self.generated_data = {}
        
    def generate_dummy_data(self):
        
        # Input validation
        self.is_valid_number_of_records()
        
        # Generate dummy data
        last_updated_dates = self.get_valid_last_updated_dates()
        post_codes = self.get_valid_post_codes()
        average_prices = self.get_valid_average_prices()
        
        for i in tqdm(range(self.number_of_records), desc="Generating Dummy Data"):
            dummy_record = {
                "last_updated": last_updated_dates[i].strftime("%Y-%m-%d"),
                "post_code": post_codes[i],
                "average_price": average_prices[i]
            }
            self.add_dummy_record(dummy_record)
        
        # Save dummy data to file
        with open(self.output_path, "w") as f:
                f.write(json.dumps(self.generated_data, indent=4))
                f.write("\n")
        
        return print(f"Generated {self.number_of_records} dummy records in {self.output_path}")
    

    ## Helper Methods ##
    def set_generator_settings(self, settings: dict):
        self.generator_settings = settings
    
    def get_generator_settings(self):
        return self.generator_settings
    
    def get_generated_data(self):
        return self.generated_data
    
    def get_generated_data_categorized(self):
        return self.generated_data_categorized

    def get_dummy_record(self, post_code: str):
        return self.generated_data[post_code]
    
    def is_valid_number_of_records(self):
        is_valid = False
        
        # Check if number of records is within valid range
        if self.number_of_records >= 0:
            number_of_valid_records = self.generator_settings["post_code_max"] - self.generator_settings["post_code_min"]
            if self.number_of_records <= number_of_valid_records:
                is_valid = True
        
        # Raise exception if invalid
        if is_valid == False:
            raise Exception(f"Invalid number of records: {self.number_of_records}, must be less than or equal to {number_of_valid_records}")

        return None

    def add_dummy_record(self, dummy_record: dict):
        
        # Add each field to categorized data
        self.generated_data_categorized["last_updated"].append(dummy_record["last_updated"])
        self.generated_data_categorized["post_code"].append(dummy_record["post_code"])
        self.generated_data_categorized["average_price"].append(dummy_record["average_price"])
        
        # Add dummy record to generated data
        self.generated_data[dummy_record["post_code"]] = dummy_record
        
        return None
    
    def get_valid_last_updated_dates(self):
        
        # Get date range
        last_updated_min_date = self.generator_settings["last_updated_min_date"]
        last_updated_max_date = self.generator_settings["last_updated_max_date"]
        number_of_dates = (last_updated_max_date - last_updated_min_date).days
        
        # Generate all dates within range
        dates_within_range = []
        for days_since_last_updated_min_date in range(number_of_dates):
            date = last_updated_min_date + timedelta(days=days_since_last_updated_min_date)
            dates_within_range.append(date)
        
        # Get random date
        last_updated_dates = [random.choice(dates_within_range) for _ in range(self.number_of_records)]
        
        return last_updated_dates
    
    def get_valid_post_codes(self):
        
        # Get post code range
        post_code_min = self.generator_settings["post_code_min"]
        post_code_max = self.generator_settings["post_code_max"]
        
        # Generate all post codes within range and shuffle
        post_codes_within_range = list(range(post_code_min, post_code_max))
        random.shuffle(post_codes_within_range)
        
        # Get random post codes from shuffled list
        post_codes = post_codes_within_range[:self.number_of_records]
        
        # Format post codes
        post_codes = self.get_formatted_post_codes(post_codes)
        
        return post_codes
    
    def get_valid_average_prices(self):
        
        # Get random average prices
        average_price_min = self.generator_settings["average_price_min"]
        average_price_max = self.generator_settings["average_price_max"]
        
        # Generate all average prices within range and shuffle
        average_prices_within_range = list(range(average_price_min, average_price_max))
        
        # Get random average prices from list
        average_prices = [random.choice(average_prices_within_range) for _ in range(self.number_of_records)]
        
        return average_prices

    def get_formatted_post_codes(self, post_codes: list):
        
        # Format post codes
        formatted_post_codes = []
        for post_code in post_codes:
            formatted_post_code = str(post_code).zfill(4)       # Pad with zeros in the beginning
            formatted_post_codes.append(formatted_post_code)
        
        return formatted_post_codes

if __name__ == "__main__":
    output_path = os.path.join(os.getcwd(), "../frontend/public/data/dummy_data.json")
    
    dummy_generator = DummyGenerator(
        output_path=output_path,
        number_of_records=1300
        )
    dummy_generator.generate_dummy_data()
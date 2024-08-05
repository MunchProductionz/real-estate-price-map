import json
import os
import pandas as pd
from pprint import pprint

def get_and_store_postnummers(municipality: str = "", with_names: bool = False, group_by_municipality: bool = False) -> dict:
    """Get postnummers in a specified municipality from an Excel file.
    
    Args:
        municipality (str): Municipality.
        with_names (bool): Include poststed names.
        group_by_municipality (bool): Group by municipality.
        
    Returns:
        None
    """
    
    data = pd.read_excel("../data/Postnummerregister.xlsx", sheet_name="Postnummerregister")
    path_string = "_all"
    folder_string = ""

    # Zfill postnummer
    data["Postnummer"] = data["Postnummer"].astype(str).str.zfill(4)

    # Filter data
    if municipality != "":
        data = data.loc[data["Poststed"] == municipality]
        path_string = f"_{municipality.lower()}"
    
    # Alter data based on with_names flag
    if with_names:
        data = data[["Postnummer", "Poststed"]]     # Get postnummers and poststed
        path_string += "_with_names"
        folder_string = "/with_names"
        
        # Alter data based on group_by_municipality flag
        if group_by_municipality:
            data = data.groupby("Poststed")["Postnummer"].apply(list).reset_index(name="Postnummer")
            path_string += "_grouped_by_municipality"
            folder_string += "_grouped_by_municipality"
        
    else:
        data = data[["Postnummer"]]                 # Get only postnummers
        path_string += "_without_names"
        folder_string = "/without_names"
    
    # Write to JSON file
    final_path = f"../data{folder_string}/postnummers{path_string}.json"
    if not os.path.exists(final_path): os.makedirs(os.path.dirname(final_path), exist_ok=True)
    data.to_json(final_path, orient="records", indent=4)
    
    # Print confirmation
    if municipality == "":
        print(f"Stored all {len(data)} postnummers in Norway to {final_path}")
    print(f"Stored {len(data)} postnummers in {municipality} to {final_path}")
    
def main():
    
    # Poststeder
    municipality = ""
    # municipality = "OSLO"
    # municipality = "TRONDHEIM"
    # municipality = "BERGEN"
    # municipality = "STAVANGER"
    # municipality = "TROMSØ"
    municipalities = ["", "OSLO", "TRONDHEIM", "BERGEN", "STAVANGER", "TROMSØ"]
    
    # Flag
    with_names = True
    group_by_municipality = True
    
    # Configurations
    configurations = {"1": { "with_names": False, "group_by_municipality": False},
                      "2": {"with_names": True, "group_by_municipality": False},
                      "3": {"with_names": True, "group_by_municipality": True}}
    
    # Get and store postnummers
    for _, config in configurations.items():
        for municipality in municipalities:
            get_and_store_postnummers(
                municipality=municipality,
                with_names=config["with_names"],
                group_by_municipality=config["group_by_municipality"]
            )
    
if __name__ == "__main__":
    main()
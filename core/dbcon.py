import json
import os

class dbcon:
    dict = []
    data = []

    def selects(self):
        dbcon.data.clear()
        # Open the JSON file and load the data
        DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/data.json')
        with open(DATA_PATH, 'r') as f:

            dbcon.data = json.load(f)

        # Select the keyword_search values from the data and append them to a list of dictionaries
        dict_list = []
        for item in dbcon.data:
            dict_list.append({"ks": item["keyword_search"]})

        return dict_list

    def add_new_data(self):
        keys_new = self
        dbcon.data.clear()
        # Read the existing JSON data
        with open('../data/excel_data_json.json', 'r') as f:
            dbcon.data = json.load(f)
        # Generate a new ID for the new item
        new_id = len(dbcon.data) + 1
        # Create a new dictionary for the new item
        new_item = {"id": new_id, "keyword_search": keys_new}
        # Add the new item to the existing data
        dbcon.data.append(new_item)
        # Write the updated data back to the JSON file
        with open('../data/data.json', 'w') as f:
            json.dump(dbcon.data, f)
        # Call the selects() method to retrieve the updated data
        dbval = dbcon.selects(self)
        return dbval



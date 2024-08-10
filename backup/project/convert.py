import json

# Read JSON data from the file
with open("app/output.json", "r") as file:
    data = json.load(file)

# Initialize an empty set to store unique combinations
unique_combinations = set()

# Initialize an empty list to store unique dictionaries
unique_data = []

# Iterate through the data and check for duplicates
for item in data:
    # Convert the dictionary to a tuple to check for uniqueness
    combination = (item["disease"], item["age"], item["gender"], item["severity"], item["drug"])
    if combination not in unique_combinations:
        # If the combination is unique, add it to the set and append the dictionary to the unique_data list
        unique_combinations.add(combination)
        unique_data.append(item)

# Write the unique data back to the file
with open("app/output.json", "w") as outfile:
    json.dump(unique_data, outfile, indent=4)

print("Unique data has been saved back to output.json")

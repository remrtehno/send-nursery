import json

# Load the JSON file into a dictionary
with open('email_data.json', 'r') as file:
    data = json.load(file)

# Create a new dictionary to store unique entries
unique_data = {}

# Loop through the original dictionary and remove duplicates
for key, value in data.items():
    if value not in unique_data.values():
        unique_data[key] = value

# Save the unique data back to the JSON file
with open('unique_json_file.json', 'w') as file:
    json.dump(unique_data, file, indent=4)

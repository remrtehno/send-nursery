import json

# Load the data from unique_json_file.json
with open('unique_json_file.json', 'r') as file:
    data1 = json.load(file)

# Load the data from unique_json_file-poznan.json
with open('emails.json', 'r') as file:
    data2 = json.load(file)

# Ensure both are dictionaries
if isinstance(data1, dict) and isinstance(data2, dict):
    # Remove matching entries in data2
    for key in list(data1.keys()):
        if key in data2 and data2[key] == data1[key]:
            del data1[key]
else:
    print("One or both files do not contain valid dictionaries.")

# Save the updated data back to unique_json_file-poznan.json
with open('unique_emails_cleared.json', 'w') as file:
    json.dump(data1, file, indent=4)

print('Matching entries have been removed from unique_json_file-poznan.json')

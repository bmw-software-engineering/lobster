import json
from pathlib import Path
import sys


def update_cpptest_output_file(filename, expected_location):
    # Load the JSON data from the file
    with open(filename, 'r') as file:
        data = json.load(file)
    
    for item in data['data']:
        if 'location' in item:
            location = item['location']
            if 'file' in location:                   
                location['file'] = (str(
                    Path(expected_location) / Path(location['file']).name
                    ).replace("\\", "/"))

    # Save the updated JSON data back to the same file
    with open(filename, 'w') as fd:
        json.dump(data, fd, indent=2)
        fd.write("\n")

    print(f"Cpptest JSON data updated and saved back to '{filename}'.")


if __name__ == "__main__":
    update_cpptest_output_file(sys.argv[1])

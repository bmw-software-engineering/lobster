import json
import subprocess
import sys


def update_json(filename):
    # Load the JSON data from the file
    with open(filename, 'r') as file:
        data = json.load(file)

    # Traverse the JSON structure and update the 'loc' values
    for level in data['levels']:
        for item in level['items']:
            location = item['location']
            if 'file' in location:
                exec_commit_id = subprocess.check_output(
                    ["git", "rev-parse", "HEAD"]).decode().strip()
                location['exec_commit_id'] = exec_commit_id

    # Save the updated JSON data back to the same file
    with open(filename, 'w') as fd:
        json.dump(data, fd, indent=2)
        fd.write("\n")

    print(f"JSON data updated and saved back to '{filename}'.")


if __name__ == "__main__":
    update_json(sys.argv[1])

import json
import subprocess

# File name
file_name = 'expected-output.lobster'

# Load the JSON data from the file
with open(file_name, 'r') as file:
    data = json.load(file)

# Traverse the JSON structure and update the 'loc' values
for level in data['levels']:
    for item in level['items']:
        location = item['location']
        exec_commit_id = subprocess.check_output(
            ["git", "log", "-n", "1", "--format=%H", "--",
             "../../../"+location['file']]).decode().strip()
        location['exec_commit_id'] = exec_commit_id

# Save the updated JSON data back to the same file
with open(file_name, 'w') as fd:
    json.dump(data, fd, indent=2)
    fd.write("\n")

print(f"JSON data updated and saved back to '{file_name}'.")
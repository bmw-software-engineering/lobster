import json
import sys


def delete_commit_ids_json(filename):
    # Load the JSON data from the file
    with open(filename, 'r') as file:
        data = json.load(file)

    # Traverse the JSON structure and update the 'loc' values
    for level in data['levels']:
        for item in level['items']:
            location = item['location']
            if 'file' in location:
                del location['exec_commit_id']

    # Save the updated JSON data back to the same file
    with open(filename, 'w') as fd:
        json.dump(data, fd, indent=2)
        fd.write("\n")

    print(f"Deleted exec ids from integration test reference_output "
          f"file and saved back to '{filename}'.")


if __name__ == "__main__":
    delete_commit_ids_json(sys.argv[1])

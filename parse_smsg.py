import argparse
import json

def parse_file(file_path):
    result = []
    with open(file_path, 'r') as file:
        json_objects = json.loads(file.read())

        for data in json_objects:
            # Parse each JSON object
            if data["storageRewrites"] > 0 or data["workgroupRewrites"] > 0 or data["f32Rewrites"] > 0:
                result.append(data)
    return result

def main():
    parser = argparse.ArgumentParser(description="Parse a file containing info from SMSG pass.")
    parser.add_argument("file", help="Path to the input file containing JSON objects.")
    args = parser.parse_args()

    non_zero_rewrites = parse_file(args.file)
    print(json.dumps(non_zero_rewrites, indent=2))

if __name__ == "__main__":
    main()


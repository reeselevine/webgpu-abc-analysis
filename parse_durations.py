import argparse
import json
from collections import defaultdict

def parse_file(file_path):
    result = {}
    with open(file_path, 'r') as file:
        content = file.readlines()

    # Process each line, stripping 'index.html' if present
    clean_lines = [line.split(" ", 1)[-1].strip() if "index.html" in line else line.strip() for line in content]

    # Combine lines back into a single string to handle JSON objects separated by blank lines
    combined_content = "\n".join(clean_lines)

    # Split by empty lines (assumes JSON objects are separated by blank lines)
    json_objects = [obj.strip() for obj in combined_content.split("\n\n") if obj.strip()]

    for obj in json_objects:
        try:
            # Parse each JSON object
            data = json.loads(obj)

            entry_points = data["entryPoints"]
            # This line sorts shader hashes, which means compute passes with the same shaders called in different orders are grouped
            data["shaderHashes"].sort()
            if len(data["shaderHashes"]) == 1:
                shader_hashes = data["shaderHashes"][0]
            else:
                shader_hashes = tuple(data["shaderHashes"])  # Use tuple to make it hashable for dict keys
            start = data["start"]
            end = data["end"]
            duration_ns = end - start
            duration_ms = duration_ns / 1_000_000  # Convert nanoseconds to milliseconds

            # Group by sets of shaderHashes
            if shader_hashes not in result:
                result[shader_hashes] = {
                    "entry_points": entry_points,
                    "durations": []
                }
            result[shader_hashes]["durations"].append(duration_ms)
        except (json.JSONDecodeError, KeyError, TypeError):
            # Skip invalid or incomplete JSON objects
            continue

    return result

def calculate_stats(data):
    stats = {}
    total_duration = sum(
        sum(group_data["durations"]) for group_data in data.values()
    )

    for shader_hashes, group_data in data.items():
        durations = group_data["durations"]
        runtime_pct = sum(durations) / total_duration
        average = sum(durations) / len(durations)
        stats[str(shader_hashes)] = {  # Convert tuple to string for JSON compatibility
            "avg": average,
            "runtime_pct": runtime_pct,
            "times_called": len(durations),
            "entry_points": group_data["entry_points"]
        }
    return stats

def main():
    parser = argparse.ArgumentParser(description="Parse JSON objects, group by shaderHashes, and calculate statistics.")
    parser.add_argument("file", help="Path to the input file containing JSON objects.")
    args = parser.parse_args()

    # Parse the file and calculate durations
    grouped_data = parse_file(args.file)

    # Calculate statistics
    stats = calculate_stats(grouped_data)

    # Print the results
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    main()

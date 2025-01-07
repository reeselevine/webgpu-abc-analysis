import argparse
import json

def parse_file(file_path):
    result = {}
    with open(file_path, 'r') as file:
        content = file.read()

        # Split the content by empty lines (assumes JSON objects are separated by blank lines)
        json_objects = [obj.strip() for obj in content.split("\n\n") if obj.strip()]

        for obj in json_objects:
            try:
                # Parse each JSON object
                data = json.loads(obj)
                entry_point = data["entryPoint"]
                start = data["start"]
                end = data["end"]
                duration_ns = end - start
                duration_ms = duration_ns / 1_000_000  # Convert nanoseconds to milliseconds

                # Append the duration in milliseconds to the list for this entry point
                if entry_point not in result:
                    result[entry_point] = []
                result[entry_point].append(duration_ms)
            except (json.JSONDecodeError, KeyError, TypeError):
                # Skip invalid or incomplete JSON objects
                continue
    return result

def calculate_stats(durations):
    stats = {}
    total_duration = 0
    for entry_point, duration_list in durations.items():
        total_duration += sum(duration_list)
    for entry_point, duration_list in durations.items():
        runtime_pct = sum(duration_list)/total_duration
        average = sum(duration_list) / len(duration_list)
        stats[entry_point] = {
            "avg": average,
            "runtime_pct": runtime_pct,
            "times_called": len(duration_list)
        }
    return stats

def main():
    parser = argparse.ArgumentParser(description="Parse a file containing JSON objects, calculate durations, and compute averages.")
    parser.add_argument("file", help="Path to the input file containing JSON objects.")
    args = parser.parse_args()

    # Parse the file and calculate durations
    durations = parse_file(args.file)

    stats = calculate_stats(durations)

    # Print the results
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    main()


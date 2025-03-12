import argparse
import json

def parse_file(file_path):
    result = []
    with open(file_path, 'r') as file:
        json_objects = json.loads(file.read())
        total_shaders = 0
        compile_times = []
        compile_pcts = []
        for data in json_objects:
            total_shaders += 1
            compile_times.append(int(data["raiseTimeUs"]))
            compile_pcts.append(int(data["smsgTimeUs"])/int(data["raiseTimeUs"]))
            # Parse each JSON object
            if data["storageRewrites"] > 0 or data["workgroupRewrites"] > 0 or data["f32Rewrites"] > 0:
                result.append(data)
        print("Total Shaders: " + str(total_shaders))
        #print(compile_pcts)
        print("Avg smsg compile pct: {}".format(sum(compile_pcts)/len(compile_pcts)))
        print("Max smsg compile pct: {}".format(max(compile_pcts)))
        print("Avg overall compile time: {}".format(sum(compile_times)/len(compile_times)))
        print("Max overall compile time: {}".format(max(compile_times)))
    return result

def main():
    parser = argparse.ArgumentParser(description="Parse a file containing info from SMSG pass.")
    parser.add_argument("file", help="Path to the input file containing JSON objects.")
    args = parser.parse_args()

    non_zero_rewrites = parse_file(args.file)
    print(json.dumps(non_zero_rewrites, indent=2))

if __name__ == "__main__":
    main()


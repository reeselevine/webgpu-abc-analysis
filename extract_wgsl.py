def extract_wgsl(input_file, output_prefix):
    with open(input_file, 'r') as infile:
        in_wgsl_block = False
        in_msl_block = False
        wgsl_block_count = 0
        outfile = None

        for line in infile:
            if "// Dumped WGSL:" in line:
                in_wgsl_block = True
                in_msl_block = False
                wgsl_block_count += 1
                if outfile:
                    outfile.close()
                outfile = open(f"{output_prefix}_{wgsl_block_count}.wgsl", 'w')
                continue
            elif "/* Dumped generated MSL */" in line:
                in_wgsl_block = False
                in_msl_block = True
                if outfile:
                    outfile.close()
                outfile = None
                continue

            if in_wgsl_block:
                if outfile:
                    outfile.write(line)

        if outfile:
            outfile.close()

input_file = 'shaders.log'
output_prefix = 'shader'
extract_wgsl(input_file, output_prefix)

print("Extracted WGSL code blocks have been written to separate files.")


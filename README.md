A set of tools for analyzing WebGPU shaders and their performance using our custom Chrome build.

## Extract WGSL

Flags: `--enable-dawn-features=dump_shaders,disable_symbol_renaming`. 

Download from console after running shaders and use `extract_wgsl.py` to parse out the WGSL shaders.

## Remove Duplicates

Given a directory of shaders, removes duplicate shaders with `remove_duplicates.py`.

## Parse Durations

Flags: `----enable-dawn-features=allow_unsafe_apis,internal_compute_timestamp_queries --disable-dawn-features=timestamp_quantization`

Download from console after running shaders and use `parse_durations.py` to get performance data for each shader

## Graph Duration Differences

Given two sets of duration data, use `graph_differences.py` to show the difference in performance between them.

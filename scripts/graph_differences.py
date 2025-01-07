import json
import matplotlib.pyplot as plt
import numpy as np
import pdb

def plot_avg_ratio(file1, file2):
    # Load JSON data from the files
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    # Extract function names and compute the ratios
    function_names = []
    ratios = []

    for func_name, metrics1 in data1.items():
        if func_name in data2:
            avg1 = metrics1.get("avg", 0)
            avg2 = data2[func_name].get("avg", 0)

            if avg2 != 0:  # Avoid division by zero
                ratio = avg1 / avg2
            else:
                ratio = np.nan  # Use NaN to indicate undefined ratios

            function_names.append(func_name)
            ratios.append(ratio)

    # Sort by function names for a consistent display
    sorted_indices = np.argsort(function_names)
    function_names = [function_names[i] for i in sorted_indices]
    ratios = [ratios[i] for i in sorted_indices]

    # Plot the ratios
    plt.figure(figsize=(12, 6))
    plt.bar(function_names, ratios, color='skyblue')
    plt.axhline(1, color='red', linestyle='--', label='Ratio = 1')
    plt.xticks(rotation=90, fontsize=10)
    plt.ylabel('Ratio of avg (file1 / file2)')
    plt.title('Comparison of avg Ratios Between Two JSON Files')
    plt.legend()
    plt.tight_layout()

    # Display the plot
    plt.show()

# Example usage:
# plot_avg_ratio('file1.json', 'file2.json')import json
import matplotlib.pyplot as plt
import numpy as np

def plot_avg_ratio(file1, file2):
    # Load JSON data from the files
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    # Extract function names and compute the ratios
    function_names = []
    ratios = []
    total_time_enabled = 0.0
    total_time_disabled = 0.0
    for func_name, metrics1 in data1.items():
        if func_name in data2:
            avg1 = metrics1.get("avg", 0)
            avg2 = data2[func_name].get("avg", 0)

            #pdb.set_trace()
            if avg2 != 0:  # Avoid division by zero
                ratio = avg1 / avg2
            else:
                ratio = np.nan  # Use NaN to indicate undefined ratios

            function_names.append(func_name)
            ratios.append(ratio)
            total_time_enabled += avg1 * metrics1.get("times_called", 0)
            total_time_disabled += avg2 * data2[func_name].get("times_called", 0)

    total_speedup = total_time_enabled/total_time_disabled
    print("total speedup: " + str(total_speedup))

    # Sort by function names for a consistent display
    sorted_indices = np.argsort(function_names)
    function_names = [function_names[i] for i in sorted_indices]
    ratios = [ratios[i] for i in sorted_indices]

     # Sort by function names for a consistent display
    sorted_indices = np.argsort(function_names)
    function_names = [function_names[i] for i in sorted_indices] + ["TOTAL SPEEDUP"]
    ratios = [ratios[i] for i in sorted_indices] + [total_speedup]

    # Plot the ratios
    plt.figure(figsize=(12, 6))
    bars = plt.bar(function_names, ratios, color='skyblue')
    tbar = plt.bar(["TOTAL SPEEDUP"], [total_speedup], color = 'yellow')
    plt.axhline(1, color='red', linestyle='--', label='Ratio = 1')
    plt.xticks(rotation=90, fontsize=10)
    plt.ylabel('Ratio of avg (enabled / disabled)')
    plt.title('Comparison of avg Ratios Between Enabled Checks and Disabled Checks')
    plt.legend()
    plt.tight_layout()

    # Add ratio values above the bars
    for bar, ratio in zip(bars, ratios):
        if not np.isnan(ratio):  # Only add text for valid ratios
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{ratio:.2f}', 
                     ha='center', va='bottom', fontsize=8)
    plt.text(tbar[0].get_x() + tbar[0].get_width() / 2, tbar[0].get_height(), f'{ratio:.2f}',
             ha='center', va='bottom', fontsize=8)

    # Display the plot
    plt.savefig("ratio_graph.png", format='png')

# Example usage:
plot_avg_ratio('../checks-enabled.json', '../checks-disabled.json')

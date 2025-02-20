import argparse
import sqlite3
from random import randint
import matplotlib.pyplot as plt
import numpy as np


def db_conn(db_path):
    con = sqlite3.connect(db_path)
    return con.cursor()


## Indexes into database rows
ITERATIONS = 1
CREATED_AT = 2
UPDATED_AT = 3
MOBILE = 4
GLVENDOR = 5
GLRENDERER = 6
WEBGPUDESC = 10
BROWSER = 11
OS = 13

def classify_framework(renderer, os, browser):
    if "Apple" in renderer or "macOS" in os:
        return "Metal"
    if "Direct3D11" in renderer or "Windows" in os:
        return "DirectX"
    if "Android" in os or "Linux" in os:
        return "Vulkan"
    if "Firefox Mobile" in browser: # firefox mobile only on android
        return "Vulkan"
    if "or similar" in renderer: # at this point assume it's metal
        return "Metal"
    print("Unknown framework: ")
    print(f"  {renderer}")
    print(f"  {os}")

def classify_browser(renderer, browser):
    if "Chrome" in browser:
        return "Chromium"
    if "Edge" in browser:
        return "Chromium"
    if "Firefox" in browser:
        return "Firefox"

    if browser != "":
        print(browser)
        return browser
    print("Unknown browser:")
    print(f"  {browser}")

def classify_vendor(glvendor, renderer, webgpu_desc):
    if "Apple M" in renderer or "Apple GPU" in renderer:
        return "Apple"
    if "Qualcomm" in renderer or "Qualcomm" in glvendor:
        return "Qualcomm"
    if "ARM" in renderer or "ARM" in glvendor:
        return "ARM"
    if "NVIDIA" in renderer:
        return "NVIDIA"
    if "Intel" in renderer:
        return "Intel"
    if "AMD" in renderer:
        return "AMD"
    if "Samsung" in renderer or "Samsung" in glvendor:
        return "Samsung"

    if "Generic Renderer" in renderer:
        print("Check generic renderer")
        return "Qualcomm"

    print("Unknown vendor:")
    print(f"  {glvendor}")
    print(f"  {renderer}")
    print(f"  {webgpu_desc}")


## Dummy data for now
def analyze_tracking(cursor):
    query = "select * from tracking;"
    tracking_info = cursor.execute(query)
    data = dict()
    framework_totals = dict()
    browser_totals = dict()
    vendor_totals = dict()
    total_fuzzing_time = 0
    total_iterations = 0
    unique_combos = 0
    for row in tracking_info:
        iterations = row[ITERATIONS]
        fuzzing_time = row[UPDATED_AT] - row[CREATED_AT]
        total_fuzzing_time += fuzzing_time
        total_iterations += iterations
        glvendor = row[GLVENDOR]
        renderer = row[GLRENDERER]
        webgpu_desc = row[WEBGPUDESC]
        browser = row[BROWSER]
        os = row[OS]

        framework = classify_framework(renderer, os, browser)
        final_browser = classify_browser(renderer, browser)
        vendor = classify_vendor(glvendor, renderer, webgpu_desc)

        if framework:
            if framework not in data:
                data[framework] = dict()
            if framework not in framework_totals:
                framework_totals[framework] = { "fuzzing_time": fuzzing_time, "iterations": iterations }
            else:
                framework_totals[framework]["fuzzing_time"] += fuzzing_time
                framework_totals[framework]["iterations"] += iterations
            if final_browser:
                if final_browser not in data[framework]:
                    data[framework][final_browser] = dict()
                if final_browser not in browser_totals:
                  browser_totals[final_browser] = { "fuzzing_time": fuzzing_time, "iterations": iterations }
                else:
                  browser_totals[final_browser]["fuzzing_time"] += fuzzing_time
                  browser_totals[final_browser]["iterations"] += iterations

                if vendor:
                    if vendor not in data[framework][final_browser]:
                        unique_combos += 1
                        data[framework][final_browser][vendor] = { "fuzzing_time": fuzzing_time, "iterations": iterations }
                    else:
                        data[framework][final_browser][vendor]["fuzzing_time"] += fuzzing_time
                        data[framework][final_browser][vendor]["iterations"] += iterations

                    if vendor not in vendor_totals:
                      vendor_totals[vendor] = { "fuzzing_time": fuzzing_time, "iterations": iterations }
                    else:
                      vendor_totals[vendor]["fuzzing_time"] += fuzzing_time
                      vendor_totals[vendor]["iterations"] += iterations
    print(data)
    print(framework_totals)
    print(browser_totals)
    print(vendor_totals)
    print(f"Total fuzzing time: {(total_fuzzing_time/60)/60} hours")
    print(f"Total iterations: {total_iterations}")
    print(f"Unique combos: {unique_combos}")
    return data


def graph_tracking(data):
    # Initialize variables for plotting
    frameworks = list(data.keys())
    browsers = sorted(
        {browser for framework in data.values() for browser in framework.keys()}
    )
    vendors = sorted(
        {
            vendor
            for framework in data.values()
            for browser in framework.values()
            for vendor in browser.keys()
        }
    )

    fig, ax = plt.subplots(figsize=(12, 10))

    # Calculate positions with additional whitespace between frameworks
    x = []
    width = 0.2
    bar_positions = []
    browser_labels = []
    framework_labels = []

    # Prepare data for plotting with additional whitespace between frameworks
    position = 0
    seen_vendors = set()
    for i, framework in enumerate(frameworks):
        framework_browsers = []
        framework_has_data = False
        for j, browser in enumerate(browsers):
            # Get the values for each vendor, defaulting to 0 if vendor is not present
            values = [
                data[framework].get(browser, {}).get(vendor, {}).get("fuzzing_time", 0) for vendor in vendors
            ]
            # Round to nearest minute
            values = [v / 60 for v in values]

            if any(values):  # Only plot bars if there is at least one non-zero value
                framework_browsers.append(browser)
                x.append(position * (width + 0.05))  # Increase space between bars
                bar_positions.append(position)
                browser_labels.append(browser)
                framework_has_data = True

                # Plot the bars for each vendor
                bottom = 0
                for k, value in enumerate(values):
                    if value > 0:
                        ax.bar(
                            x[-1],
                            value,
                            width,
                            bottom=bottom,
                            label=vendors[k] if vendors[k] not in seen_vendors else "",
                            color=f"C{k}",
                        )
                        seen_vendors.add(vendors[k])
                        bottom += value
                position += 1

        if framework_has_data:
            # Calculate framework label position with additional whitespace
            framework_position = (
                np.mean(x[-len(framework_browsers) :]) if len(x) > 0 else 0
            )
            framework_labels.append((framework_position, framework))
            position += 0.4  # Add extra space between different frameworks

        # Set x-axis labels for browsers
        ax.set_xticks(x)
        ax.set_xticklabels(browser_labels, rotation=45, fontsize=24)

    # Add framework labels beneath the grouped browser labels
    for position, framework in framework_labels:
        ax.text(position, -200, framework, ha="center", va="top", fontsize=28)

    # Customize chart
    ax.set_ylabel("Fuzzing Time (minutes)", fontsize=28)
    ax.yaxis.set_tick_params(labelsize=24)
    ax.legend(title="Vendors", title_fontsize=24, fontsize=24, loc="upper right")
    plt.tight_layout()
    plt.savefig("tracking.pdf")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("db_path", help="Path to sqlite database")
    args = parser.parse_args()
    cursor = db_conn(args.db_path)
    data = analyze_tracking(cursor)
    graph_tracking(data)


if __name__ == "__main__":
    main()

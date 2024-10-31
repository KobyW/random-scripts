import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# 1. Parsing the data from the CSV

def parse_data_from_csv(handle, filename="./TuningOct22.csv"):
    df = pd.read_csv(filename)
    html_data = df[df['Handle'] == handle]['Body (HTML)'].iloc[0]

    # Extracting relevant data using regex
    factory_hp, factory_torque = map(int, re.findall(r"Factory:</strong>\s*?(\d+)\s*HP.*?(\d+)\s*lb-ft", html_data)[0])
    stage1_hp, stage1_torque = map(float, re.findall(r"Stage 1 Tune:</strong>\s*?(\d+(\.\d+)?)\s*HP.*?(\d+(\.\d+)?)\s*lb-ft", html_data)[0][::2])
    stage2_hp, stage2_torque = map(float, re.findall(r"Stage 2 Tune:</strong>\s*?(\d+(\.\d+)?)\s*HP.*?(\d+(\.\d+)?)\s*lb-ft", html_data)[0][::2])
    
    # Calculating gains
    stage1_gain_hp = stage1_hp - factory_hp
    stage1_gain_torque = stage1_torque - factory_torque
    stage2_gain_hp = stage2_hp - factory_hp
    stage2_gain_torque = stage2_torque - factory_torque

    parsed_data = {
        "factory_hp": factory_hp,
        "factory_torque": factory_torque,
        "stage1_hp": stage1_hp,
        "stage1_torque": stage1_torque,
        "stage2_hp": stage2_hp,
        "stage2_torque": stage2_torque,
        "stage1_gain_hp": stage1_gain_hp,
        "stage1_gain_torque": stage1_gain_torque,
        "stage2_gain_hp": stage2_gain_hp,
        "stage2_gain_torque": stage2_gain_torque,
    }

    return parsed_data
def aston_parse_data_from_csv(handle, filename="./TuningOct22.csv"):
    """
    Parse tuning data specifically for the Aston Martin product with the updated structure.
    """
    if handle != "aston-martin-vantage-412-tune":
        raise ValueError("This function is specifically designed for the 'aston-martin-vantage-412-tune' handle.")

    df = pd.read_csv(filename)
    html_data = df[df['Handle'] == handle]['Body (HTML)'].iloc[0]

    # Extracting relevant data using regex for the updated structure
    factory_hp, factory_torque = map(int, re.findall(r"STOCK:\s(\d+)\sHP\s/\s(\d+)\slb-ft", html_data)[0])
    stage1_hp, stage1_torque = map(int, re.findall(r"STAGE 1 TUNE:\s+(\d+)\sHP\s/\s(\d+)\slb-ft", html_data)[0])
    stage2_hp, stage2_torque = map(int, re.findall(r"STAGE 2 TUNE:\s+(\d+)\sHP\s/\s(\d+)\slb-ft", html_data)[0])

    # Calculating gains
    stage1_gain_hp = stage1_hp - factory_hp
    stage1_gain_torque = stage1_torque - factory_torque
    stage2_gain_hp = stage2_hp - factory_hp
    stage2_gain_torque = stage2_torque - factory_torque

    parsed_data = {
        "factory_hp": factory_hp,
        "factory_torque": factory_torque,
        "stage1_hp": stage1_hp,
        "stage1_torque": stage1_torque,
        "stage2_hp": stage2_hp,
        "stage2_torque": stage2_torque,
        "stage1_gain_hp": stage1_gain_hp,
        "stage1_gain_torque": stage1_gain_torque,
        "stage2_gain_hp": stage2_gain_hp,
        "stage2_gain_torque": stage2_gain_torque,
    }

    return parsed_data

# Parsing the data for the given handle

handle = "aston-martin-vantage-412-tune"
if handle == "aston-martin-vantage-412-tune":
    aston_martin_parsed_data = aston_parse_data_from_csv(handle)
else:
    aston_martin_parsed_data = parse_data_from_csv(handle)


# 2. Plotting the parsed data

def plot_tuning_bars_final_v14(data):
    """
    Plot the tuning bars for horsepower and torque with further vertical title spacing and centered title.
    """
    # Define the labels and values
    labels = ['Horsepower (HP)', 'Torque (lb-ft)']
    factory_values = [data['factory_hp'], data['factory_torque']]
    stage1_values = [data['stage1_gain_hp'], data['stage1_gain_torque']]
    stage2_values = [data['stage2_gain_hp'], data['stage2_gain_torque']]
    
    # Create a figure and axis with modern aesthetics
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.grid(False)
    ax.tick_params(axis='both', which='both', length=0)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.xaxis.set_tick_params(width=0.5)
    ax.yaxis.set_tick_params(width=0.5)
    plt.xticks(fontsize=20, fontweight='bold')
    ax.get_yaxis().set_visible(False)  # Remove the y-axis

    # Bar width
    bar_width = 0.4
    index = np.arange(len(labels))

    # Plot bars
    bars1 = ax.barh(index, factory_values, bar_width, label='Factory', color='#22232b', edgecolor='none')
    bars2 = ax.barh(index, stage1_values, bar_width, label='Stage 1', color='orange', edgecolor='none',
                    left=factory_values)
    bars3 = ax.barh(index, stage2_values, bar_width, label='Stage 2', color='red', edgecolor='none',
                    left=np.array(factory_values) + np.array(stage1_values))

    # Label the bars with the gain values (correctly positioned) and added units
    for i, bar in enumerate(bars2):
        if stage1_values[i]:
            y_pos = bar.get_y() + bar.get_height()/2
            unit = "HP" if labels[i] == 'Horsepower (HP)' else "TQ"
            if labels[i] == 'Horsepower (HP)':
                y_pos += 0.3
                ax.text(bar.get_x() + bar.get_width()/2, y_pos,
                        f"+{stage1_values[i]:.0f} {unit}", va='center', ha='center', color='black', fontsize=20, fontweight='bold')
            else:
                y_pos -= 0.3
                ax.text(bar.get_x() + bar.get_width()/2, y_pos,
                        f"+{stage1_values[i]:.0f} {unit}", va='center', ha='center', color='black', fontsize=20, fontweight='bold')

    for i, bar in enumerate(bars3):
        if stage2_values[i]:
            y_pos = bar.get_y() + bar.get_height()/2
            unit = "HP" if labels[i] == 'Horsepower (HP)' else "TQ"
            x_pos = bar.get_x() + bar.get_width() + 0  # Further adjusted to the left
            if labels[i] == 'Horsepower (HP)':
                y_pos += 0.3
                ax.text(x_pos, y_pos,
                        f"+{stage2_values[i]:.0f} {unit}", va='center', ha='center', color='black', fontsize=20, fontweight='bold')
            else:
                y_pos -= 0.3
                ax.text(x_pos, y_pos,
                        f"+{stage2_values[i]:.0f} {unit}", va='center', ha='center', color='black', fontsize=20, fontweight='bold')

    # Adjust title positions and color them appropriately
    factory_title = f"Factory: {data['factory_hp']:.0f}HP {data['factory_torque']:.0f}TQ"
    stage1_title = f"Stage 1: {data['stage1_hp']:.0f}HP {data['stage1_torque']:.0f}TQ"
    stage2_title = f"Stage 2: {data['stage2_hp']:.0f}HP {data['stage2_torque']:.0f}TQ"
    
    ax.text(0.5, 1.19, factory_title, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=24, fontweight='bold')
    ax.text(0.5, 1.14, stage1_title, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=24, fontweight='bold', color='orange')
    ax.text(0.5, 1.09, stage2_title, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=24, fontweight='bold', color='red')
    
    # Restore bar titles
    ax.text(-50, 0, "Horsepower (HP)", color="black", va='center', ha='right', fontsize=20, fontweight='bold')
    ax.text(-50, 1, "Torque (lb-ft)", color="black", va='center', ha='right', fontsize=20, fontweight='bold')
    
    # Show the plot
    plt.tight_layout()
    plt.show()

# Plotting the tuning bars for the Aston Martin product with the final adjustments
plot_tuning_bars_final_v14

# Plotting the tuning bars for the Aston Martin product
plot_tuning_bars_final_v14(aston_martin_parsed_data)


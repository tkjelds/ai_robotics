from glob import glob
import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent

json_path = BASE_DIR / "experiments.json"

palette = {
    "Black": "black",
    "White": "gray",   # white not visible on white background
    "Red": "red",
    "Yellow": "gold"
}

with open(json_path, 'r') as f:
    experiment_data = json.load(f)

def save_plot(plot,filename):
    filename = filename.replace(" ", "_") + ".png"
    path = BASE_DIR / "visualisations"
    plot.savefig(path / filename)

### DATA FRAME CREATION ###
df_sensor_overlap = pd.DataFrame.from_dict(
    experiment_data["Relfection_value_given_sensor_overlap"],
    orient="index",
    columns=["value"]
)

df_overshoot = pd.DataFrame(
    [(forwards, value) for forwards, values in experiment_data["overshoot"].items() for value in values],
    columns=["Amount_of_forwards", "Distance (mm)"]
)

df_turn_overshoot_left = pd.DataFrame(
    [(turns,value) for turns, values in experiment_data["Degrees_turned_after_amount_of_left_turns"].items() for value in values],
    columns=["Amount_of_turns", "Distance (mm)"]
)
df_turn_overshoot_right = pd.DataFrame(
    [(turns,value) for turns, values in experiment_data["Degrees_turned_after_amount_of_right_turns"].items() for value in values],
    columns=["Amount_of_turns", "Distance (mm)"]
)

df_planner_runtime = pd.DataFrame(experiment_data["Time_to_run_planner_given_class_competion_map"], columns=["Time to run planner (s)"])


### PLOTS ###

## Sensor overlap plot ### 
plt.figure()
plt.title("Reflection value given sensor overlap")
plt.ylabel("Reflection value")
plt.xlabel("Distance (mm)")
sns.lineplot(data=df_sensor_overlap)

save_plot(plt, "sensor_overlap")
plt.show()

## Robot overshoot plot
plt.figure()
plt.title("Overshoot given Amount of Forwards")
sns.boxplot(data=df_overshoot, x="Amount_of_forwards", y="Distance (mm)")
sns.swarmplot(data=df_overshoot, x="Amount_of_forwards", y="Distance (mm)", color="black")

save_plot(plt, "forward_overshoot")
plt.show()

## Turn overshoot left plot
plt.figure()
plt.title("Overshoot given Amount of Left Turns")
sns.boxplot(data=df_turn_overshoot_left, x="Amount_of_turns", y="Distance (mm)")
sns.swarmplot(data=df_turn_overshoot_left, x="Amount_of_turns", y="Distance (mm)", color="black")

save_plot(plt, "left_turn_overshoot")
plt.show()
    
## Turn overshoot right plot
plt.figure()
plt.title("Overshoot given Amount of Right Turns")
sns.boxplot(data=df_turn_overshoot_right, x="Amount_of_turns", y="Distance (mm)")
sns.swarmplot(data=df_turn_overshoot_right, x="Amount_of_turns", y="Distance (mm)", color="black")

save_plot(plt, "right_turn_overshoot")
plt.show()

## Planner runtime plot
plt.figure()
plt.title("Time to run planner given class competition map")
sns.boxplot(data=df_planner_runtime, y="Time to run planner (s)")
sns.swarmplot(data=df_planner_runtime, y="Time to run planner (s)", color="black")

save_plot(plt, "execution_time_planner")
plt.show()
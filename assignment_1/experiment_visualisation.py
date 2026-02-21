from glob import glob
import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent

json_path = BASE_DIR / "measurements" / "experiment_data.json"

with open(json_path, 'r') as f:
    experiment_data = json.load(f)

def save_plot(plot,filename):
    filename = filename.replace(" ", "_") + ".png"
    path = BASE_DIR / "visualisations"
    plot.savefig(path / filename)

### DATA FRAME CREATION ###
df_colours = pd.DataFrame(experiment_data["colour_measurement"])
df_colours = df_colours.T
df_colours.index = df_colours.index.str.replace("mm", "").astype(int)
df_colours = df_colours.sort_index()


df_exploration = pd.DataFrame(experiment_data["exploration"])

df_edgeDetection = pd.DataFrame(
    [(angle, value) for angle, values in experiment_data["edgeDetection"].items() for value in values],
    columns=["Entrance Degree", "Distance (mm)"]
)

df_objectDetection = pd.DataFrame(
    [(object, distance) for object, distances in experiment_data["objectDetection"].items() for distance in distances],
    columns=["Object", "Distance (mm)"]
)

df_cornerEvacuation = pd.DataFrame(experiment_data["cornerEvacuation"], columns=["Corner Evacuation Time (s)"])


### PLOTS

palette = {
    "Black": "black",
    "White": "gray",   # white not visible on white background
    "Red": "red",
    "Yellow": "gold"
}

plt.figure()
sns.lineplot(
    data=df_colours,
    palette=palette,
    marker="o"
)

plt.xlabel("Distance (mm)")
plt.ylabel("Value")
plt.title("Reflection Measurements by Distance")

save_plot(plt, "Reflection_Measurements_by_Distance")
plt.show()

plt.figure(figsize=(8,6))

plt.title("Exploration Data Heatmap")
sns.heatmap(df_exploration, annot=True, )
save_plot(plt, "Exploration Data Heatmap")
plt.show()

sns.boxplot(data=df_edgeDetection, x="Entrance Degree", y="Distance (mm)")
sns.swarmplot(data=df_edgeDetection, x="Entrance Degree", y="Distance (mm)", color="black")
plt.title("Nearest Contact Distance vs Entrance Degree")
save_plot(plt, "Nearest Contact Distance vs Entrance Degree")
plt.show()

plt.title("Object Detection Distances")
sns.boxplot(data=df_objectDetection, x="Object", y="Distance (mm)")
sns.swarmplot(data=df_objectDetection, x="Object", y="Distance (mm)", color="black")
save_plot(plt, "Object Detection Distances")
plt.show()

plt.title("Distribution of Corner Evacuation Time")

sns.boxplot(y=df_cornerEvacuation["Corner Evacuation Time (s)"])
sns.stripplot(y=df_cornerEvacuation["Corner Evacuation Time (s)"], color="black")
save_plot(plt, "Corner Evacuation Time Distribution")
plt.show()
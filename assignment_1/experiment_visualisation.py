import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent

json_path = BASE_DIR / "experiment_data.json"

with open(json_path, 'r') as f:
    experiment_data = json.load(f)


df_exploration = pd.DataFrame(experiment_data["exploration"])

sns.heatmap(df_exploration, annot=True,)
plt.show()
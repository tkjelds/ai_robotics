import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


datasets = [
    {"data": "data/results_epoch_5.jsonl", "save_name": "epoch_5.png"},
    {"data": "data/results_epoch_10.jsonl", "save_name": "epoch_10.png"},
    {"data": "data/results_epoch_20.jsonl", "save_name": "epoch_20.png"},
    {"data": "data/results_epoch_30.jsonl", "save_name": "epoch_30.png"},
    {"data": "data/results_epoch_40.jsonl", "save_name": "epoch_40.png"},
    {"data": "data/results_epoch_50.jsonl", "save_name": "epoch_50.png"}
]

def plot_fitness(
    filepath,
    start_epoch_at_one=True,
    save_path=None,
    show=False,
    figsize=(10, 6),
    save_name=None,
    # metric="average_fitness_per_epoch"
):


    data = []
    with open(filepath, "r") as f:
        for line in f:
            data.append(json.loads(line))

    df = pd.DataFrame(data)


    rows = []
    for _, row in df.iterrows():
        num_robots = row["num_robots"]
        average_fitness_list = row["average_fitness_per_epoch"]
        max_fitness_list = row["max_fitness_per_epoch"]

        for epoch, fitness in enumerate(average_fitness_list):
            rows.append({
                "epoch": epoch + 1 if start_epoch_at_one else epoch,
                "average_fitness": fitness,
                "max_fitness": max_fitness_list[epoch],
                "num_robots": num_robots
            })

    plot_df = pd.DataFrame(rows)

    # --- Plot ---
    sns.set(style="whitegrid")
    plt.figure(figsize=figsize)

    sns.lineplot(
        data=plot_df,
        x="epoch",
        y="average_fitness",
        hue="num_robots",
        marker="o",
        hue_order=sorted(plot_df["num_robots"]),
        legend="full"
    )

    plt.title("Average Fitness per Epoch")
    plt.xlabel("Epoch")
    plt.ylabel("Average Fitness")
    plt.legend(title="Number of Robots", fontsize=12, title_fontsize=14)

    plt.tight_layout()

    # --- Save / Show ---

    plt.savefig(f"visualisation/plots/average_fitness_{save_name}", dpi=300)

    if show:
        plt.show()
    else:
        plt.close()
        
    plt.figure(figsize=figsize)
    
    sns.lineplot(
        data=plot_df,
        x="epoch",
        y="max_fitness",
        hue="num_robots",
        marker="o",
        hue_order=sorted(plot_df["num_robots"]),
        legend="full"
    )
    
    plt.title("Max Fitness per Epoch")
    plt.xlabel("Epoch")
    plt.ylabel("Max Fitness")
    plt.legend(title="Number of Robots", fontsize=12, title_fontsize=14)
    
    plt.tight_layout()
    plt.savefig(f"visualisation/plots/max_fitness_{save_name}", dpi=300)

    if show:
        plt.show()
    else:
        plt.close()
        
        
        
def plot_max_fitness_overall(filepath, save_name=None, show = False):
    import json
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt

    data = []
    with open(filepath, "r") as f:
        for line in f:
            data.append(json.loads(line))

    df = pd.DataFrame(data)

    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 5))

    sns.lineplot(
        data=df,
        x="num_robots",
        y="max_fitness_overall",
        marker="o"
    )

    plt.title("Max Fitness Overall vs Number of Robots")
    plt.xlabel("Number of Robots")
    plt.ylabel("Max Fitness Overall")

    plt.tight_layout()


    plt.savefig(f"visualisation/plots/max_fitness_overall_{save_name}", dpi=300)

    if show:
        plt.show()
    else:
        plt.close()
    
for path in datasets:
    plot_fitness(filepath=path["data"], save_name=path["save_name"])
    plot_max_fitness_overall(filepath=path["data"], save_name=path["save_name"])

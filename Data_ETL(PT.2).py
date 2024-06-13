import pandas as pd
import numpy as np

all_player_stats = pd.read_csv("nba_player_stats_with_names.csv")

# Reorder columns to move PLAYER_NAME to the front
columns = ['PLAYER_NAME'] + [col for col in all_player_stats.columns if col != 'PLAYER_NAME']
all_player_stats = all_player_stats[columns]

# Display the updated DataFrame
print("Updated DataFrame with PLAYER_NAME at the front:")
print(all_player_stats.head)

# Save the updated DataFrame to a new CSV file
all_player_stats.to_csv("nba_stats_with_names.csv", index=False)
import pandas as pd
from pandas import array
import numpy as np
import sqlalchemy
import nba_api
from nba_api.stats.endpoints import commonplayerinfo  

all_stats_players = pd.read_csv("nba_stats_with_names.csv")


# Check for NaN values in the DataFrame and print rows with missing values
missing_values = all_stats_players.isna()




# Print the rows and columns where values are missing
print("Rows and columns with missing values:")
for column in all_stats_players.columns:
    missing_in_column = missing_values[missing_values[column]].index
    if not missing_in_column.empty:
        if(column == "PLAYER_NAME"):
            print(f"Column '{column}' has missing names in rows: {missing_in_column.tolist()}")
        else:
            print(f"Column '{column}' has missing values in rows: {missing_in_column.tolist()}")

# Alternatively, print the entire DataFrame showing where NaN values are
print("DataFrame with NaN values indicated:")
print(missing_values)

# Filter rows where PLAYER_NAME is missing
missing_names_df = all_stats_players[all_stats_players['PLAYER_NAME'].isna()]

def get_player_name(player_id):
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id, timeout=60)
    player_data = player_info.get_data_frames()[0]
    if not player_data.empty:
        return player_data.loc[0, 'DISPLAY_FIRST_LAST']
    else:
        return None

# Apply the get_player_name function to query names and update only the missing names
missing_names_df['PLAYER_NAME'] = missing_names_df['PLAYER_ID'].apply(get_player_name)

# Update the original DataFrame with the updated missing names
all_stats_players.update(missing_names_df)

# Save the updated DataFrame back to CSV
all_stats_players.to_csv("nba_stats_with_names_updated.csv", index=False)

# Check how many values in PLAYER_NAME are still missing
missing_names_count = all_stats_players['PLAYER_NAME'].isna().sum()
print("Number of missing names after update:", missing_names_count)


# Get the columns containing quantitative data
quantitative_columns = all_stats_players.select_dtypes(include=[np.number]).columns.tolist()

# Fill missing quantitative values with zeros
all_stats_players[quantitative_columns] = all_stats_players[quantitative_columns].fillna(0)

# Print the updated DataFrame
print(all_stats_players)
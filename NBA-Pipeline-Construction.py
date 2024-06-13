#NBA-Pipeline-Construction

#import nessecary libraries
import pandas as pd
import numpy as np
import time
import datetime as dts
from sqlalchemy import create_engine
import pyodbc
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import requests 
from requests.exceptions import RequestException


#Add Comments...
#retrieve all the players
all_players = players.get_players()
all_players_df = pd.DataFrame(all_players)

def get_player_stats(player_id, retries=3):
    for attempt in range(retries):
        try:
            career = playercareerstats.PlayerCareerStats(player_id=player_id)
            return career.get_data_frames()[0]
        except requests.exceptions.ReadTimeout:
            if attempt < retries - 1:
                print(f"Timeout for player ID {player_id}. Retrying...")
                time.sleep(5)  # Wait before retrying
            else:
                print(f"Failed to retrieve data for player ID {player_id} after {retries} attempts.")
                return pd.DataFrame()  # Return an empty DataFrame on failure

# Step 3: Collect all player stats in batches
all_player_stats = pd.DataFrame()
batch_size = 50  # Number of players to process in each batch

for start in range(0, len(all_players_df), batch_size):
    end = start + batch_size
    batch = all_players_df['id'][start:end]

    for player_id in batch:
        player_stats = get_player_stats(player_id)
        all_player_stats = pd.concat([all_player_stats, player_stats], ignore_index=True)

    # Save intermediate results to CSV (optional)
    all_player_stats.to_csv('nba_player_stats_intermediate.csv', index=False)
    print(f"Processed players {start} to {end}")

# Move the PLAYER_NAME column to the front
columns = ['PLAYER_NAME'] + [col for col in all_player_stats.columns if col != 'PLAYER_NAME']
all_player_stats = all_player_stats[columns]
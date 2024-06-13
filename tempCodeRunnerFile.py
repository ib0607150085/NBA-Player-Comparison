# Get the columns containing quantitative data
quantitative_columns = all_stats_players.select_dtypes(include=[np.number]).columns.tolist()

# Fill missing quantitative values with zeros
all_stats_players[quantitative_columns] = all_stats_players[quantitative_columns].fillna(0)

# Print the updated DataFrame
print(all_stats_players)
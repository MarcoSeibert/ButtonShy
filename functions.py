def get_game_data_by_name(json_data, game_name):
    for game in json_data:
        if game["name"] == game_name:
            return game
    return None
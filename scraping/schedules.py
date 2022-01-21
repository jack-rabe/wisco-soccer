import requests
import sys
import json
import logging
from bs4 import BeautifulSoup
from urls import get_schedule_url, set_up_driver
from utils import extract_contents

def parse_schedule(team_name, year=2021):
    url = get_schedule_url(team_name, year, last_request=True)
    schedule_page = requests.get(url)
    parsed_page = BeautifulSoup(schedule_page.content, 'html.parser')
    games = parsed_page.find(class_="statTable").find_all('tr', class_='compactGameList')

    games_array = []
    for game in games:
        other_team = extract_contents(game.find(class_='teamName'))
        game_location = extract_contents(game.contents[5].find(class_='scheduleListTeam'))
        is_home_game = '@' not in game_location
        if is_home_game:
            home_team = team_name
            away_team = other_team
        else:
            home_team = other_team
            away_team = team_name

        dateTag = game.contents[1]
        scoreTag = game.find(class_='game_link_referrer')

        outcome = extract_contents(game.find(class_='scheduleListResult'))
        winner = team_name if outcome == 'W' else other_team
        winner = 'tie' if outcome == 'T' else winner
        try:
            game_json = {
                    'date': f'{extract_contents(dateTag)}, {year}',
                    'winner': winner,
                    'score': extract_contents(scoreTag),
                    'home': home_team,
                    'away': away_team
                    }
            games_array.append(game_json)
        except Exception as e:
            pass

    return games_array

#  set_up_driver()
#  team_name, date = sys.argv[1], sys.argv[2]
#  response = json.dumps(parse_schedule(team_name, date))
#  print(response)

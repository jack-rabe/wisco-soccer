import requests
import sys
import json
import logging
from bs4 import BeautifulSoup
from urls import get_roster_url, get_schedule_url, get_stats_url, set_up_driver

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
        outcomeTag = game.find(class_='scheduleListResult')
        scoreTag = game.find(class_='game_link_referrer')
        try:
            game_json = {
            'date': f'{extract_contents(dateTag)} {year}',
            'outcome': extract_contents(outcomeTag),
            'score': extract_contents(scoreTag),
            'home': home_team,
            'away': away_team
            }
            games_array.append(game_json)
        except Exception as e:
            pass

    return games_array

# some teams do not have roster pages, in this case, there will be no positions
def parse_roster(team_name, year=2021):
    try:
        url = get_roster_url(team_name, year)
        roster_page = requests.get(url)
        parsed_page = BeautifulSoup(roster_page.content, 'html.parser')
        roster_table = parsed_page.find(id='rosterListingTableBodyPlayer')

        players = []
        for row in roster_table.contents:
            # filter out navigable strings
            if hasattr(row, 'contents'):
                numTag = row.find(class_='number')
                nameTag = row.find(class_='name').find('a')
                posTag = row.find(class_='position')
                gradYearTag = row.contents[-2]
                try:
                    player_json = {
                        'num': extract_contents(numTag),
                        'name': extract_contents(nameTag),
                        'pos': extract_contents(posTag),
                        'gradYear': extract_contents(gradYearTag)
                    }
                    players.append(player_json)
                except Exception as e:
                    logging.error('Could not extract contents of a player', exc_info=True)
        return players
    except Exception as e:
        url = get_stats_url(team_name, year)
        stats_page = requests.get(url)
        parsed_page = BeautifulSoup(stats_page.content, 'html.parser')
        stats_table = parsed_page.find(class_='NginTableWrapper')
        players = stats_table.find_all(class_='odd') + stats_table.find_all(class_='even')

        for player in players:
            player_json = {
                'num': extract_contents(player.find(class_='jersey-number')),
                'name': extract_contents(player.find(class_='statPlayer').find('a'))
            }
            print(player_json)
    
# returns a list of all team
def parse_teams(conference='all'):
    pass

def extract_contents(tag):
    if hasattr(tag, 'contents') and len(tag.contents) > 0:
        return tag.contents[0].strip()
    else:
        return None

set_up_driver()

# team_name, date = sys.argv[1], sys.argv[2]
# response = json.dumps(parse_schedule(team_name, date))
# print(response)

team_name, date = sys.argv[1], sys.argv[2]
response = json.dumps(parse_roster(team_name, date))
print(response)
import requests
import sys
import json
import logging
from bs4 import BeautifulSoup
from urls import get_roster_url, get_stats_url, set_up_driver
from utils import extract_contents

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
        print(url)
        stats_page = requests.get(url)
        try:
            parsed_page = BeautifulSoup(stats_page.content, 'html.parser')
            stats_table = parsed_page.find(class_='NginTableWrapper')
            player_tags = stats_table.find_all(class_='odd') + stats_table.find_all(class_='even')

            for tag in player_tags:
                player_json = {
                    'num': extract_contents(tag.find(class_='jersey-number')),
                    'name': extract_contents(tag.find(class_='statplayer').find('a'))
                }
                players.append(player_json)
            return players
        except Exception as e:
            logging.error(f'No player stats exists for {team} in {year}')

set_up_driver()
team_name, date = sys.argv[1], sys.argv[2]
response = json.dumps(parse_roster(team_name, date))
print(response)


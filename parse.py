import requests
from bs4 import BeautifulSoup
from urls import get_roster_url, get_schedule_url, get_stats_url

def parse_schedule(team_name, year=2021):
    url = get_schedule_url(team_name, year, last_request=True)
    schedule_page = requests.get(url)
    parsed_page = BeautifulSoup(schedule_page.content, 'html.parser')
    games = parsed_page.find(class_="statTable").find_all('tr', class_='compactGameList')

    games_array = []
    for game in games:
        other_team = game.find(class_='teamName').contents[0]
        game_location = game.contents[5].find(class_='scheduleListTeam').contents[0]
        is_home_game = '@' not in game_location
        if is_home_game:
            home_team = team_name
            away_team = other_team
        else:
            home_team = other_team
            away_team = team_name

        json = {
          'date': f'{game.contents[1].contents[0].strip()} {year}',
          'outcome': game.find(class_='scheduleListResult').contents[0].strip(),
          'score': game.find(class_='game_link_referrer').contents[0].strip(),
          'home': home_team,
          'away': away_team
         }
        games_array.append(json)
    return games_array

# some teams do not have roster pages
def parse_roster(team_name, year=2021):
    try:
        url = get_roster_url(team_name, year)
    except Exception:
        url = get_stats_url(team_name, year)
    


print(parse_schedule('Winnebago Lutheran', 2014))
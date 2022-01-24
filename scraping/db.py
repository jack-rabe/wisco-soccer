import mysql.connector
from decouple import config
from schedules import parse_schedule
from urls import get_conf_schedule_urls 
from utils import get_teams_by_conference

def set_up_database():
    cursor.execute(f'CREATE DATABASE {db_name}')
    print(f'Creating database {db_name}')
    cursor.execute(f'USE {db_name}')
    print(f'Using database {db_name}')
    cursor.execute('CREATE TABLE games (id INT AUTO_INCREMENT PRIMARY KEY, date '\
        'DATE, winner VARCHAR(50), score VARCHAR(15), home VARCHAR(50), away '\
        'VARCHAR(50))')
    print(f'Creating table games')

def reset_games_table():
    cursor.execute(f'DROP table games')
    print('Dropping games table')
    cursor.execute('CREATE TABLE games (id INT AUTO_INCREMENT PRIMARY KEY, date '\
        'DATE, winner VARCHAR(50), score VARCHAR(15), home VARCHAR(50), away '\
        'VARCHAR(50))')
    print('Creating table games')

def insert_game(game_json):
    sql = 'INSERT INTO games (date, winner, score, home, away) VALUES '\
            '(%s, %s, %s, %s, %s)'
    j = game_json
    vals = (j['date'], j['winner'], j['score'], j['home'], j['away'])
    cursor.execute(sql, vals)

username = config('USER')
password = config('PASSWORD')
db_name = 'wisco_soccer'

mydb = mysql.connector.connect(
        host="localhost",
        user='root',
        password=password
        )

cursor = mydb.cursor(buffered=True)
cursor.execute(f'USE {db_name}')
print(f'Using database {db_name}')

#  url = r'https://www.wissports.net/schedule/team_instance/6407762?subseason=751045'
#  team_name = 'Winnebago Lutheran Academy'
#  date = 2010
#  response = parse_schedule(team_name, date, url=url)
#  #  reset_games_table()
#  for game in response:
    #  insert_game(game)
seasons = []
num_games = 0
conf = 'Flyway'
urls_json = get_conf_schedule_urls(conf)
for team_name, game_urls in urls_json.items():
    idx = 0
    for year in range(2010, 2022):
        try:
            season = parse_schedule(team_name, year, url=game_urls[idx])
            seasons.append(season)
        except Exception as e:
            print(f'Error finding games for {team_name} in {year}')
        finally:
            idx += 1
for season in seasons:
    for game in season:
        insert_game(game)
        num_games += 1
mydb.commit()
print(f'{num_games} Games added to database')

cursor.execute('select * from games')
for x in cursor:
    print(x)
cursor.close()
mydb.close()

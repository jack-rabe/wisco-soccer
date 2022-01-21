import mysql.connector
from decouple import config
from schedules import parse_schedule
from urls import set_up_driver

def set_up_database():
    cursor.execute(f'CREATE DATABASE {db_name}')
    print(f'Creating database {db_name}')
    cursor.execute(f'USE {db_name}')
    print(f'Using database {db_name}')
    cursor.execute('CREATE TABLE games (id INT AUTO_INCREMENT PRIMARY KEY, date '\
        'VARCHAR(50), winner VARCHAR(50), score VARCHAR(15), home VARCHAR(50), away '\
        'VARCHAR(50)))')
    print(f'Creating table games')

def insert_game(game_json):
    sql = 'INSERT INTO games (date, winner, score, home, away) VALUES '\
            '(%s, %s, %s, %s, %s)'
    j = game_json
    print(j)
    vals = (j['date'], j['winner'], j['score'], j['home'], j['away'])
    cursor.execute(sql, vals)
    mydb.commit()
    print(f'Game sucessfully added')

username = config('USER')
password = config('PASSWORD')
db_name = 'wisco_soccer'

mydb = mysql.connector.connect(
        host="localhost",
        user='root',
        password=password
        )


game_json = {
        'date': 'January 12, 2021',
        'winner': 'Oshkosh',
        'score': '3-2', 
        'home': 'WLA',
        'away': 'Oshkosh'
        }

cursor = mydb.cursor(buffered=True)
cursor.execute(f'USE {db_name}')
print(f'Using database {db_name}')
#  insert_game(game_json)

#  set_up_driver()
#  games = parse_schedule('Neenah')
#  print(games)
#  for game in games:
    #  insert_game(game)

cursor.execute('select * from games')
for x in cursor:
    print(x)
cursor.close()
mydb.close()

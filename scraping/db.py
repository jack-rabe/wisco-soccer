import mysql.connector
from decouple import config

def set_up_database():
    cursor.execute(f'CREATE DATABASE {db_name}')
    print(f'Creating database {db_name}')
    cursor.execute(f'USE {db_name}')
    print(f'Using database {db_name}')
    cursor.execute('CREATE TABLE games (id INT AUTO_INCREMENT PRIMARY KEY, date '\
        'VARCHAR(50), outcome CHAR(1), score VARCHAR(25), home VARCHAR(255), away '\
        'VARCHAR(255), taken_from VARCHAR(255))')
    print(f'Creating table games')

def insert_game(game_json):
    global mydb
    global cursor
    sql = 'INSERT INTO games (date, outcome, score, home, away, taken_from) VALUES '\
            '(%s, %s, %s, %s, %s, %s)'
    j = game_json
    print(j)
    vals = (j['date'], j['outcome'], j['score'], j['home'], j['away'], j['taken_from'])
    cursor.execute(sql, vals)
    mydb.commit()

username = config('USER')
password = config('PASSWORD')
db_name = 'wisco_soccer'

mydb = mysql.connector.connect(
        host="localhost",
        user='root',
        password=password
        )


game_json = {
        'date': 'January 13, 2021',
        'outcome': 'L',
        'score': '2-2', 
        'home': 'WLA',
        'away': 'Neenah',
        'taken_from': 'Neenah'
        }

cursor = mydb.cursor(buffered=True)
cursor.execute(f'USE {db_name}')
print(f'Using database {db_name}')
insert_game(game_json)
cursor.execute('select * from games')
for x in cursor:
    print(x)
cursor.close()
mydb.close()



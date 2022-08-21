import psycopg2
 
user = 'postgres'
password = '1234'
db_name = 'test'
host='localhost'
port = 5432

conn = psycopg2.connect(dbname=db_name, user=user, 
                        password=password, host=host)

class User:
    def __init__(self):
        self.__name="Vasya"
        self.__scope=123


cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
results = cursor.fetchall()
print(results)

cursor.close()
conn.close()
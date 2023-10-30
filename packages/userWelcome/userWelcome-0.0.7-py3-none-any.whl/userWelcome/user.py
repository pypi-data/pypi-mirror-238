import os
import mysql.connector
from datetime import datetime

class user:
    def __init__(self):
        self.db = mysql.connector.connect(
            host = "mysql",
            user=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DATABASE')
        )
        self.cursor = self.db.cursor()

    def create_db(self):
        try:
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS userWelcome")
            return True
        except Exception as e:
            print(e)
            print("errore creazione")
            return False

    def get_username(self):
        return input("Benvenuto! \nInserisci il tuo nome utente: ")

    def get_timestamp(self):
        return int(datetime.now().timestamp())

    def create_user_table(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS user (username varchar(255), timestamp INT)")
            return True
        except Exception as e:
            print(e)
            print("errore creazione tab")
            return False

    def add_user(self, user, ts):
        try:
            self.cursor.execute(f"INSERT INTO user (username, timestamp) VALUES ('{user}', {ts})") #nosec
            self.db.commit()
            print("Benvenuto user: ", user)
        except Exception as e:
            print(e)
            print("errore add")
            self.db.rollback()

    def print_users(self):
        try:
            self.cursor.execute("SELECT * FROM user")
            res = self.cursor.fetchall()
            print(res)
            return True
        except Exception as e:
            print(e)
            print("Errore print")
            return False

    def get_user_log(self, username):
        self.cursor.execute(f"SELECT * FROM user WHERE username='{username}'") #nosec
        results = self.cursor.fetchall()
        return results
    
    def recentUser(self, user):
        print("Bentornato", user)

    def oldUser(self, user, time):
        print(f"Ciao {user}! Da quanto tempo!")
        self.cursor.execute(f"UPDATE user set timestamp = {time} WHERE username = '{user}'") #nosec
        self.db.commit()

    def checktime(self,t1, t2):
        if t1-t2 <= 60:
            return True
        return False

def userWelcome():
    u = user()
    username = u.get_username()
    if u.create_db():
        if u.create_user_table():
            res = u.get_user_log(username)
            timestamp = u.get_timestamp()
            if res == []:
                u.add_user(username, timestamp)
            else :
                #if timestamp-res[0][1] <= 60 :
                if u.checktime(timestamp, res[0][1]):
                    u.recentUser(username)
                else :
                    u.oldUser(username, timestamp)
            u.print_users()



if __name__ == "__main__":
    userWelcome()

import os.path
import datetime
import sqlite3
import sys
import re 

from tabnanny import check
from time import timezone
from typing import List

# Connecting sql query for creating a new database and
# connecting path to the directory with the settings file
if __name__ == '__main__':
    from create_db_sql import create_status_table
    from create_db_sql import create_users_table
    from create_db_sql import insert_status
    sys.path.append('D:/!GitClones/DiscordBot/src/')
else:
    from .create_db_sql import create_status_table
    from .create_db_sql import create_users_table
    from .create_db_sql import insert_status
    sys.path.append(os.getcwdb()) 
    
from config import Config

class Database:
    __filePath = Config.get('db', 'path') + Config.get('db', 'name')
    __connection = None
    __statusList = []

    # Object constructor
    def __init__(self):
        if os.path.exists(self.__filePath):
            print('Exist')
            self.__connection = self.create_connection()
        else:
            print('Database not exist, create new one')
            self.__connection = self.create_connection()
            self.execute_query(create_status_table)
            self.execute_query(create_users_table)
            self.execute_query(insert_status)
            tempStatusList = self.execute_query('SELECT Name FROM status')
            for status in tempStatusList:
                self.__statusList.append(status[0])

    # Connecting database
    def create_connection(self):
        connection = None
        try:
            connection = sqlite3.connect(self.__filePath)
            print('Connected to SQLite DB')
        except sqlite3.Error as err_string:
            print(f''' The error in create_connection '{err_string}' occured ''')
        return connection

    # Execute SQL query
    def execute_query(self, query):
        cursor = self.__connection.cursor()
        try:
            cursor.execute(query)
            self.__connection.commit()
            return cursor.fetchall()
        except sqlite3.Error as err_string:
            print(f'''[ERROR] The error in execute_query '{err_string}' occurred''')
            return 'ERROR'

    # Add a new user
    def add_user(self, id):
        if (id.isnumeric()):
            now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours = 3)))
            result = self.execute_query(f''' INSERT INTO users (DiscordID, JoinedDatetime) VALUES ("{id}", "{now}") ''')
            return result
        else:
            print(f'[ERROR] [add_user] Invalid ID: {id}')

    # Is there a user with the specified ID
    def check_user(self, id):
        if (id.isnumeric()):
            result = self.execute_query(f'''SELECT CASE WHEN EXISTS(SELECT Name FROM users where DiscordID = '{id}') = 1 THEN "TRUE" ELSE "FALSE" END''')
            return 1 if (result[0][0] == 'TRUE') else 0
        else:
            print(f'[ERROR] The error in check_user occurred ID {id}')

    # Set user registration status
    def set_status(self, id, status):
        if self.check_user(id): 
            if status in self.__statusList:
                self.execute_query(f''' UPDATE users SET status="{status}" WHERE DiscordID="{id}" ''')
            else:
                print(f'[ERROR] [set_status] Status not exist: {status}')
                return 0
        else:
            print(f'[ERROR] [set_status] No player with such id: {id}')

    # Set user name
    def set_name(self, id, name):
        match = re.fullmatch(Config.get('db', 'name_pattern'), name)
        if (match):
            if self.check_user(id): 
                self.execute_query(f''' UPDATE users SET Name="{name}" WHERE DiscordID="{id}" ''')
            else:
                print(f'[ERROR] [set_name] No player with such id: {id}')
        else:
            print(f'[ERROR] [set_name] Invalid name: {name}')
    
    # Set user nickname
    def set_nickname(self, id, nickname):
        match = re.fullmatch(Config.get('db', 'nickname_pattern'), nickname)
        if (match):
            if self.check_user(id): 
                self.execute_query(f''' UPDATE users SET Nickname="{nickname}" WHERE DiscordID="{id}" ''')
            else:
                print(f'[ERROR] [set_nickname] No player with such id: {id}')
        else:
            print(f'[ERROR] [set_nickname] Invalid nickname: {nickname}')
    
    # Update registration date
    def update_reg_date(self, id):
        if self.check_user(id): 
            now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours = 3)))
            self.execute_query(f''' UPDATE users SET RegDatetime="{now}" WHERE DiscordID="{id}" ''')
        else:
            print(f'[ERROR] [update_reg_date] No player with such id: {id}')

    # TODO: DELETE
    def __exit__(self):
        print('EXIT')
        self.__connection.close()
        os.remove(self.__filePath)

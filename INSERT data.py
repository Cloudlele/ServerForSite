import pypyodbc
import json
import os

login = 'OlegTest'
password = '12345'
email = 'omikula123@gmail.com'
print('Login: ', login, '\n', 'Pass: ', password, '\n', 'Email: ', email)
connection = pypyodbc.connect(driver='{SQL Server}', server='DESKTOP-7GE22QK\SQLEXPRESS', database='Library')
cursor = connection.cursor()

SQLQuery = ('INSERT INTO Client(User_Login, User_Password, Email, Code_Rank) VALUES(' + "'" + login + "'" + ',' + "'" + password + "'" + ',' + "'" + email + "'" + ',' + "'1' )")
cursor.execute(SQLQuery)
try:
    connection.commit()
except Exception as e:
    print(e)
connection.close()

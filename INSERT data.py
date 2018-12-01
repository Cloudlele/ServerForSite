import pypyodbc
import json
import os

login = 'cloeferefeudlelefger'
password = '12345'

print('Login: ', login, '\n', 'Pass: ', password)
connection = pypyodbc.connect(driver='{SQL Server}', server='DESKTOP-7GE22QK\SQLEXPRESS', database='Library')
cursor = connection.cursor()

SQLQuery = ('INSERT INTO Client(User_Login, User_Password, Code_Rank) VALUES(' + "'" + login + "'" + ',' + "'" + password + "'" + ',' + "'1' )")
try:
    cursor.execute(SQLQuery)
    connection.commit()
except Exception as e:
    print(e)
connection.close()

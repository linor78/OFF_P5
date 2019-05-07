#! /usr/bin/env python3
# coding: utf-8

import mysql.connector
from mysql.connector import errorcode
import private as p
import os
TABLES = {}
TABLES['off'] = (
    "CREATE TABLE IF NOT EXISTS off ("
    "EAN BIGINT PRIMARY KEY NOT NULL,"
    "Name VARCHAR(30) NOT NULL,"
    "Category SMALLINT,"
    "Stores VARCHAR(150),"
    "Grade CHAR(1) NOT NULL,"
    "URL Char(50) NOT NULL,"
    "CONSTRAINT fk_category_off_cat FOREIGN KEY off(Category)"
    "REFERENCES categories(id)"
    ")ENGINE=InnoDB")
TABLES['mysubstituts'] =(
    "CREATE TABLE IF NOT EXISTS mysubstituts ("
    "EAN BIGINT NOT NULL,"
    "Origin BIGINT NOT NULL,"
    "CONSTRAINT fk_EAN_subs_off FOREIGN KEY mysubstituts(EAN)"
    "REFERENCES off(EAN),"
    "CONSTRAINT fk_EAN_osubs_off FOREIGN KEY mysubstituts(Origin)"
    "REFERENCES off(EAN)"
    ")ENGINE=InnoDB")
TABLES['categories'] = (
    "CREATE TABLE IF NOT EXISTS categories ("
    "id SMALLINT PRIMARY KEY AUTO_INCREMENT,"
    "Name VARCHAR(15) NOT NULL UNIQUE"
    ")ENGINE=InnoDB")
CATEGORIES = ('Lait', 'Beurre', 'Farine', 'Sodas', 'Pain')
def init_database():
    #the function try to connect to the mysql server
    try :
        mydb = mysql.connector.connect(host = p.host, user = p.user,             \
            passwd = p.passwd, database = p.dbname)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            exit(1)
    dbcursor = mydb.cursor()
    dbcursor.execute(TABLES['categories'])
    dbcursor.execute(TABLES['off'])
    dbcursor.execute(TABLES['mysubstituts'])
    for item in CATEGORIES:
    #    cmd = 'INSERT INTO categories(Name) VALUES (\'' + item + '\')'
    #    print(cmd)
        try:
            dbcursor.execute('INSERT INTO categories(Name) VALUES (\'' + item + '\')')
        except mysql.connector.Error as err:
            pass;
    mydb.commit()

def choose_action():
    choice = 0
    while choice != '1' and choice != '2' :
        os.system('clear')
        print('\n1-Quel aliment souhaitez-vous remplacer?\n')
        print('2-Retrouver mes aliments substitués.\n')
        choice = input('Veuiller rentrer le numero correspondant à votre action:\n')
    return choice
def main():
    init_database()
    choice = choose_action()
if __name__ == '__main__':
    main()

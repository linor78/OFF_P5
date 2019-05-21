#! /usr/bin/env python3
# coding: utf-8

import mysql.connector
from mysql.connector import errorcode
import private as p
import os
import requests
S1_URL = 'https://fr.openfoodfacts.org/cgi/search.pl?&tagtype_0=languages&tag_contains_0=contains&tag_0=fr&tagtype_1=categories&tag_contains_1=contains&tag_1='
S2_URL = "&search_simple=1&action=process&page_size=1000&json=1&page="
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

class list_of_products():
    def __init__(self):
        self.products = list()

    def add_product(self,tuple_of_values):
        self.products.append(tuple_of_values)
    def get_all_products(self):
        s=', '
        return s.join((str(p) for p in self.products)).replace('[','(').replace(']',')')
    def get_len(self):
        return len(self.products)
    def reset_list():
        self.products[:] = []

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
    return mydb

def choose_action():
    choice = 0
    while choice != '1' and choice != '2' :
        os.system('clear')
        print('\n      1-Quel aliment souhaitez-vous remplacer?\n')
        print('      2-Retrouver mes aliments substitués.\n')
        choice = input('Veuiller rentrer le numero correspondant à votre action:\n')
    return choice
def choose_category(dbcursor):
    category = 0
    dbcursor.execute("select * from categories order by id")
    categories = {str(a):b for (a,b) in dbcursor}
    while category not in categories.keys():
        os.system('clear')
        for key in categories.keys():
            print('     {} - {}\n'.format(key,categories[key]))
        category = input('Veuillez choisir une categorie\n')
    return int(category)

def return_values(category,jsond):

    values = list()
    value = None
    for key in COLUMNS.keys():
        try:
            value = jsond[COLUMNS[key]]
            if key == 'EAN':
                value = int(value)
                values.append(value)
            else :
                values.append(value)
        except:
            pass
    values.append(category)
    #print(values)
    return values

def get_all_pages(cursor,category,list_of_products):
    i = 1
    cursor.execute('SELECT Name FROM categories WHERE id like {}'.format(category))
    for item in cursor:
        cat_name = item[0]
    while True:
        #url = B_URL + cat_name + '/' + str(i) +'.json'
        url = S1_URL + cat_name + S2_URL + str(i)
        print(url)
        r = requests.get(url)
        jsond = r.json()
        jsond = jsond['products']
        if  not jsond:
            break
        for product in jsond:
            try:
                if product['stores'] and product['nutrition_grade_fr']:
                    list_of_products.add_product(return_values(category,product))
            except:
                pass
        i += 1

def main():
    mydb = init_database()
    products = list_of_products()
    dbcursor = mydb.cursor()
    choice = choose_action()
    category = choose_category(dbcursor)
    get_all_pages(dbcursor,category,products)
    print(products.products)
if __name__ == '__main__':
    main()

#! /usr/bin/env python3
# coding: utf-8

import mysql.connector
from mysql.connector import errorcode
import private as p
import os
import requests
COLUMNS = {'EAN': 'code', 'Name': 'product_name', 'Stores' : 'stores', 'URL': 'url', 'Grade': 'nutrition_grade_fr'}
S1_URL = 'https://fr.openfoodfacts.org/cgi/search.pl?&tagtype_0=languages&tag_contains_0=contains&tag_0=fr&tagtype_1=categories&tag_contains_1=contains&tag_1='
S2_URL = "&search_simple=1&action=process&page_size=1000&json=1&page="
INS_COLUMNS = ('Ean', 'Name', 'Stores', 'URL', 'Grade', 'Category')
TABLES = {}
TABLES['off'] = (
    "CREATE TABLE IF NOT EXISTS off ("
    "EAN BIGINT PRIMARY KEY NOT NULL,"
    "Name VARCHAR(150) NOT NULL,"
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
CATEGORIES = ('Laits', 'Beurres', 'Farines', 'Sodas', 'Pains')

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
    #dbcursor.execute('drop table mysubstituts,off,categories;')
    dbcursor.execute(TABLES['categories'])
    dbcursor.execute(TABLES['off'])
    dbcursor.execute(TABLES['mysubstituts'])
    for item in CATEGORIES:
        try:
            dbcursor.execute('INSERT IGNORE INTO categories(Name) VALUES (\'' + item + '\')')
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

def insert_products_into_off(mydb,products):
    s= ', '
    cursor = mydb.cursor()
    query = 'INSERT IGNORE into off ({}) VALUES {} ;'.format(s.join(INS_COLUMNS), products.get_all_products())
    try:
        cursor.execute(query)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    mydb.commit()

def choose_product(mydb,category):
    cursor = mydb.cursor()
    choice = 0
    index = ['1','2','3','4','5','6','7','8','9','10']
    query = 'select EAN,Name,URL from off where Category=' + str(category) + ' order by rand() limit 10;'
    cursor.execute(query)
    eans = [a for a in cursor]
    #index = range(1,len(eans))
    menu_index = dict(zip(index,eans))
    while choice not in menu_index.keys():
        os.system('clear')
        for index in menu_index.keys():
            print('\n{} - {}'.format(index,menu_index[index]).replace('(','').replace(')','').replace(', ','    -    ').replace('\'','').replace('\"',''))
        choice = input('Veuiller selectionner le produit à substitué\n')
    return menu_index[choice][0]

def choose_sub(mydb,category,product_ean):
    cursor = mydb.cursor()
    query = 'select EAN from off where EAN!=' + str(product_ean) + ' and Grade>=(select Grade from off where EAN=' + str(product_ean) + ') order by rand() limit 1;'
    cursor.execute(query)
    ean = [a for a in cursor]
    return ean[0][0]

def insert_into_mysubstituts(mydb, product_ean, sub_ean):
    cursor = mydb.cursor()
    query = 'insert into mysubstituts (EAN,Origin) values (' + str(sub_ean) + ', ' + str(product_ean) + ');'
    try:
        cursor.execute(query)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    mydb.commit()

def print_product_from_EAN(mydb,EAN):
    cursor = mydb.cursor()
    query = 'select EAN,Name,URL from off where EAN=' + str(EAN) + ';'
    try:
        cursor.execute(query)
        product = [str(a) for a in cursor]
        print(str(product).replace('[\"(', '').replace(')\"]', '').replace('\'', '').replace('\"', '').replace(',', '  -  '))
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    mydb.commit()

def substituts_list(mydb):
    cursor = mydb.cursor()
    choice = 0
    query = 'select off.EAN,Name,URL from off inner join mysubstituts on off.EAN = mysubstituts.EAN;'
    cursor.execute(query)
    eans = [a for a in cursor]
    index = range(1,len(eans)+1)
    index = [str(a) for a in index]
    menu_index = dict(zip(index,eans))
    while choice not in menu_index.keys():
        os.system('clear')
        for index in menu_index.keys():
            print('\n{} - {}'.format(index,menu_index[index]).replace('(','').replace(')','').replace(', ','    -    ').replace('\'','').replace('\"',''))
        choice = input('Veuiller selectionner le produit à substitué\n')
    return menu_index[choice][0]

def get_ean_of_origin(mydb, sub_ean):
    cursor = mydb.cursor()
    query = 'select Origin from mysubstituts where EAN=' + str(sub_ean) + ';'
    cursor.execute(query)
    ean = [a for a in cursor]
    return ean[0][0]

def choose_end():
    choice = 0
    while choice not in ('n','y'):
        choice = input('Souhaiter vous retourner au menu principal? (y/n):\n')
    return choice

def main():
    mydb = init_database()
    products = list_of_products()
    dbcursor = mydb.cursor()
    while 1:
        action = choose_action()
        if action == '1' :
            category = choose_category(dbcursor)
            get_all_pages(dbcursor,category,products)
            insert_products_into_off(mydb,products)
            #products.reset_list()
            product_ean = choose_product(mydb,category)
            sub_ean = choose_sub(mydb,category,product_ean)
            insert_into_mysubstituts(mydb, product_ean, sub_ean)
            print('\nVous avez choisi de trouver un substitut pour le produit:\n')
            print_product_from_EAN(mydb,product_ean)
            print('\nNous vous proposons le produit:\n')
            print_product_from_EAN(mydb,sub_ean)
            print('\n')
        elif action == '2':
            sub_ean = substituts_list(mydb)
            product_ean = get_ean_of_origin(mydb,sub_ean)
            print('\nVous aviez choisi de trouver un substitut pour le produit:\n')
            print_product_from_EAN(mydb,product_ean)
            print('\nNous vous avions proposer le produit:\n')
            print_product_from_EAN(mydb,sub_ean)
            print('\n')
        if choose_end() == 'n':
            break;
if __name__ == '__main__':
    main()

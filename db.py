#! /usr/bin/env python3
# coding: utf-8
import private as p
import mysql.connector
from mysql.connector import errorcode

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
TABLES['mysubstituts'] = (
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

class init_db():
    #Class who will connect the program to the database
    # and initialise the Tables if needed.
    def __init__(self):
        #Initialisation of the db connector and creation of the tables required
        #Also fill the catagory table with the CATEGORIES list
        try :
            self.con = mysql.connector.connect(host = p.host, user = p.user, \
                passwd = p.passwd, database = p.dbname)
            self.curs = self.con.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            else :
                print('Something went wrong when trying to connect \
                to the database')
            return NONE
        self.create_tables()
        self.put_categories()

    def create_tables(self):
        #Function that create the tables
        self.curs.execute(TABLES['categories'])
        self.curs.execute(TABLES['off'])
        self.curs.execute(TABLES['mysubstituts'])

    def put_categories(self):
        #Function that fill the category table
        for item in CATEGORIES:
            try:
                self.curs.execute('INSERT INTO categories(Name) VALUES \
                (\'' + item + '\')')
            except mysql.connector.Error as err:
                pass
        self.con.commit()

    def erase(self):
        #Function that erase all the tables, only used when this file is
        #executed alone
        self.curs.execute('drop table mysubstituts,off,categories;')

class select():
    def __init__(self, cursor):
        #initialisation of the db cursor
        self.curs = cursor

    def cat_name_from_id(self, id):
        #Function that return the name of the category from its id
        self.curs.execute('SELECT Name FROM categories WHERE id like {}' \
        .format(id))
        for item in self.curs:
            cat_name = item[0]
        return cat_name

    def cat_dict_id_name(self):
        #Function that return a dict of the categories id and name , used to
        #print the selection screen of the category
        self.curs.execute("select * from categories order by id")
        categories = {str(a):b for (a,b) in self.curs}
        return categories

    def prod_10_rand(self, query):
        #Function that return 10 random products from the selected category
        self.curs.execute(query)
        prods = [a for a in self.curs]
        return prods

    def get_sub(self, category, product_ean):
        #Function that return one substitut that isnt the selected product, from
        #the same category and with equal or better nutrition_grade_fr
        query = 'select EAN from off where (EAN!=' + str(product_ean) + ' and \
        Category=' + str(category) + ' and Grade<=(select Grade from off where EAN \
        =' + str(product_ean) + ')) order by rand() limit 1;'
        self.curs.execute(query)
        sub = [a for a in self.curs]
        return sub[0][0]

    def get_sub_list(self):
        #Function that return the list of all the previously saved substituts
        self.curs.execute('select off.EAN,Name,URL,Grade,Category from off inner \
        join mysubstituts on off.EAN = mysubstituts.EAN;')
        eans = [a for a in self.curs]
        return eans

    def get_prod_from_ean(self, ean):
        #Function that return a product information from its EAN
        self.curs.execute('select EAN,Name,URL,Grade,Category,Stores \
        from off where EAN=' + str(ean) + ';')
        product = [str(a) for a in self.curs]
        return product
        
    def get_ean_of_origin(self, sub_ean):
        #Function that return the substituted product's ean from
        #the substitut's ean
        query = 'select Origin from mysubstituts where EAN=' + str(sub_ean) + ';'
        self.curs.execute(query)
        ean = [a for a in self.curs]
        return ean[0][0]

def main():
    db = init_db()
    db.erase()

if __name__ == '__main__':
    main()

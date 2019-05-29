#! /usr/bin/env python3
# coding: utf-8

import mysql.connector
from mysql.connector import errorcode
import db
import view
import time
import requests
import products as p
COLUMNS = {'EAN': 'code', 'Name': 'product_name', 'Stores' : 'stores', 'URL':\
 'url', 'Grade': 'nutrition_grade_fr'}
S1_URL = 'https://fr.openfoodfacts.org/cgi/search.pl?&tagtype_0=languages&tag_c\
ontains_0=contains&tag_0=fr&tagtype_1=categories&tag_contains_1=contains&tag_1='
S2_URL = "&search_simple=1&action=process&page_size=1000&json=1&page="
INS_COLUMNS = ('Ean', 'Name', 'Stores', 'URL', 'Grade', 'Category')

class controller():
    def __init__(self, v, s, mydb, products):
        #Initialisation of the class by getting all the classes needed for the
        #program
        self.v = v
        self.s = s
        self.db = mydb
        self.products = products

    def main_menu_loop(self):
        #Main menu loop that will bring back the user to teh beginning until
        #he decide to leave
        while 1:
            action = self.v.choose_action()
            if action == '1' : #The user chose to find a substitut
                category = self.v.choose_category()
                self.get_all_pages(category)
                self.insert_products_into_off()
                self.products.reset_list()
                product_ean = self.v.choose_product(category)
                sub_ean = self.s.get_sub(category, product_ean)
                self.insert_into_mysubstituts(product_ean, sub_ean)
                self.v.print_new_sub(product_ean, sub_ean)
            elif action == '2': #The user chose to look at substitut's list
                sub_ean = self.v.substituts_list()
                if not sub_ean:
                    print('No substituts saved so far\n')
                    time.sleep(3)
                    continue
                product_ean = self.s.get_ean_of_origin(sub_ean)
                self.v.print_old_sub(product_ean, sub_ean)
            if self.v.choose_end() == 'n':
                break;

    def return_values(self, category, jsond):
        #Function that return the list of all the values we want to save in our
        #database for every product from its json object
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

    def get_all_pages(self, category):
        #Funtion that will ask the api for every page of the chosen category
        #and add the values of each product inside the products list
        i = 1
        cat_name = self.s.cat_name_from_id(category)
        while True:
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
                        self.products.add_product \
                        (self.return_values(category,product))
                except:
                    pass
            i += 1

    def insert_products_into_off(self):
        #Function that insert the products into the off table
        s= ', '
        query = 'INSERT IGNORE into off ({}) VALUES {} ;' \
        .format(s.join(INS_COLUMNS), self.products.get_all_products())
        time.sleep(2)
        try:
            self.db.curs.execute(query)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        self.db.con.commit()

    def insert_into_mysubstituts(self, product_ean, sub_ean):
        #Function that insert the substituted's eanand the substitut's ean
        #into the mysubstituts table
        query = 'insert into mysubstituts (EAN,Origin) values (' + str(sub_ean) \
        + ', ' + str(product_ean) + ');'
        try:
            self.db.curs.execute(query)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        self.db.con.commit()

def main():
    mydb = db.init_db()
    s = db.select(mydb.curs)
    products = p.list_of_products()
    v = view.view(s)
    c = controller(v, s, mydb, products)
    c.main_menu_loop()

if __name__ == '__main__':
    main()

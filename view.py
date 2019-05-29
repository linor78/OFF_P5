#! /usr/bin/env python3
# coding: utf-8

import os

class view():
    def __init__(self, s):
        #The class is initialised by getting the select class which it will user
        #to get the information to print
        self.s = s

    def choose_action(self):
        #Function that print the 2 option the user can select and send it to
        #the controller
        choice = 0
        while choice != '1' and choice != '2' :
            os.system('clear')
            print('\n      1-Quel aliment souhaitez-vous remplacer?\n')
            print('      2-Retrouver mes aliments substitués.\n')
            choice = input('Veuiller rentrer le numero correspondant à votre\
 action:\n')
        return choice

    def choose_category(self):
        #Function that print all the categories present in the categories table
        #and ask the user to select one and send it to the controller
        category = 0
        categories = self.s.cat_dict_id_name()
        while category not in categories.keys():
            os.system('clear')
            for key in categories.keys():
                print('     {} - {}\n'.format(key,categories[key]))
            category = input('Veuillez choisir une categorie\n')
        return int(category)

    def choose_product(self, category):
        #Function that will ask the user to choose between 10 products of the
        #chosen category until one valid product is chosen
        choice = 0
        index = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        query = 'select EAN,Name,URL,Grade,Category from off where Category='\
         + str(category) + ' order by rand() limit 10;'
        eans = self.s.prod_10_rand(query)
        menu_index = dict(zip(index, eans))
        while choice not in menu_index.keys():
            os.system('clear')
            for index in menu_index.keys():
                print(self.replace('\n{} - {}'.format(index,menu_index[index])))
            choice = input('Veuiller selectionner le produit à substitué\n')
        return menu_index[choice][0]

    def substituts_list(self):
        #Function that will ask the user to choose from all the substituts in
        #the list until his choice is valid
        choice = 0
        eans = self.s.get_sub_list()
        if not eans:
            return None
        index = range(1, len(eans) + 1)
        index = [str(a) for a in index]
        menu_index = dict(zip(index, eans))
        while choice not in menu_index.keys():
            os.system('clear')
            for index in menu_index.keys():
                print(self.replace('\n{} - {}'.format(index,menu_index[index])))
            choice = input('Veuiller selectionner le produit à substitué\n')
        return menu_index[choice][0]

    def choose_end(self):
        #Function that ask the user if he want to quit or go back to main menu
        choice = 0
        while choice not in ('n','y'):
            choice = input('Souhaiter vous retourner \
            au menu principal? (y/n):\n')
        return choice

    def print_new_sub(self, EAN, sub_EAN):
        #Function that print the substituted and the substitut right after
        #finding it
        print('\nVous avez choisi de trouver un substitut pour le produit:\n')
        product = self.s.get_prod_from_ean(EAN)
        print(self.replace(str(product)))
        print('\nNous vous proposons le produit:\n')
        product = self.s.get_prod_from_ean(sub_EAN)
        print(self.replace(str(product)))
        print('\n')

    def print_old_sub(self, EAN, sub_EAN):
        #Function that print the substituted and the substitut
        #from the sub_list
        print('\nVous aviez choisi de trouver un substitut pour le produit:\n')
        product = self.s.get_prod_from_ean(EAN)
        print(self.replace(str(product)))
        print('\nNous vous avions proposer le produit:\n')
        product = self.s.get_prod_from_ean(sub_EAN)
        print(self.replace(str(product)))
        print('\n')

    def replace(self, s):
        #Function that replace somme character with another for visual purpose
        return s.replace('(','').replace(')','').replace(', ','  -  ') \
        .replace('\'','').replace('\"','').replace('[', '').replace(']', '')\
        .replace('\\', '').replace('\/', '')

def main():
    pass
if __name__ == '__main__':
    main()

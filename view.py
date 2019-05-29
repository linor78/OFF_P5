#! /usr/bin/env python3
# coding: utf-8

import os

class view():
    def __init__(self, s):
        self.s = s

    def print_action(self):
        os.system('clear')
        print('\n      1-Quel aliment souhaitez-vous remplacer?\n')
        print('      2-Retrouver mes aliments substitués.\n')
        choice = input('Veuiller rentrer le numero correspondant à votre\
 action:\n')
        return choice

    def print_category(self, categories):
        os.system('clear')
        for key in categories.keys():
            print('     {} - {}\n'.format(key,categories[key]))
        category = input('Veuillez choisir une categorie\n')
        return category
    def print_10_product(self, menu_index):
        os.system('clear')
        for index in menu_index.keys():
            print(self.replace('\n{} - {}'.format(index,menu_index[index])))
        choice = input('Veuiller selectionner le produit à substitué\n')
        return choice
    def print_new_sub(self, EAN, sub_EAN):
        print('\nVous avez choisi de trouver un substitut pour le produit:\n')
        product = self.s.get_prod_from_ean(EAN)
        print(self.replace(str(product)))
        print('\nNous vous proposons le produit:\n')
        product = self.s.get_prod_from_ean(sub_EAN)
        print(self.replace(str(product)))
        print('\n')
    def print_old_sub(self, EAN, sub_EAN):
        print('\nVous aviez choisi de trouver un substitut pour le produit:\n')
        product = self.s.get_prod_from_ean(EAN)
        print(self.replace(str(product)))
        print('\nNous vous avions proposer le produit:\n')
        product = self.s.get_prod_from_ean(sub_EAN)
        print(self.replace(str(product)))
        print('\n')
    def print_sub_list(self, menu_index):
        os.system('clear')
        for index in menu_index.keys():
            print(self.replace('\n{} - {}'.format(index,menu_index[index])))
        choice = input('Veuiller selectionner le produit à substitué\n')
        return choice
    def replace(self, s):
        return s.replace('(','').replace(')','').replace(', ','  -  ') \
        .replace('\'','').replace('\"','').replace('[', '').replace(']', '')\
        .replace('\\', '').replace('\/', '')
def main():
    pass
if __name__ == '__main__':
    main()

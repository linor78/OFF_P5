#! /usr/bin/env python3
# coding: utf-8

class list_of_products():
    def __init__(self):
        self.products = list()
    def add_product(self,tuple_of_values):
        self.products.append(tuple_of_values)
    def get_all_products(self):
        s=', '
        return s.join((str(p) for p in self.products)).\
        replace('[','(').replace(']',')')
    def reset_list(self):
        self.products[:] = []


def main():
    pass
if __name__ == '__main__':
    main()

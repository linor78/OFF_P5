# OOF_P5
Program that will give the user a subsitute to the selected food using OpenFoodFacts's API.

**Functions of the program:**

The program need a function 'init_database()' that will connect to the mysql database and check if the three tables we will use in the program already exists.If the tables don't exist, it will create them. This function need the login,adress and database name of the mysql database, they will be set as constants of the program in a separate file named private.py to avoid leaking of the password on github, this file should be added to .gitignore .

The program need a function 'choose_action()' that will show the user the main menu and ask him to choose between two actions, each action is linked to a number, the user has to enter '1' or '2', if he enter a wrong choice, he is asked to do it again.This function will return the choice of the user.

The program need a function 'choose_category()' that will show the user the categories he can choose from and ask him to enter the number next to the category he want to search food in.If he enter a wrong number  he is asked to retry.This function returns the category he chose in the list. The list of the categories is taken from the database table 'categories'.

The programe need a class named list_of_products() that will contain the list of the products the program will get from the OpenFoodFacts's API and will also contain the function needed to add a product, get the lenght of the list, reset the list and get the string representation of the products to insert in the database.

The program need a function named 'return_values(category,jsond)'' that will take only the columns we need from each json product into a list  and return it

The program need a function 'get_all_pages(cursor, category, list_of_products)' that will ask the OFF Api for every page of food from the category chosen by the user as json files.Get the database cursor ,the category chosen by the user and the list_of_products as arguments, For each product who contain both 'stores' and 'nutrition_grade_fr' values, add the product to the list of products.

The program need a function 'insert_products_into_off(mydb,products)' that will insert the products into the 'off' table of the database, it will ignore any error due to duplicates during insertion.

The program need a function 'choose_product(mydb,category)' that will get 10 products of the category and ask the user to choose one, it will ask until one is choosen.it will return the ean of the chosen product.

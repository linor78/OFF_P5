# OOF_P5
Program that will give the user a subsitute to the selected food using OpenFoodFacts's API.

**Functions of the program:**

The program need a function 'init_database()' that will connect to the mysql database and check if the three tables we will use in the program already exists.If the tables don't exist, it will create them. This function need the login,adress and database name of the mysql database, they will be set as constants of the program in a separate file named private.py to avoid leaking of the password on github, this file should be added to .gitignore .

The program need a function 'choose_action()' that will show the user the main menu and ask him to choose between two actions, each action is linked to a number, the user has to enter '1' or '2', if he enter a wrong choice, he is asked to do it again.This function will return the choice of the user.

The program need a function 'choose_category()' that will show the user the categories he can choose from and ask him to enter the number next to the category he want to search food in.If he enter a wrong number  he is asked to retry.This function returns the category he chose in the list. The list of the categories is taken from the database table 'categories'.

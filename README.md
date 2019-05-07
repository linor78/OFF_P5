# OOF_P5
Program that will give the user a subsitute to the selected food using OpenFoodFacts's API.

**Functions of the program:**

The program need a function 'init_database()' that will connect to the mysql database and check if the two tables we will use in the program already exists.If the tables don't exist, it will create them. This function need the login,adress and database name of the mysql database, they will be set as constants of the program in a separate file named private.py to avoid leaking of the password on github, this file should be added to .gitignore .

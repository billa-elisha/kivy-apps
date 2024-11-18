import mysql.connector as mydbConnector
import sqlite3

class CreatSqlite3Database:
    def __init__(self):
        self.mydb = sqlite3.connect('BERMS.db')
        self.mydb
        self.usersTable()
        self.productsTable()
        self.companyDetailsTable()
        self.salesTable()
        self.deletingFoldersDates()
        self.dele()

    def usersTable(self):
        """This function is use to create the users table
        and it is called in the init method
        """
        mydb = sqlite3.connect('BERMS.db')
        mycursor = mydb.cursor()
        quary = ('''CREATE TABLE IF NOT EXISTS users(
                 user_id INTEGER PRIMARY KEY, 
                 name text NOT NULL, 
                 email text, 
                 password text NOT NULL,
                 designation text NOT NULL);''')
        mycursor.execute(quary)
        mydb.close()

    def productsTable(self):
        """This function is use to create the users table
        and it is called in the init method
        """
        mydb = sqlite3.connect('BERMS.db')
        mycursor = mydb.cursor()
        quary = ('''CREATE TABLE IF NOT EXISTS products(
                 product_id INTEGER PRIMARY KEY, 
                 product_bar_code text, 
                 product_name text NOT NULL, 
                 product_cost_price real NOT NULL,
                 product_selling_price real NOT NULL,
                 product_quantity INTEGER NOT NULL
                );''')
        mycursor.execute(quary)
        mydb.close()
    def companyDetailsTable(self):
        """This function is use to create the company details table
        and it is called in the init method
        """
        mydb = sqlite3.connect('BERMS.db')
        mycursor = mydb.cursor()
        quary = ('''CREATE TABLE IF NOT EXISTS company(
                 company_id INTEGER PRIMARY KEY, 
                 company_name text,
                 company_tell text,
                 company_location text);''')
        mycursor.execute(quary)
        mydb.commit()
        mydb =self.mydb
        company = 'insert into company (company_name,company_tell,company_location) values("Enter Company Name","9999999","Enter Company Location")'
        mycursor.execute(company)
        mydb.commit()
        mydb.close()
    def salesTable(self):
        """This function is use to create the sales table
        and it is called in the init method
        """
        
        mydb = sqlite3.connect('BERMS.db')
        mycursor = mydb.cursor()
        quary = ('''CREATE TABLE IF NOT EXISTS sales(
                 sales_id INTEGER PRIMARY KEY, 
                 product_name text NOT NULL, 
                 quantity_sold INTEGER NOT NULL,
                 profit_made REAL NOT NULL,
                 date TEXT NOT NULL,
                 month TEXT NOT NULL
                );''')
        mycursor.execute(quary)
        mydb.close()
    def deletingFoldersDates(self):
        """This function is use to create the date table
        and it is called in the init method
        """
        
        mydb = sqlite3.connect('BERMS.db')
        mycursor = mydb.cursor()
        quary = ('''CREATE TABLE IF NOT EXISTS recordFilesDeletedDays(
                 date_id INTEGER PRIMARY KEY, 
                 date TEXT NOT NULL
                );''')
        mycursor.execute(quary)
        mydb.close()
    def dele(self):
        """This function is use to create the date table
        and it is called in the init method
        """
        
        mydb = sqlite3.connect('BERMS.db')
        mycursor = mydb.cursor()
        quary = ('DELETE from recordFilesDeletedDays where date_id=1;')
        mycursor.execute(quary)
        mydb.commit()
        mydb.close()

CreatSqlite3Database()



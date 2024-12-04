import mysql.connector as mydbConnector
import sqlite3
import pathlib
from configparser import ConfigParser


pathToConfigFile=pathlib.Path(__file__).parent.parent.absolute().joinpath('config.ini')
Config = ConfigParser()
Config.read(pathToConfigFile)
dbinfo = Config['database']
dbname =dbinfo['dbname']
class CreatSqlite3Database:
    def __init__(self):
        self.mydb = sqlite3.connect(dbname)
        self.mydb
        self.usersTable()
        self.productsTable()
        self.companyDetailsTable()
        self.deletingFoldersDates()
        self.logedInUsersTable()
        self.creatingDefautLogedInuser()
        self.salesTable()
        

    def usersTable(self):
        """This function is use to create the users table
        and it is called in the init method
        """
        mydb = sqlite3.connect(dbname)
        mycursor = mydb.cursor()
        quary = ('''CREATE TABLE IF NOT EXISTS users(
                 user_id INTEGER PRIMARY KEY, 
                 name text NOT NULL, 
                 email text, 
                 password text NOT NULL,
                 designation text NOT NULL);''')
        mycursor.execute(quary)
        mydb.close()
    def logedInUsersTable(self):
        """This function is use to create the users table
        and it is called in the init method
        """
        mydb = sqlite3.connect(dbname)
        mycursor = mydb.cursor()
        quary1 = ('''CREATE TABLE IF NOT EXISTS UserLogedIn(
                 luser_id INTEGER PRIMARY KEY, 
                 name text NOT NULL, 
                 id text);''')
        mycursor.execute(quary1)
        mydb.close()

    def productsTable(self):
        """This function is use to create the users table
        and it is called in the init method
        """
        mydb = sqlite3.connect(dbname)
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
        mydb = sqlite3.connect(dbname)
        mycursor = mydb.cursor()
        quary = ('''CREATE TABLE IF NOT EXISTS company(
                 company_id INTEGER PRIMARY KEY, 
                 company_name text,
                 company_tell text,
                 company_location text);''')
        mycursor.execute(quary)
        mydb.commit()
        mydb.close()

        mydb =self.mydb
        cur = mydb.cursor()
        iscompanyempty = 'select company_name from company'
        cur.execute(iscompanyempty)
        names=cur.fetchall()
        length=len([i for i in names[0]])
        mydb.close()
        if length <=0:
            self.creatingDefautCompanyDetails()

       
    def salesTable(self):
        """This function is use to create the sales table
        and it is called in the init method
        """
        
        mydb = sqlite3.connect(dbname)
        mycursor = mydb.cursor()
        quary = ('''CREATE TABLE IF NOT EXISTS sales(
                 sales_id INTEGER PRIMARY KEY, 
                 product_name text NOT NULL, 
                 quantity_sold INTEGER NOT NULL,
                 amount_sold REAL NOT NULL,
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
        
        mydb = sqlite3.connect(dbname)
        mycursor = mydb.cursor()
        quary = ('''CREATE TABLE IF NOT EXISTS recordFilesDeletedDays(
                 date_id INTEGER PRIMARY KEY, 
                 date TEXT NOT NULL
                );''')
        mycursor.execute(quary)
        mydb.close()
    def creatingDefautLogedInuser(self):
        mydb = sqlite3.connect(dbname)
        mycursor = mydb.cursor()
        quary = ('''select * from UserLogedIn''')
        mycursor.execute(quary)
        count =mycursor.fetchall()
        if len(count)==0:
            q = "insert into UserLogedIn(name,id) values('default','1')"
            mycursor.execute(q)
            mydb.commit()
            mydb.close()
    def creatingDefautCompanyDetails(self):
        mydb = sqlite3.connect(dbname)
        mycursor = mydb.cursor()
        company = 'insert into company (company_name,company_tell,company_location) values("Enter Company Name","9999999","Enter Company Location")'
        mycursor.execute(company)
        mydb.commit()
        mydb.close()
        
        
    

CreatSqlite3Database()



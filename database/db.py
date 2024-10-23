import mysql.connector as mydbConnector


class CreateDb:
    """this class is use to create the database aand all the 
    and all the tables of the system.
    """
    # the database connection variables
    user = 'root'
    localhost= 'localhost'
    password = '@#mysql@#'
    database="BE_RETAIL_MANAGEMENT_DATABASE"

    def __init__(self):
        self.productsTable()
        self.categoriesTable()
        self.isDatabaseAreadyCreated = self.isDatabasePresent()
        if self.isDatabaseAreadyCreated == "dataBaseIsPresent":
            pass
        else:
            # create database
            self.createDatabase()
            # create the user table
            self.usersTable()
            # creating products table
            self.productsTable()

    # database connectivity
    def dbConnection(self):
        '''this is used to check if there is connection to the database or not
        it returns
        1. mydb => database connection object
        2. DbConnectionPresent => content to determine connection
        '''
        try:
            mydb = mydbConnector.connect(user=self.user, password=self.password,
                                    host=self.localhost,
                                    database=self.database
                                    )
            return [mydb,"DbConnectionPresent"]
        except:
            return "DbConnectionUpsent"

    # checking to see if the database is already present or not
    def isDatabasePresent(self):
        '''this function is use to check if there is a database or not'''
        mydb = self.dbConnection()
        # print(mydb[0])
        if mydb[1] =="DbConnectionPresent":
            return "dataBaseIsPresent"
        else:
            return "dataBaseIsNotPresent"

    # creating user database t
    def createDatabase(self):
        '''this function is use to create the databae'''
        try:
            mydb = mydbConnector.connect(user=self.user, password=self.password,
                                host=self.localhost,
                                )
            mycursor = mydb.cursor()
            mycursor.execute(f"CREATE DATABASE {self.database};")
        except Exception as e:
            print(e)
        finally:
            mydb.close()

    # creating the users table
    def usersTable(self):
        """This function is use to create the users table
        and it is called in the init method
        """
        connection =self.dbConnection()
        mydb =connection[0]
        mycursor = mydb.cursor()
        quary = ('''CREATE TABLE IF NOT EXISTS users(
                 user_id INT AUTO_INCREMENT PRIMARY KEY, 
                 name VARCHAR (200) NOT NULL, 
                 email VARCHAR (200), 
                 password VARCHAR (200) NOT NULL,
                 designation VARCHAR (200) NOT NULL);''')
        mycursor.execute(quary)
        mydb.close()
    # creating the products table
    def productsTable(self):
        """This function is use to create the users table
        and it is called in the init method
        """
        connection =self.dbConnection()
        mydb =connection[0]
        mycursor = mydb.cursor()
        quary = ('''CREATE TABLE IF NOT EXISTS products(
                 product_id INT AUTO_INCREMENT PRIMARY KEY, 
                 product_bar_code VARCHAR (200) NOT NULL, 
                 product_name VARCHAR (200) NOT NULL, 
                 product_cost_price FLOAT NOT NULL,
                 product_selling_price FLOAT NOT NULL,
                 product_quantity INT NOT NULL,
                 product_category VARCHAR (200));''')
        mycursor.execute(quary)
        mydb.close()

    # creating the categories table
    def categoriesTable(self):
        """This function is use to create the categories table
        and it is called in the init method
        """
        connection =self.dbConnection()
        mydb =connection[0]
        mycursor = mydb.cursor()
        quary = ('''CREATE TABLE IF NOT EXISTS categories(
                 cat_id INT AUTO_INCREMENT PRIMARY KEY, 
                 category_name VARCHAR (200));''')
        mycursor.execute(quary)
        mydb.close()

CreateDb()
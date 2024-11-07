from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ObjectProperty
from kivy.uix.recycleview import RecycleView
import mysql.connector as DbConnector
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button



class AdminScreenManager(ScreenManager):
    pass
class HomeScreen(Screen):
    pass
class AnalysisScreen(Screen):
    pass
class ProductsScreen(Screen):
    pass
class UsersScreen(Screen):
    pass
class ProductRecycleView(RecycleView):
    pass
class UserRecycleView(RecycleView):
    pass
class DateLableButton(Button):
    root_widget = ObjectProperty()

    def on_release(self, **kwargs):
        super().on_release(**kwargs)
        self.root_widget.btn_callback(self)
class DateRecycleView(RecycleView):
    def __init__(self, **kwargs): 
        super().__init__(**kwargs)
        data =self.getAllTheSalesDate()
        self.data = [{'text': str(buttonText), 'root_widget': self} for buttonText in data]

    def btn_callback(self, btn):
        reportData = self.parent.parent.children[0].children[0]
        reportTitle = self.parent.parent.children[0].children[2]
        profit =self.parent.parent.parent.children[0].children[0]

        # the title of each month or day
        reportTitle.text=f"[u]{btn.text} Report[/u]"

        # the data for that day of the month
        buttonText=btn.text
        dayData=self.getAllTheSalesByDate(buttonText)[0]
        totalProfit=self.getAllTheSalesByDate(buttonText)[1]

        # data for the text area
        reportData.data=dayData
        profit.text=str(totalProfit)

    def getAllTheSalesDate(self):
        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"

        '''this function is used to update a categories give its id,
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                     )
            query = "SELECT DISTINCT(date) FROM sales;"
            cursor = mydb.cursor()
            cursor.execute(query)
            dates=cursor.fetchall()
            listOfDates=[]
            for date in dates:
                listOfDates.append(str(date[0]))
            mydb.close()
            return listOfDates
        except Exception as e:
            print(e)
            mgs='The is an issue trying to connect to the database to perform delete operation'
            return
    
    def getAllTheSalesByDate(self,date):
        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                     )
                
            query = f"SELECT DISTINCT(product_name) FROM sales WHERE date='{date}';"
            cursor = mydb.cursor()
            cursor.execute(query)
            names = cursor.fetchall()
            soldProducts=[]
            totalProfit=0.00
            for n in names:
                query2 = f"SELECT SUM(quantity_sold),ROUND(SUM(profit_made),2) FROM sales WHERE date='{date}'and product_name='{n[0]}';"
                cursor.execute(query2)
                soldDetails=cursor.fetchall()
                soldProducts.append({'text':str(n[0])})
                soldProducts.append({'text':str(soldDetails[0][0])})
                soldProducts.append({'text':str(soldDetails[0][1])})
                totalProfit += soldDetails[0][1]
            mydb.close()
            return [soldProducts,totalProfit]
        except Exception as e:
            print(e)
            mgs='The is an issue trying to connect to the database to perform delete operation'
            return
    
class MonthLableButton(Button):
    root_widget = ObjectProperty()

    def on_release(self, **kwargs):
        super().on_release(**kwargs)
        self.root_widget.btn_callback(self)
class MonthRecycleView(RecycleView):
    def __init__(self, **kwargs): 
        super().__init__(**kwargs)
        data =self.getAllTheSalesMonths()
        self.data = [{'text': str(buttonText), 'root_widget': self} for buttonText in data]

    def btn_callback(self, btn):
        # # print(btn, btn.text)
        monthlyReportData = self.parent.parent.children[0].children[0]
        monthlyReportTitle = self.parent.parent.children[0].children[2]
        monthlyProfit =self.parent.parent.parent.children[0].children[0]

        # the title of each month
        monthlyReportTitle.text=f"[u]{btn.text} Report[/u]"

        # the data for that month
        buttonText=btn.text
        monthData=self.getAllTheSalesByMonth(buttonText)[0]
        monthTotalProfit=self.getAllTheSalesByMonth(buttonText)[1]
        
        # data for the text area
        monthlyReportData.data=monthData
        monthlyProfit.text=str(monthTotalProfit)

    def getAllTheSalesMonths(self):
        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"

        '''this function is used to update a categories give its id,
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                     )
            query = "SELECT DISTINCT(month) FROM sales;"
            cursor = mydb.cursor()
            cursor.execute(query)
            months=cursor.fetchall()
            listOfMonths=[]
            for date in months:
                listOfMonths.append(str(date[0]))
            mydb.close()
            return listOfMonths
        except Exception as e:
            print(e)
            mgs='The is an issue trying to connect to the database to perform delete operation'
            return
    
    def getAllTheSalesByMonth(self,month):
        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                     )
                
            query = f"SELECT DISTINCT(product_name) FROM sales WHERE month='{month}';"
            cursor = mydb.cursor()
            cursor.execute(query)
            names = cursor.fetchall()
            monthlysoldProducts=[]
            totalMonthlyProfit=0.00
           
            for n in names:
                query3 = f"SELECT SUM(quantity_sold),ROUND(SUM(profit_made),2) FROM sales WHERE month='{month}'and product_name='{n[0]}';"
                cursor.execute(query3)
                soldDetails=cursor.fetchall()
                monthlysoldProducts.append({'text':str(n[0])})
                monthlysoldProducts.append({'text':str(soldDetails[0][0])})
                monthlysoldProducts.append({'text':str(soldDetails[0][1])})
                totalMonthlyProfit += soldDetails[0][1]
                
            mydb.close()
            return [monthlysoldProducts,totalMonthlyProfit]
        
        except Exception as e:
            print(e)
            mgs='The is an issue trying to connect to the database to perform delete operation'
            return
    



class AdministrationPage(BoxLayout):
    def __init__(self, **kwargs):
        super(AdministrationPage,self).__init__(**kwargs)
        
        self.fetchAllProducts()
        self.fetchAllUsers()

        # calling functions
        self.populateCategoryRecycleView()

        # compandetails
        self.details = self.fetchCompanyDetails()
        try:
            self.companyName= self.details[1]
            self.companyTell= self.details[2]
            self.companyLocation=self.details[3]
            self.ids.companyName.text=self.companyName
            self.ids.companyTell.text=self.companyTell
            self.ids.companyLocation.text=self.companyLocation
            self.ids.companyNameId.text=''
            self.ids.companyTellId.text=''
            self.ids.companyLocationId.text=''
        except:
            self.ids.companyName.text='Enter company Name'
            self.ids.companyTell.text="Enter company tell"
            self.ids.companyNameId.text=''
            self.ids.companyTellId.text=''
            
    
    def changeToHomePage(self):
        '''
        change to the home window page function
        '''

        self.ids.adminScreenManagerId.current="homeScreen"

        ''' 
        this makes the page to slide from the 
        left when the daily report button is clicked
        '''
        self.ids.homeScreenId.manager.transition.direction='right'
        
    def changeToProductsPage(self):
        '''
        change to the priducts window page function
        '''

        self.ids.adminScreenManagerId.current="productsScreen"

        ''' 
        this makes the page to slide from the 
        left when the daily report button is clicked
        '''
        self.ids.productsScreenId.manager.transition.direction='left'
        
        
    
    def changeToAnalysisPage(self):
        '''
        change to the analysis window page function
        '''
        self.ids.adminScreenManagerId.current="analysisScreen"

        '''
        this makes the page to slide from the right when the
        daily report button is clicked
        '''
        self.ids.analysisScreenId.manager.transition.direction='left'

    def changeToUsersPage(self):
        '''
        change to the users window page function
        '''
        self.ids.adminScreenManagerId.current="usersScreen"

        '''
        this makes the page to slide from the right when the
        daily report button is clicked
        '''
        self.ids.usersScreenId.manager.transition.direction='left'


    def populateCategoryRecycleView(self):
        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        
        '''this function is used to fetch all the categories from the database and 
        insert them into the categorie  window,
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                        )
            
            selectAllCategories = "SELECT * from categories"
            cursor = mydb.cursor()
            cursor.execute(selectAllCategories)
            listOfAllCategories = cursor.fetchall()

            self.ids.categorylistId.data =[{'text':str(f"{x[0] }  {x[1] } ")} for x in listOfAllCategories]
            
        except:
            pass

       
            
    def fetchCompanyDetails(self):
        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                     )
            query = "select * from company;"
            cursor = mydb.cursor()
            cursor.execute(query)
            details = cursor.fetchone()
            mydb.close()
            return details #(1,name,tell)
        except Exception as e:
            pass

    def changeCompanyName(self):
        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                     )
            query = f"update company SET company_name='{self.ids.companyNameId.text}' where company_id=1;"

            cursor = mydb.cursor()
            cursor.execute(query)
            mydb.commit()
            mydb.close()
            # compandetails
            self.details = self.fetchCompanyDetails()
            try:
                self.companyName= self.details[1]
                self.companyTell= self.details[2]
                self.companyLocation= self.details[3]
                self.ids.companyName.text=self.companyName
                self.ids.companyTell.text=self.companyTell
                self.ids.companyLocation.text=self.companyLocation
                self.ids.companyNameId.text=''
                self.ids.companyTellId.text=''
                self.ids.companyLocationId.text=''
            except:
                self.ids.companyName.text='Enter company Name'
                self.ids.companyTell.text="Enter company tell"
                self.ids.companyLocation.text="Enter company location"
                self.ids.companyNameId.text=''
                self.ids.companyTellId.text=''
                self.ids.companyLocationId.text=''

        except:
            pass

    def changeCompanyTell(self):
        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                     )
            query = f"update company SET company_tell='{self.ids.companyTellId.text}' where company_id=1;"

            cursor = mydb.cursor()
            cursor.execute(query)
            mydb.commit()
            mydb.close()
            # compandetails
            self.details = self.fetchCompanyDetails()
            try:
                self.companyName= self.details[1]
                self.companyTell= self.details[2]
                self.companyLocation= self.details[3]

                self.ids.companyName.text=self.companyName
                self.ids.companyTell.text=self.companyTell
                self.ids.companyLocation.text=self.companyLocation

                self.ids.companyNameId.text=''
                self.ids.companyTellId.text=''
                self.ids.companyLocationId.text=''

            except:
                self.ids.companyName.text='Enter company Name'
                self.ids.companyTell.text="Enter company tell"
                self.ids.companyLocation.text='Enter company location'

                self.ids.companyNameId.text=''
                self.ids.companyTellId.text=''
                self.ids.companyLocationId.text=''


        except:
            pass
    def changeCompanyLocation(self):
        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                     )
            query = f"update company SET company_location='{self.ids.companyLocationId.text}' where company_id=1;"

            cursor = mydb.cursor()
            cursor.execute(query)
            mydb.commit()
            mydb.close()
            # compandetails
            self.details = self.fetchCompanyDetails()
            try:
                self.companyName= self.details[1]
                self.companyTell= self.details[2]
                self.companyLocation = self.details[3]

                self.ids.companyName.text=self.companyName
                self.ids.companyTell.text=self.companyTell
                self.ids.companyLocation.text=self.companyLocation

                self.ids.companyNameId.text=''
                self.ids.companyTellId.text=''
                self.ids.companyLocationId.text=''
            except:
                self.ids.companyName.text='Enter company Name'
                self.ids.companyTell.text="Enter company tell"
                self.ids.companyLocation.text="Enter company location"
                self.ids.companyNameId.text=''
                self.ids.companyTellId.text=''
                self.ids.companyLocationId.text=''


        except:
            pass
    # populating the products
    def fetchAllProducts(self):
        self.ids.productToSearchId.text=''
        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                     )
            query = "SELECT * FROM products;"

            cursor = mydb.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            # (1, '2345', 'tomatoe', 5.0, 6.0, 56, 'vegetables')
            listData=[]
            for result in results:
                listData.append({'text':str(result[0])})
                listData.append({'text':str(result[1])})
                listData.append({'text':str(result[2])})
                listData.append({'text':str(result[3])})
                listData.append({'text':str(result[4])})
                listData.append({'text':str(result[5])})

                self.ids.productListId.refresh_from_data()
                self.ids.productListId.data = listData
            mydb.close()
        except:
            pass

    def addProduct(self):
        # clearing all the error messages
        self.ids.productNameEmptyErrorMessageId.text=''
        self.ids.productQuantityEmptyErrorMessageId.text=''
        self.ids.productCPriceEmptyErrorMessageId.text=''
        self.ids.productSPriceEmptyErrorMessageId.text=''
        self.ids.productIdEmptyErrorMessageId.text=''



        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                     )
            # getting the data
            try:

                pcode = (self.ids.productCodeId.text).strip()
                pname = (self.ids.productNameId.text).strip()
                pquantity = (self.ids.productQuantityId.text).strip()
                pcostprice = (self.ids.productCPriceId.text).strip()
                psellingprice = (self.ids.productSPriceId.text).strip()
                # making sure that the id box is empty when adding product
                pId= (self.ids.productToDeleteNameId.text).strip()

                if pId!='':
                    self.ids.productIdEmptyErrorMessageId.text='Please product "id" must be empty when adding'
                    return
                

                'Making sure the name field is not empty'
                if pname=="":
                    self.ids.productNameEmptyErrorMessageId.text='Please provide product name'
                    return

                'Making sure the quantity field is not empty or not integer'
                try:
                    int(pquantity)
                except:
                    self.ids.productQuantityEmptyErrorMessageId.text='Product quantity should numbers'
                    return

                'Making sure the Cost price field is not empty and is an integer or float'
                try:
                    pcostprice=float(pcostprice)
                    
                except:
                    self.ids.productCPriceEmptyErrorMessageId.text='Enter cost price(number)'
                    return
                
                'Making sure the Selling price field is not empty and is an integer or float'
                try:
                    psellingprice=float(psellingprice)
                    
                except:
                    self.ids.productSPriceEmptyErrorMessageId.text='Enter selling price(number)'
                    return


            except Exception as e:
                self.ids.productsEntryErrorsId.text='and error occured trying to add product'
                
            else:
                query = "insert into products values (product_id,%s,%s,%s,%s,%s);"
                pcostprice=float(pcostprice)
                psellingprice=float(psellingprice)
                pquantity=int(pquantity)

                cursor = mydb.cursor()
                cursor.execute(query,(pcode,pname,pcostprice,psellingprice,pquantity))
                mydb.commit()
                mydb.close()
                self.ids.productListId.refresh_from_data()
                self.fetchAllProducts()
                self.clearProductFields()
                
            
        except:
            self.ids.productsEntryErrorsId.text='The is an issue trying to connect to the database'
            
    def clearProductFields(self):
        self.ids.productCodeId.text=''
        self.ids.productNameId.text=''
        self.ids.productQuantityId.text=''
        self.ids.productCPriceId.text=''
        self.ids.productSPriceId.text=''
        #clearing all error messages
        self.ids.productIdEmptyErrorMessageId.text=''
        self.ids.productsEntryErrorsId.text=''
        self.ids.productNameEmptyErrorMessageId.text=''
        self.ids.productQuantityEmptyErrorMessageId.text=''
        self.ids.productCPriceEmptyErrorMessageId.text=''
        self.ids.productSPriceEmptyErrorMessageId.text=''
            
    

    def searchProductsByIdButton(self,*args, **kwargs):
        self.ids.productIdEmptyErrorMessageId.text=''
        self.clearProductFields()

        productId= (self.ids.productToDeleteNameId.text).strip()

        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                     )
            try:
                productId = int(productId)
                query = "SELECT * FROM products where product_id=%s;"

                cursor = mydb.cursor()
                cursor.execute(query,(productId,))
                result= cursor.fetchone()
                self.ids.productCodeId.text=str(result[1])
                self.ids.productNameId.text=str(result[2])
                self.ids.productQuantityId.text=str(result[5])
                self.ids.productCPriceId.text=str(result[3])
                self.ids.productSPriceId.text=str(result[4])
            except:
                self.ids.productIdEmptyErrorMessageId.text=f'No product with id ="{productId}"'

        except:
            self.ids.productsEntryErrorsId.text='The is an issue trying to connect to the database in order to search the product'

       
    def deleteProduct(self):
        self.ids.productIdEmptyErrorMessageId.text=''
        self.ids.productsEntryErrorsId.text=''

        productToDeleteId= (self.ids.productToDeleteNameId.text).strip()

        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                     )
            try:
                productToDeleteId= int(productToDeleteId)
                
                query = "DELETE FROM products where product_id=%s;"

                cursor = mydb.cursor()
                cursor.execute(query,(productToDeleteId,))
                mydb.commit()
                mydb.close()
                self.ids.productListId.refresh_from_data()
                self.fetchAllProducts()
                self.clearProductFields()
                self.ids.productToDeleteNameId.text=''

                
            except Exception as e:
                self.ids.productIdEmptyErrorMessageId.text='Please product id must be number in order to delete'
             
        except Exception as e:
            self.ids.productsEntryErrorsId.text='The is an issue trying to connect to the database to perform delete operation'
        

    def updateProduct(self):
        self.ids.productIdEmptyErrorMessageId.text=''
        self.ids.productsEntryErrorsId.text=''
        self.ids.productNameEmptyErrorMessageId.text=''
        self.ids.productQuantityEmptyErrorMessageId.text=''
        self.ids.productCPriceEmptyErrorMessageId.text=''
        self.ids.productSPriceEmptyErrorMessageId.text=''



        productToUpdateId= (self.ids.productToDeleteNameId.text).strip()

        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                     )
            try:
                productToUpdateId= int(productToUpdateId)
                # search product updated information
                pcode = (self.ids.productCodeId.text).strip()
                pname = (self.ids.productNameId.text).strip()
                pquantity = (self.ids.productQuantityId.text).strip()
                pcostprice = (self.ids.productCPriceId.text).strip()
                psellingprice = (self.ids.productSPriceId.text).strip()
                pId= (self.ids.productToDeleteNameId.text).strip()

                if pId=='':
                    self.ids.productIdEmptyErrorMessageId.text='Please provide product "id" to update'
                    return
                
                'Making sure the name field is not empty'
                if pname=="":
                    self.ids.productNameEmptyErrorMessageId.text='Please provide product name'
                    return
                
                try:
                    pId= int(pId)
                except:
                    self.ids.productIdEmptyErrorMessageId.text=f'No product with id ="{pId}"'


                'Making sure the quantity field is not empty or not integer'
                try:
                    int(pquantity)
                except:
                    self.ids.productQuantityEmptyErrorMessageId.text='Product quantity should numbers'
                    return

                'Making sure the Cost price field is not empty and is an integer or float'
                try:
                    pcostprice=float(pcostprice)
                    
                except:
                    self.ids.productCPriceEmptyErrorMessageId.text='Enter cost price(number)'
                    return
                
                'Making sure the Selling price field is not empty and is an integer or float'
                try:
                    psellingprice=float(psellingprice)
                except:
                    self.ids.productSPriceEmptyErrorMessageId.text='Enter selling price(number)'
                    return
                
                else:
                    pcostprice=float(pcostprice)
                    psellingprice=float(psellingprice)
                    pquantity=int(pquantity)

                    query = f"""update products SET product_bar_code='{pcode}',product_name='{pname}',product_cost_price={pcostprice},product_selling_price={psellingprice},product_quantity={pquantity} where product_id={pId};"""
                    cursor = mydb.cursor()
                    cursor.execute(query)
                    mydb.commit()
                    mydb.close()
                    self.ids.productListId.refresh_from_data()
                    self.fetchAllProducts()
                    self.clearProductFields()
                    self.ids.productToDeleteNameId.text=''
            except Exception as e:
                self.ids.productIdEmptyErrorMessageId.text='Wrong product id'
        except Exception as e:
            self.ids.productsEntryErrorsId.text='The is an issue trying to connect to the database to perform Update operation'
        
    def searchProductsByName(self,*args, **kwargs):
        self.ids.noProductMessage.text=""


        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                     )
            searchedproduct= (self.ids.productToSearchId.text).strip()
            
            if searchedproduct=='':
                self.ids.noProductMessage.text="Enter product Name to search"
                return
            else:
                productToSearchName=str(searchedproduct+'%')
                selectAllProducts = f" SELECT * FROM products WHERE product_name LIKE '{productToSearchName}';"
                cursor = mydb.cursor()
                cursor.execute(selectAllProducts)
                listOfAllProducts = cursor.fetchall()
                listData=[]
                for result in listOfAllProducts:
                    listData.append({'text':str(result[0])})
                    listData.append({'text':str(result[1])})
                    listData.append({'text':str(result[2])})
                    listData.append({'text':str(result[3])})
                    listData.append({'text':str(result[4])})
                    listData.append({'text':str(result[5])})
                # give and a message if the id no product
                try:
                    listData[0]
                except:
                    self.ids.noProductMessage.text=f'No product with the name {searchedproduct}'
                    return

                self.ids.productListId.refresh_from_data()
                self.ids.productListId.data = listData
                self.ids.productToSearchId.text=''
                mydb.close()

        except:
            self.ids.noProductMessage.text='The is an issue trying to connect to the database to perform the product search operation'
            


    # =================================THE USERS SECTION=========================
    # populating the products
    def fetchAllUsers(self):
        self.ids.userToSearchId.text=''
        self.ids.noUserMessage.text=""
        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                     )
            query = "SELECT * FROM users;"

            cursor = mydb.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            userslistData=[]
            for result in results:
                userslistData.append({'text':str(result[0])})
                userslistData.append({'text':str(result[1])})
                userslistData.append({'text':str(result[2])})
                userslistData.append({'text':str(result[3])})
                userslistData.append({'text':str(result[4])})

                self.ids.usersListId.refresh_from_data()
                self.ids.usersListId.data = userslistData
            mydb.close()
        except:
            pass
        
    def searchUsersByName(self,*args, **kwargs):
        self.ids.noUserMessage.text=""
        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                     )
            searcheduser= (self.ids.userToSearchId.text).strip()
            
            if searcheduser=='':
                self.ids.noUserMessage.text="Enter User Name to search"
                return
            else:
                userToSearchName=str(searcheduser+'%')
                selectAllUsers = f" SELECT * FROM users WHERE name LIKE '{userToSearchName}';"
                cursor = mydb.cursor()
                cursor.execute(selectAllUsers)
                listOfAllUsers = cursor.fetchall()
                userlistData=[]
                for result in listOfAllUsers:
                    userlistData.append({'text':str(result[0])})
                    userlistData.append({'text':str(result[1])})
                    userlistData.append({'text':str(result[2])})
                    userlistData.append({'text':str(result[3])})
                    userlistData.append({'text':str(result[4])})
                # give and a message if the id no product
                try:
                    userlistData[0]
                except:
                    self.ids.noUserMessage.text=f'No user with the name {searcheduser}'
                    return

                self.ids.usersListId.refresh_from_data()
                self.ids.usersListId.data = userlistData
                self.ids.userToSearchId.text=''
                mydb.close()
        except Exception as e:
            self.ids.noUserMessage.text='The is an issue trying to connect to the database to perform the user search operation'
            return

    def clearUserFields(self):
        self.ids.userNameId.text=''
        self.ids.userEmailId.text=''
        self.ids.userPasswordId.text=''
        self.ids.userDesignationId.text=''
        #clearing all error messages
        self.ids.userIdEmptyErrorMessageId.text=''
        self.ids.userIdEmptyErrorMessageId.text=''
        self.ids.userNameEmptyErrorMessageId.text=''
        self.ids.userEmailEmptyErrorMessageId.text=''
        self.ids.userPasswordEmptyErrorMessageId.text=''
        self.ids.userDesignationEmptyErrorMessageId.text=''


    def addUser(self):
        # clearing all the error messages
        self.ids.userIdEmptyErrorMessageId.text=''
        self.ids.userIdEmptyErrorMessageId.text=''
        self.ids.userNameEmptyErrorMessageId.text=''
        self.ids.userEmailEmptyErrorMessageId.text=''
        self.ids.userPasswordEmptyErrorMessageId.text=''
        self.ids.userDesignationEmptyErrorMessageId.text=''
        
        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                     )
            # getting the data
            try:
                userId= (self.ids.userToDeleteOrUpdateId.text).strip()
                username = (self.ids.userNameId.text).strip()
                useremail = (self.ids.userEmailId.text).strip()
                userpassword = (self.ids.userPasswordId.text).strip()
                userdesignation = ((self.ids.userDesignationId.text).strip()).lower()

                # making sure that the id box is empty when adding product

                if userId!='':
                    self.ids.userIdEmptyErrorMessageId.text='Please user "id" must be empty when adding'
                    return
                

                'Making sure the name field is not empty'
                if  username=="":
                    self.ids.userNameEmptyErrorMessageId.text='Please provide user name'
                    return

                'Making sure the email field is not empty or not integer'
                if useremail=='':
                    self.ids.userEmailEmptyErrorMessageId.text='user email is empty'
                    return

                'Making sure the user password field is not empty'
                if userpassword=='':
                    self.ids.userPasswordEmptyErrorMessageId.text='Enter password'
                    return
                
                'Making sure the designation field is not empty '
                if (userdesignation==''):
                    self.ids.userDesignationEmptyErrorMessageId.text='Enter designation (admin or operator)'
                    return
                if str(userdesignation)!="admin":
                    if str(userdesignation)!="operator":
                        self.ids.userDesignationEmptyErrorMessageId.text='Enter designation (admin or operator)'
                        return
                    else:
                        pass


            except Exception as e:
                self.ids.usersEntryErrorsId.text='and error occured trying to add user'
                return
                
            else:
                query = "insert into users values (user_id,%s,%s,%s,%s);"
                cursor = mydb.cursor()
                cursor.execute(query,(username,useremail,userpassword,userdesignation))
                mydb.commit()
                mydb.close()
                self.ids.usersListId.refresh_from_data()
                self.fetchAllUsers()
                self.clearUserFields()
        except Exception as e:
            self.ids.usersEntryErrorsId.text='The is an issue trying to connect to the database to add the user'
            return
            
    def updateUser(self):
        # clearing all the error messages
        self.ids.userIdEmptyErrorMessageId.text=''
        self.ids.userIdEmptyErrorMessageId.text=''
        self.ids.userNameEmptyErrorMessageId.text=''
        self.ids.userEmailEmptyErrorMessageId.text=''
        self.ids.userPasswordEmptyErrorMessageId.text=''
        self.ids.userDesignationEmptyErrorMessageId.text=''

        userToUpdateId_= (self.ids.userToDeleteOrUpdateId.text).strip()

        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                     )
            # getting the data
            try:
                username = (self.ids.userNameId.text).strip()
                useremail = (self.ids.userEmailId.text).strip()
                userpassword = (self.ids.userPasswordId.text).strip()
                userdesignation = ((self.ids.userDesignationId.text).strip()).lower()

                # making sure that the id box is not empty when updating product

                if userToUpdateId_=='':
                    self.ids.userIdEmptyErrorMessageId.text='Please user "id" must not be empty'
                    return
                
                try:
                    userToUpdateId_= int(userToUpdateId_)
                except:
                    self.ids.userIdEmptyErrorMessageId.text=f'No user with id ="{userToUpdateId_}"'
                    return

                'Making sure the name field is not empty'
                if  username=="":
                    self.ids.userNameEmptyErrorMessageId.text='Please provide user name'
                    return

                'Making sure the email field is not empty or not integer'
                if useremail=='':
                    self.ids.userEmailEmptyErrorMessageId.text='user email is empty'
                    return

                'Making sure the user password field is not empty'
                if userpassword=='':
                    self.ids.userPasswordEmptyErrorMessageId.text='Enter password'
                    return
                
                'Making sure the designation field is not empty '
                if (userdesignation==''):
                    self.ids.userDesignationEmptyErrorMessageId.text='Enter designation (admin or operator)'
                    return
                if str(userdesignation)!="admin":
                    if str(userdesignation)!="operator":
                        self.ids.userDesignationEmptyErrorMessageId.text='Enter designation (admin or operator)'
                        return
                    else:
                        pass
            except Exception as e:
                self.ids.userIdEmptyErrorMessageId.text='Wrong user id'
                return
            else:
                query = f"""update users SET name='{username}',email='{useremail}',password='{userpassword}',designation='{userdesignation}' where user_id={userToUpdateId_};"""

                cursor = mydb.cursor()
                cursor.execute(query)
                mydb.commit()
                mydb.close()
                self.ids.usersListId.refresh_from_data()
                self.fetchAllUsers()
                self.clearUserFields()
                self.ids.userToDeleteOrUpdateId.text=''
        except Exception as e:
            self.ids.usersEntryErrorsId.text='The is an issue trying to connect to the database to update the user'
            return
            
    def searchUserByIdButton(self,*args, **kwargs):
        self.ids.userIdEmptyErrorMessageId.text=''
        self.clearUserFields()
        UserId= (self.ids.userToDeleteOrUpdateId.text).strip()

        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                     )
            try:
                UserId = int(UserId)
                query = "SELECT * FROM users where user_id=%s;"
                cursor = mydb.cursor()
                cursor.execute(query,(UserId,))
                result= cursor.fetchone()
                
                self.ids.userNameId.text=str(result[1])
                self.ids.userEmailId.text=str(result[2])
                self.ids.userPasswordId.text=str(result[3])
                self.ids.userDesignationId.text=str(result[4])

            except Exception as e:
                self.ids.userIdEmptyErrorMessageId.text=f'No user with id ="{UserId}"'
                return
        except:
            self.ids.usersEntryErrorsId.text='The is an issue trying to connect to the database in order to search the user'
            return
          
    def deleteUser(self):
        self.ids.userIdEmptyErrorMessageId.text=''
        self.ids.usersEntryErrorsId.text=''

        userToDeleteId= (self.ids.userToDeleteOrUpdateId.text).strip()

        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                     )
            try:
                userToDeleteId= int(userToDeleteId)
                
                query = "DELETE FROM users where user_id=%s;"
                cursor = mydb.cursor()
                cursor.execute(query,(userToDeleteId,))
                mydb.commit()
                mydb.close()
                self.ids.usersListId.refresh_from_data()
                self.fetchAllUsers()
                self.clearUserFields()
                self.ids.userToDeleteOrUpdateId.text=''
            except Exception as e:
                self.ids.userIdEmptyErrorMessageId.text='wrong user id '
                return
             
        except Exception as e:
            self.ids.usersEntryErrorsId.text='The is an issue trying to connect to the database to perform delete operation'
            return
        
    
class AdministrationApp(App):
    def build(self):
        return AdministrationPage()
    
if __name__=="__main__":
    AdministrationApp().run()




















# def addCategory(self):
#         user ='root'
#         dbpassword = '@#mysql@#'
#         host ='localhost'
#         database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        
#         '''this function is used to fetch all the categories from the database and 
#         insert them into the categorie  window,
#         '''
#         try:
#             mydb = DbConnector.connect(user=user, password=dbpassword,
#                                         host=host,
#                                         database=database
#                                         )
#             catName = self.ids.categoryTextId.text
#             insertCategories = f"insert into categories values(cat_id,'{catName}');"
#             cursor = mydb.cursor()
#             cursor.execute(insertCategories)
#             mydb.commit()
#             mydb.close()

#             # calling the fetch function
#             self.populateCategoryRecycleView()

#             # resetting the input field to nothing
#             self.ids.categoryTextId.text=''
#             # refreshing the recycle view
#             self.ids.categorylistId.refresh_from_data()

#             print("add function")
#         except Exception as e:
#             print(e)
            
        
    
    
#     def updateCategory(self):
#         self.ids.errorMessagesId.text=''
#         user ='root'
#         dbpassword = '@#mysql@#'
#         host ='localhost'
#         database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        
#         '''this function is used to update a categories give its id,
#         '''
#         try:
#             mydb = DbConnector.connect(user=user, password=dbpassword,
#                                         host=host,
#                                         database=database
#                                      )
#             try:
#                 catId = int(self.ids.productToDeletOrUpdate.text)
                
#                 # checking if the user has enter the new name of not
#                 newCatName=self.ids.categoryTextId.text
#                 if newCatName!="":
#                     try:
#                         updateCat = f"update categories SET category_name='{newCatName}' where cat_id={catId};"
#                         print(updateCat)
#                         cursor = mydb.cursor()
#                         cursor.execute(updateCat)
#                         mydb.commit()
#                         mydb.close()
#                     except:
#                         self.ids.errorMessagesId.text="am having an issue in trying to update your category"

#                     # calling the fetch function
#                     self.populateCategoryRecycleView()

#                     # resetting the input fields to nothing
#                     self.ids.categoryTextId.text=''
#                     self.ids.productToDeletOrUpdate.text=''
#                     # refreshing the recycle view
#                     self.ids.categorylistId.refresh_from_data()
#                 else:
#                     self.ids.errorMessagesId.text="Please provide the new category name you want to update with"

#             except Exception as e:
#                 self.ids.errorMessagesId.text="The id must not be empty and it should be a number in order to update"

                
#         except Exception as e:
#             self.ids.errorMessagesId.text="An issue occured in connecting the database"
            
#     def deleteCategory(self):
#         self.ids.errorMessagesId.text=''
#         user ='root'
#         dbpassword = '@#mysql@#'
#         host ='localhost'
#         database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        
#         '''this function is used to update a categories give its id,
#         '''
#         try:
#             mydb = DbConnector.connect(user=user, password=dbpassword,
#                                         host=host,
#                                         database=database
#                                      )
#             try:
#                 catId = int(self.ids.productToDeletOrUpdate.text)
                
#                 try:
#                     deleteCat = f"delete from categories where cat_id={catId};"
#                     cursor = mydb.cursor()
#                     cursor.execute(deleteCat)
#                     mydb.commit()
#                     mydb.close()
#                 except:
#                     self.ids.errorMessagesId.text="am having an issue in trying to delete your category"

#                 # calling the fetch function
#                 self.populateCategoryRecycleView()

#                 # resetting the input fields to nothing
#                 self.ids.categoryTextId.text=''
#                 self.ids.productToDeletOrUpdate.text=''
#                 # refreshing the recycle view
#                 self.ids.categorylistId.refresh_from_data()
                
#             except Exception as e:
#                 self.ids.errorMessagesId.text="The id must not be empty and it should be a number in order to delete"

                
#         except Exception as e:
#             self.ids.errorMessagesId.text="An issue occured in connecting the database"
         
# def categoryDropDownFunction(self):
#         # Creating a category dropdown
#         categoryDropDown= DropDown()
#         categories=self.fetchAllCategories()
        
#         for cat in categories:
#             categoriesButton= Button(text=f'{cat[0]}',size_hint_y=None, height=30,color=(0,0,0,1))
#             categoriesButton.bind(on_release=lambda categoriesButton: categoryDropDown.select(categoriesButton.text))
#             categoryDropDown.add_widget(categoriesButton)
#         categoryDropDown.open

    
#     def fetchAllCategories(self):
#         user ='root'
#         dbpassword = '@#mysql@#'
#         host ='localhost'
#         database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        
#         '''this function is used to update a categories give its id,
#         '''
#         try:
#             mydb = DbConnector.connect(user=user, password=dbpassword,
#                                         host=host,
#                                         database=database
#                                      )
#             query = "select category_name from categories;"
#             cursor = mydb.cursor()
#             cursor.execute(query)
#             listOfCategories = cursor.fetchall()
#             mydb.close()
#             return listOfCategories #(1,name,tell)
#         except Exception as e:
#             self.ids.productsEntryErrorsId.text='The is an issue trying to connect to the database'

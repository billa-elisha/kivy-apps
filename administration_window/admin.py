from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ObjectProperty
from kivy.uix.recycleview import RecycleView
import sqlite3
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from datetime import datetime
from inspect import currentframe, getframeinfo
from kivy.lang import Builder
import os
import win32api
import time
import shutil
import pathlib
from configparser import ConfigParser

pathToConfigFileToConnectDb=pathlib.Path(__file__).parent.parent.absolute().joinpath('config.ini')
Config = ConfigParser()
Config.read(pathToConfigFileToConnectDb)
dbinfo = Config['database']
dbname =dbinfo['dbname']



path = os.getcwd()
Builder.load_file(path +'/administration_window/administration1.kv')
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
        # database configuration
        self.databaseName=dbname
        
        data =self.getAllTheSalesDate()
        self.data = [{'text': str(buttonText), 'root_widget': self} for buttonText in data]

        

    def loggingMessage(self,appname,e):
        date = datetime.now()
        ms = (f'''[{appname} APP]: {date} 
{e}
\n''')
        f = open(f'{appname}App-loggmessages.txt','a')
        f.write(ms)

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
        '''this function is used to update a categories give its id,
        '''
        try:
            
            mydb=sqlite3.connect(dbname)
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
            self.loggingMessage('administration_window',e)
            return
    
    def getAllTheSalesByDate(self,date):
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb =sqlite3.connect(self.databaseName)
                
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
            self.loggingMessage('administration_window',e)
            return
    
class MonthLableButton(Button):
    root_widget = ObjectProperty()

    def on_release(self, **kwargs):
        super().on_release(**kwargs)
        self.root_widget.btn_callback(self)
class MonthRecycleView(RecycleView):
    def __init__(self, **kwargs): 
        super().__init__(**kwargs)
        self.databaseName=dbname
        

        data =self.getAllTheSalesMonths()
        self.data = [{'text': str(buttonText), 'root_widget': self} for buttonText in data]
        

    def loggingMessage(self,appname,e):
        date = datetime.now()
        ms = (f'''[{appname} APP]: {date} 
{e}
\n''')
        f = open(f'{appname}App-loggmessages.txt','a')
        f.write(ms)

    def btn_callback(self, btn):
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
        '''this function is used to update a categories give its id,
        '''
        try:
           
            mydb=sqlite3.connect(self.databaseName)
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
            self.loggingMessage('administration_window',e)
            return
    
    def getAllTheSalesByMonth(self,month):
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb=sqlite3.connect(self.databaseName)
                
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
            self.loggingMessage('administration_window',e)
            return
    



class AdministrationPage(BoxLayout):
    
    def __init__(self, **kwargs):
        super(AdministrationPage,self).__init__(**kwargs)
        self.databaseName=dbname
        self.deletingAllSaveFilesEveryMonth()
        self.fetchAllProducts()
        self.fetchAllUsers()
        self.summaryOfProducts_Employees()
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
    

    # =============popup section============
    def popUpNotification(self,instance):
        buttonClicked = (instance.text).lower()
        self.mainlayout =BoxLayout(orientation='vertical')
        self.popup= Popup(
            title='Test popup',
            content=self.mainlayout,
            size_hint=(None, None), size=(300, 200),
            auto_dismiss=False
        )
        self.mainlayout.add_widget(Label(text=f'Do you really you want to {buttonClicked}'))

        self.buttonLayout=BoxLayout(
            size_hint_y=None,
            height='40dp',
            spacing='50dp')
        
        okButton = Button(text='Yes')
        self.buttonLayout.add_widget(okButton)
        # the how page site
        if buttonClicked =="change name":
            okButton.bind(on_press=self.changeCompanyName)
        if buttonClicked =="change tell":
            okButton.bind(on_press=self.changeCompanyTell)
        if buttonClicked =="change location":
            okButton.bind(on_press=self.changeCompanyLocation)

        # the productl page
        if buttonClicked =="clear product":
            okButton.bind(on_press=self.clearProductFields)
        if buttonClicked =="add product":
            okButton.bind(on_press=self.addProduct)
        if buttonClicked =="delete product":
            okButton.bind(on_press=self.deleteProduct)
        if buttonClicked =="update product":
            okButton.bind(on_press=self.updateProduct)
        # the user page
        if buttonClicked =="clear fields":
            okButton.bind(on_press=self.clearUserFields)
        if buttonClicked =="add user":
            okButton.bind(on_press=self.addUser)
        if buttonClicked =="delete user":
            okButton.bind(on_press=self.deleteUser)
        if buttonClicked =="update user":
            okButton.bind(on_press=self.updateUser)
        # the print repor section
        if buttonClicked =="print day report":
            okButton.bind(on_press=self.printsDailyReport)
        if buttonClicked =="print month report":
            okButton.bind(on_press=self.printsMontlyReport)
        

        else:
            pass
        
        self.concelBtn=Button(text='No',on_press=self.popup.dismiss)
        self.buttonLayout.add_widget(self.concelBtn)
        self.mainlayout.add_widget(self.buttonLayout)
        self.popup.open()

# =============popup section end_============

    def loggingMessage(self,appname,e):
        date = datetime.now()
        ms = (f'''[{appname} APP]: {date} 
{e}
\n''')
        f = open(f'{appname}App-loggmessages.txt','a')
        f.write(ms)

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


    

       
            
    def fetchCompanyDetails(self):
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb=sqlite3.connect(self.databaseName)
            query = "select * from company;"
            cursor = mydb.cursor()
            cursor.execute(query)
            details = cursor.fetchone()
            mydb.close()
            return details #(1,name,tell)
        except Exception as e:
            self.loggingMessage('administration_window',e)
            pass

    def changeCompanyName(self,instance):
        self.popup.dismiss()
        '''this function is used to update a categories give its id,
        '''
        try:
           
            mydb=sqlite3.connect(self.databaseName)
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

        except Exception as e:
            self.loggingMessage('administration_window',e)
            pass

    def changeCompanyTell(self,instance):
        self.popup.dismiss()
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb=sqlite3.connect(self.databaseName)
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


        except Exception as e:
            self.loggingMessage('administration_window',e)
            pass

    def changeCompanyLocation(self,instance):
        self.popup.dismiss()
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb=sqlite3.connect(self.databaseName)
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


        except Exception as e:
            self.loggingMessage('administration_window',e)
            pass
    # populating the products
    def fetchAllProducts(self):
        self.ids.productToSearchId.text=''
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb=sqlite3.connect(self.databaseName)
            query = "SELECT * FROM products;"

            cursor = mydb.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            # (1, '2345', 'tomatoe', 5.0, 6.0, 56, 'vegetables')
            listData=[]
            for result in results:
                if int(result[5])<=0:
                    listData.append({'text':str(result[0]),'color':(1,0,0,1)})
                    listData.append({'text':str(result[1]),'color':(1,0,0,1)})
                    listData.append({'text':str(result[2]),'color':(1,0,0,1)})
                    listData.append({'text':str(result[3]),'color':(1,0,0,1)})
                    listData.append({'text':str(result[4]),'color':(1,0,0,1)})
                    listData.append({'text':str(result[5]),'color':(1,0,0,1)})
                elif int(result[5])<5:
                    listData.append({'text':str(result[0]),'color':(0,1,0,1)})
                    listData.append({'text':str(result[1]),'color':(0,1,0,1)})
                    listData.append({'text':str(result[2]),'color':(0,1,0,1)})
                    listData.append({'text':str(result[3]),'color':(0,1,0,1)})
                    listData.append({'text':str(result[4]),'color':(0,1,0,1)})
                    listData.append({'text':str(result[5]),'color':(0,1,0,1)})
                else:
                    listData.append({'text':str(result[0])})
                    listData.append({'text':str(result[1])})
                    listData.append({'text':str(result[2])})
                    listData.append({'text':str(result[3])})
                    listData.append({'text':str(result[4])})
                    listData.append({'text':str(result[5])})

                self.ids.productListId.refresh_from_data()
                self.ids.productListId.data = listData
            mydb.close()
        except Exception as e:
            self.loggingMessage('administration_window',e)
            pass

    def addProduct(self,instance):
        self.popup.dismiss()
        # clearing all the error messages
        self.ids.productNameEmptyErrorMessageId.text=''
        self.ids.productQuantityEmptyErrorMessageId.text=''
        self.ids.productCPriceEmptyErrorMessageId.text=''
        self.ids.productSPriceEmptyErrorMessageId.text=''
        self.ids.productIdEmptyErrorMessageId.text=''

        '''this function is used to update a categories give its id,
        '''
        try:
            mydb=sqlite3.connect(self.databaseName)
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
                except Exception as e:
                    self.loggingMessage('administration_window',e)
                    self.ids.productQuantityEmptyErrorMessageId.text='Product quantity should numbers'
                    return

                'Making sure the Cost price field is not empty and is an integer or float'
                try:
                    pcostprice=float(pcostprice)
                    
                except Exception as e:
                    self.loggingMessage('administration_window',e)
                    self.ids.productCPriceEmptyErrorMessageId.text='Enter cost price(number)'
                    return
                
                'Making sure the Selling price field is not empty and is an integer or float'
                try:
                    psellingprice=float(psellingprice)
                    
                except Exception as e:
                    self.loggingMessage('administration_window',e)
                    self.ids.productSPriceEmptyErrorMessageId.text='Enter selling price(number)'
                    return


            except Exception as e:
                self.loggingMessage('administration_window',e)
                self.ids.productsEntryErrorsId.text='and error occured trying to add product'
                
            else:
                "Making sure product name is unique"
                cursor = mydb.cursor()
                cursor.execute('Select product_name from products;')
                pnamess= cursor.fetchall()
                listOfpNames=[]
                for pn in pnamess:
                    listOfpNames.append(pn[0])
                if pname in  listOfpNames:
                    self.ids.productNameEmptyErrorMessageId.text='Please product name already exist'
                    return
                query = f"insert into products (product_bar_code,product_name,product_cost_price,product_selling_price,product_quantity) values('{pcode}','{pname}',{pcostprice},{psellingprice},{pquantity});"
                pcostprice=float(pcostprice)
                psellingprice=float(psellingprice)
                pquantity=int(pquantity)

                cursor = mydb.cursor()
                cursor.execute(query)
                mydb.commit()
                mydb.close()
                self.ids.productListId.refresh_from_data()
                self.fetchAllProducts()
                # clearing fields
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
                self.summaryOfProducts_Employees()
            
        except Exception as e:
            print(e)
            self.loggingMessage('administration_window',e)
            self.ids.productsEntryErrorsId.text='The is an issue trying to connect to the database'
            
    def clearProductFields(self,instance):
        self.popup.dismiss()
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
        # clearing products
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
        productId= (self.ids.productToDeleteNameId.text).strip()

        '''this function is used to update a categories give its id,
        '''
        try:
            mydb=sqlite3.connect(self.databaseName)
            try:
                productId = int(productId)
                query = f"SELECT * FROM products where product_id={productId};"

                cursor = mydb.cursor()
                cursor.execute(query)
                result= cursor.fetchone()
                self.ids.productCodeId.text=str(result[1])
                self.ids.productNameId.text=str(result[2])
                self.ids.productQuantityId.text=str(result[5])
                self.ids.productCPriceId.text=str(result[3])
                self.ids.productSPriceId.text=str(result[4])
                mydb.close()
            except Exception as e:
                mydb.close()
                self.loggingMessage('administration_window',e)
                self.ids.productIdEmptyErrorMessageId.text=f'No product with id ="{productId}"'

        except Exception as e:
            mydb.close()
            self.loggingMessage('administration_window',e)
            self.ids.productsEntryErrorsId.text='The is an issue trying to connect to the database in order to search the product'

       
    def deleteProduct(self,instance):
        self.popup.dismiss()
        self.ids.productIdEmptyErrorMessageId.text=''
        self.ids.productsEntryErrorsId.text=''

        productToDeleteId= (self.ids.productToDeleteNameId.text).strip()

        '''this function is used to update a categories give its id,
        '''
        try:
            mydb=sqlite3.connect(self.databaseName)
            try:
                productToDeleteId= int(productToDeleteId)
                
                query = f"DELETE FROM products where product_id={productToDeleteId};"

                cursor = mydb.cursor()
                cursor.execute(query)
                mydb.commit()
                mydb.close()
                self.ids.productListId.refresh_from_data()
                self.fetchAllProducts()
                # clearing products fields
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

                self.ids.productToDeleteNameId.text=''
                self.summaryOfProducts_Employees()

                
            except Exception as e:
                print(e)
                self.loggingMessage('administration_window',e)
                self.ids.productIdEmptyErrorMessageId.text='Please product id must be number in order to delete'
             
        except Exception as e:
            self.loggingMessage('administration_window',e)
            self.ids.productsEntryErrorsId.text='The is an issue trying to connect to the database to perform delete operation'
        finally:
            mydb.close()

    def updateProduct(self,instance):
        self.popup.dismiss()
        self.ids.productIdEmptyErrorMessageId.text=''
        self.ids.productsEntryErrorsId.text=''
        self.ids.productNameEmptyErrorMessageId.text=''
        self.ids.productQuantityEmptyErrorMessageId.text=''
        self.ids.productCPriceEmptyErrorMessageId.text=''
        self.ids.productSPriceEmptyErrorMessageId.text=''



        productToUpdateId= (self.ids.productToDeleteNameId.text).strip()

        '''this function is used to update a categories give its id,
        '''
        try:
            mydb=sqlite3.connect(self.databaseName)
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
                except Exception as e:
                    self.loggingMessage('administration_window',e)
                    self.ids.productIdEmptyErrorMessageId.text=f'No product with id ="{pId}"'


                'Making sure the quantity field is not empty or not integer'
                try:
                    int(pquantity)
                except Exception as e:
                    self.loggingMessage('administration_window',e)
                    self.ids.productQuantityEmptyErrorMessageId.text='Product quantity should numbers'
                    return

                'Making sure the Cost price field is not empty and is an integer or float'
                try:
                    pcostprice=float(pcostprice)
                    
                except Exception as e:
                    self.loggingMessage('administration_window',e)
                    self.ids.productCPriceEmptyErrorMessageId.text='Enter cost price(number)'
                    return
                
                'Making sure the Selling price field is not empty and is an integer or float'
                try:
                    psellingprice=float(psellingprice)
                except Exception as e:
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
                    # clearing products fields
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

                    self.ids.productToDeleteNameId.text=''
            except Exception as e:
                self.loggingMessage('administration_window',e)
                self.ids.productIdEmptyErrorMessageId.text='Wrong product id'
        except Exception as e:
            self.loggingMessage('administration_window',e)
            self.ids.productsEntryErrorsId.text='The is an issue trying to connect to the database to perform Update operation'
        finally:
            mydb.close()

    def searchProductsByName(self,*args, **kwargs):
        self.ids.noProductMessage.text=""

        '''this function is used to update a categories give its id,
        '''
        try:
            mydb=sqlite3.connect(self.databaseName)
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
                except Exception as e:
                    self.loggingMessage('administration_window',e)
                    self.ids.noProductMessage.text=f'No product with the name {searchedproduct}'
                    return

                self.ids.productListId.refresh_from_data()
                self.ids.productListId.data = listData
                self.ids.productToSearchId.text=''
                mydb.close()

        except Exception as e:
            self.loggingMessage('administration_window',e)
            self.ids.noProductMessage.text='The is an issue trying to connect to the database to perform the product search operation'
        finally:
            mydb.close()   


    # =================================THE USERS SECTION=========================
    # populating the products
    def fetchAllUsers(self):
        self.ids.userToSearchId.text=''
        self.ids.noUserMessage.text=""
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb=sqlite3.connect(self.databaseName)
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
        except Exception as e:
            self.loggingMessage('administration_window',e)
           
        finally:
            mydb.close()

    def searchUsersByName(self,*args, **kwargs):
        self.ids.noUserMessage.text=""
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb=sqlite3.connect(self.databaseName)
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
                except Exception as e:
                    self.loggingMessage('administration_window',e)
                    self.ids.noUserMessage.text=f'No user with the name {searcheduser}'
                    return

                self.ids.usersListId.refresh_from_data()
                self.ids.usersListId.data = userlistData
                self.ids.userToSearchId.text=''
                mydb.close()
        except Exception as e:
            self.loggingMessage('administration_window',e)
            self.ids.noUserMessage.text='The is an issue trying to connect to the database to perform the user search operation'
            return
        finally:
            mydb.close()

    def clearUserFields(self,instance):
        self.popup.dismiss()
        # clear user fields
        self.ids.userNameId.text=''
        self.ids.userEmailId.text=''
        self.ids.userPasswordId.text=''
        # self.ids.userDesignationId.text=''
        #clearing all error messages
        self.ids.userIdEmptyErrorMessageId.text=''
        self.ids.userIdEmptyErrorMessageId.text=''
        self.ids.userNameEmptyErrorMessageId.text=''
        self.ids.userEmailEmptyErrorMessageId.text=''
        self.ids.userPasswordEmptyErrorMessageId.text=''
        self.ids.userDesignationEmptyErrorMessageId.text=''


    def addUser(self,instance):
        self.popup.dismiss()
        # clearing all the error messages
        self.ids.userIdEmptyErrorMessageId.text=''
        self.ids.userIdEmptyErrorMessageId.text=''
        self.ids.userNameEmptyErrorMessageId.text=''
        self.ids.userEmailEmptyErrorMessageId.text=''
        self.ids.userPasswordEmptyErrorMessageId.text=''
        self.ids.userDesignationEmptyErrorMessageId.text=''
        
        '''this function is used to update a categories give its id,
        '''
        try:
            mydb=sqlite3.connect(self.databaseName)
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
                self.loggingMessage('administration_window',e)
                self.ids.usersEntryErrorsId.text='and error occured trying to add user'
                return
                
            else:
                "Making sure username is unique"
                cursor = mydb.cursor()
                cursor.execute('Select name from users;')
                namess= cursor.fetchall()
                listOfNames=[]
                for n in namess:
                    listOfNames.append(n[0])
                if username in  listOfNames:
                    self.ids.userNameEmptyErrorMessageId.text='Please user name already exist'
                    return
                
                query = f"insert into users (name,email,password,designation) values ('{username}','{useremail}','{userpassword}','{userdesignation}');"
                cursor = mydb.cursor()
                cursor.execute(query)
                mydb.commit()
                mydb.close()
                self.ids.usersListId.refresh_from_data()
                self.fetchAllUsers()
                # clear user fields
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
                self.summaryOfProducts_Employees()
        except Exception as e:
            self.loggingMessage('administration_window',e)
            self.ids.usersEntryErrorsId.text='The is an issue trying to connect to the database to add the user'
            return
        finally:
            mydb.close()  

    def updateUser(self,instance):
        self.popup.dismiss()
        # clearing all the error messages
        self.ids.userIdEmptyErrorMessageId.text=''
        self.ids.userIdEmptyErrorMessageId.text=''
        self.ids.userNameEmptyErrorMessageId.text=''
        self.ids.userEmailEmptyErrorMessageId.text=''
        self.ids.userPasswordEmptyErrorMessageId.text=''
        self.ids.userDesignationEmptyErrorMessageId.text=''

        userToUpdateId_= (self.ids.userToDeleteOrUpdateId.text).strip()

        '''this function is used to update a categories give its id,
        '''
        try:
            mydb=sqlite3.connect(self.databaseName)
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
                except Exception as e:
                    self.loggingMessage('administration_window',e)
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
                self.loggingMessage('administration_window',e)
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
                # clear user fields
                self.ids.userNameId.text=''
                self.ids.userEmailId.text=''
                self.ids.userPasswordId.text=''
                # self.ids.userDesignationId.text=''
                #clearing all error messages
                self.ids.userIdEmptyErrorMessageId.text=''
                self.ids.userIdEmptyErrorMessageId.text=''
                self.ids.userNameEmptyErrorMessageId.text=''
                self.ids.userEmailEmptyErrorMessageId.text=''
                self.ids.userPasswordEmptyErrorMessageId.text=''
                self.ids.userDesignationEmptyErrorMessageId.text=''

                self.ids.userToDeleteOrUpdateId.text=''
        except Exception as e:
            self.loggingMessage('administration_window',e)
            self.ids.usersEntryErrorsId.text='The is an issue trying to connect to the database to update the user'
            return
        finally:
            mydb.close() 

    def searchUserByIdButton(self,*args, **kwargs):
        self.ids.userIdEmptyErrorMessageId.text=''
        # clear user fields
        self.ids.userNameId.text=''
        self.ids.userEmailId.text=''
        self.ids.userPasswordId.text=''
        # self.ids.userDesignationId.text=''
        #clearing all error messages
        self.ids.userIdEmptyErrorMessageId.text=''
        self.ids.userIdEmptyErrorMessageId.text=''
        self.ids.userNameEmptyErrorMessageId.text=''
        self.ids.userEmailEmptyErrorMessageId.text=''
        self.ids.userPasswordEmptyErrorMessageId.text=''
        self.ids.userDesignationEmptyErrorMessageId.text=''
        
        UserId= (self.ids.userToDeleteOrUpdateId.text).strip()

        '''this function is used to update a categories give its id,
        '''
        try:
            mydb=sqlite3.connect(self.databaseName)
            try:
                UserId = int(UserId)
                query = f"SELECT * FROM users where user_id={UserId};"
                cursor = mydb.cursor()
                cursor.execute(query)
                result= cursor.fetchone()
                
                self.ids.userNameId.text=str(result[1])
                self.ids.userEmailId.text=str(result[2])
                self.ids.userPasswordId.text=str(result[3])
                self.ids.userDesignationId.text=str(result[4])

            except Exception as e:
                self.loggingMessage('administration_window',e)
                self.ids.userIdEmptyErrorMessageId.text=f'No user with id ="{UserId}"'
                return
        except Exception as e:
            self.loggingMessage('administration_window',e)
            self.ids.usersEntryErrorsId.text='The is an issue trying to connect to the database in order to search the user'
            return
        finally:
            mydb.close() 

    def deleteUser(self,instance):
        self.popup.dismiss()
        self.ids.userIdEmptyErrorMessageId.text=''
        self.ids.usersEntryErrorsId.text=''

        userToDeleteId= (self.ids.userToDeleteOrUpdateId.text).strip()

        '''this function is used to update a categories give its id,
        '''
        try:
            mydb=sqlite3.connect(self.databaseName)
            try:
                userToDeleteId= int(userToDeleteId)
                
                query = f"DELETE FROM users where user_id={int(userToDeleteId)};"
                cursor = mydb.cursor()
                cursor.execute(query)
                mydb.commit()
                mydb.close()
                self.ids.usersListId.refresh_from_data()
                self.fetchAllUsers()
                # clear user fields
                self.ids.userNameId.text=''
                self.ids.userEmailId.text=''
                self.ids.userPasswordId.text=''
                # self.ids.userDesignationId.text=''
                #clearing all error messages
                self.ids.userIdEmptyErrorMessageId.text=''
                self.ids.userIdEmptyErrorMessageId.text=''
                self.ids.userNameEmptyErrorMessageId.text=''
                self.ids.userEmailEmptyErrorMessageId.text=''
                self.ids.userPasswordEmptyErrorMessageId.text=''
                self.ids.userDesignationEmptyErrorMessageId.text=''

                self.ids.userToDeleteOrUpdateId.text=''
                self.summaryOfProducts_Employees()
            except Exception as e:
                
                self.loggingMessage('administration_window',e)
                self.ids.userIdEmptyErrorMessageId.text='wrong user id '
                return
             
        except Exception as e:
            self.loggingMessage('administration_window',e)
            self.ids.usersEntryErrorsId.text='The is an issue trying to connect to the database to perform delete operation'
            return
        finally:
            mydb.close()

    def summaryOfProducts_Employees(self):
        try:
            mydb=sqlite3.connect(self.databaseName)
            totalUsers = "SELECT user_id from users;"
            cursor = mydb.cursor()
            cursor.execute(totalUsers)
            employeesTotal=len(cursor.fetchall())
            self.ids.totalEmployeesId.text=str(employeesTotal)
            # totalporducts
            totalProducts ='SELECT product_id from products;'
            cursor = mydb.cursor()
            cursor.execute(totalProducts)
            productsTotal=len(cursor.fetchall())
            self.ids.productsTotalId.text=str(productsTotal)
            # MOST SOLD porducts
            namesOfProductsSold ='SELECT DISTINCT(product_name) from sales;'
            cursor = mydb.cursor()
            cursor.execute(namesOfProductsSold)
            names = cursor.fetchall()
            productName_value_pair ={}

            for name in names:
                prod =f"SELECT sales_id from sales where product_name='{name[0]}';"
                cursor = mydb.cursor()
                cursor.execute(prod)
                number = len(cursor.fetchall())
                productName_value_pair[number]=name[0]
            # getting the maximum and minimum value and using it to get the name of the product
            prodkeys =productName_value_pair.keys() 
            maxNumber= max(prodkeys)
            minNumber = min(prodkeys)
            mostSoldProduct=  productName_value_pair[maxNumber]
            listSoldProduct =productName_value_pair[minNumber]
            self.ids.mostSoldProductId.text=str(mostSoldProduct)
            self.ids.listSoldProductId.text=str(listSoldProduct)

            mydb.commit()
            mydb.close()
        except Exception as e:
            self.loggingMessage('administration_window',e)
        finally:
            mydb.close()

    def printsMontlyReport(self,instance):
        self.popup.dismiss()
        reportData =self.ids.monthRecycleViewId.data
        report=[]
        for r in reportData:
            report.append(r['text'])
        title=str(self.ids.monthlyReportTitleId.text).strip('[/u]')+'\n'
        reformatedReportList=[f'{title}','Item\t\t','No sold\t\t','Profit\t\t\n','------------------------------------------']
        for d in report:
            try:
                int(d[0])
                reformatedReportList.append(f'{d}\t\t')
            except:
                reformatedReportList.append(f'\n{d}\t\t')
                
        reportToPrint=' '.join(reformatedReportList)

        'write to file print and delete the report from the system'
        try:
            os.mkdir("MONTHLY_REPORTS")
            date = datetime.now()
            time_= date.strftime('%d-%b-%Y-%H-%M-%S')
            name=f'report_{time_}'
            file = open(f'MONTHLY_REPORTS/{name}.txt',"+w")
            file.write(reportToPrint)
            file.close()
            path =os.getcwd()+f'\\MONTHLY_REPORTS\\{name}.txt'
            # printing
            win32api.ShellExecute(0,'print',path,None,'.',0)
            
        except:
            date = datetime.now()
            time_= date.strftime('%d-%b-%Y-%H-%M-%S')
            name=f'report_{time_}'
            file = open(f'MONTHLY_REPORTS\\{name}.txt',"+w")
            file.write(reportToPrint)
            file.close()
            path =os.getcwd()+f'\\MONTHLY_REPORTS\\{name}.txt'
            # printing
            win32api.ShellExecute(0,'print',path,None,'.',0)
           
          

    
    def printsDailyReport(self,instance):
        self.popup.dismiss()
        reportData =self.ids.dailyRecycleViewId.data
        report=[]
        for r in reportData:
            report.append(r['text'])
        title=str(self.ids.dailyReportTitleId.text).strip('[/u]')+'\n'
        reformatedReportList=[f'{title}','Item\t\t','No sold\t\t','Profit\t\t\n','------------------------------------------']
        index_=0
        for d in report:
            try:
                int(d[0:])
                reformatedReportList.append(f'{d}\t\t')
                
            except:
                reformatedReportList.append(f'\n{d}\t\t')
                
                
        reportToPrint=' '.join(reformatedReportList)
       

        'write to file print and delete the report from the system'
        try:
            os.mkdir("DAILY_REPORTS")
            date = datetime.now()
            time_= date.strftime('%d-%b-%Y-%H-%M-%S')
            name=f'report_{time_}'
            file = open(f'DAILY_REPORTS/{name}.txt',"+w")
            file.write(reportToPrint)
            file.close()
            path =os.getcwd()+f'\\DAILY_REPORTS\\{name}.txt'
            # printing
            win32api.ShellExecute(0,'print',path,None,'.',0)
            
        except:
            date = datetime.now()
            time_= date.strftime('%d-%b-%Y-%H-%M-%S')
            name=f'report_{time_}'
            file = open(f'DAILY_REPORTS\\{name}.txt',"+w")
            file.write(reportToPrint)
            file.close()
            path =os.getcwd()+f'\\DAILY_REPORTS\\{name}.txt'
            # printing
            win32api.ShellExecute(0,'print',path,None,'.',0)
           
          

       
    def deletingAllSaveFilesEveryMonth(self):
        checkingDate=datetime.now()
        dateofdeleting= checkingDate.strftime('%d-%b-%Y')
        day = checkingDate.strftime('%d')
        if int(day)==1:
            try:
                mydb=sqlite3.connect(self.databaseName)

                'making sure the folders are deleated once every month'

                dates = "SELECT date from recordFilesDeletedDays;"
                cursor = mydb.cursor()
                cursor.execute(dates)
                alldates=cursor.fetchall()
                datesToCompare=[]
                for h in alldates:
                    try:
                        datesToCompare.append(h[0])
                    except Exception as e:
                        pass

                if dateofdeleting in datesToCompare:
                    pass
                else:
                    try:
                        insertDate = f"insert into recordFilesDeletedDays (date) values ('{dateofdeleting}');"
                        cursor = mydb.cursor()
                        cursor.execute(insertDate)
                        mydb.commit()
                        mydb.close()
                        foldersPath=os.getcwd()
                        shutil.rmtree(foldersPath+"\\DAILY_REPORTS")
                        shutil.rmtree(foldersPath+"\\MONTHLY_REPORTS")
                        shutil.rmtree(foldersPath+"\\SALES RECORDS FOLDER")
                    except:
                        pass
            except:
                pass
        

    def changeScreenToLogIn(self,btn):
        self.parent.parent.parent.ids.scrn_mngr_main.current='scrn_si'
        self.lpopup.dismiss()

    def logout(self): 
        layout=BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Do you want to logout?'))
        btnLayout=BoxLayout(spacing=50,
                            size_hint_y=None,
                            height=40)
        YBtn=Button(text='Yes')
        Nbtn=Button(text='No')
        btnLayout.add_widget(YBtn)
        btnLayout.add_widget(Nbtn)
        layout.add_widget(btnLayout)
        self.lpopup=Popup(
            size_hint=(None,None),
            size=(200,150),
            title='LogOut',
            content=layout,
        )
        self.lpopup.open()
        Nbtn.bind(on_press=self.lpopup.dismiss)
        YBtn.bind(on_press=self.changeScreenToLogIn)      
        
    
class AdministrationApp(App):
    def build(self):
        return AdministrationPage()
    
if __name__=="__main__":
    AdministrationApp().run()





















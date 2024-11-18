from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ObjectProperty,BooleanProperty
# import mysql.connector as DbConnector
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from datetime import date,datetime
import win32api
import time
import sqlite3
from contextlib import closing
import os
from kivy.lang import Builder


# sqlite3 connection

def get_db_connection():
    return sqlite3.connect('BERMS.db')


        
path = os.getcwd()
Builder.load_file(path +'/operator_window/operator1.kv')
        
class HomeScreen(Screen):
    '''This is the home screen and we can navigate to'''
    pass

class DailyReportScreen(Screen):
    '''This is the Daily Report Screen and we can navigate to'''
    pass


class OperatorScreenManager(ScreenManager):
    '''the manager for all the screens'''
    pass


class SelectableRecycleBoxLayout(FocusBehavior,LayoutSelectionBehavior,RecycleBoxLayout):
    """IT ADDS selection behavior and focus behavior to the view"""
    pass

class SelectableLabel(RecycleDataViewBehavior,Label):
    """
    THIS CLASS is use to create a selectable label for the recycleview class.
    IT ADDS selection behavior and focus behavior to the view"""
    buttontext=ObjectProperty()
    index = None
    selected = BooleanProperty(False)
    selectable= BooleanProperty(True)

    def get_db_connection(self):
        return sqlite3.connect('BERMS.db')


    def refresh_view_attrs(self, rv, index, data):
        """catch and handle the view changes"""
        self.index = index

        return super(SelectableLabel,self).refresh_view_attrs(rv, index, data)
    def on_touch_down(self, touch):
        if super(SelectableLabel,self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index,touch)
        
    def apply_selection(self, rv, index, is_selected):
        ''' Respond to selection of items in the view'''
        self.selected = is_selected
        if is_selected:
            splitDataIntoId_Name = (rv.data[index]['text']).split()
        
            getIdOfSelectedProduct = int(splitDataIntoId_Name[0])
            
            # print(self.parent.parent.parent.parent.parent.parent.children[1].children[3].children[3].text)#=======================================>
            try:
                #=====================================================================>is the boxlayout for the whole Homescreen
                                                                                                    #the boxlayout containing products to insert lables
                nameToInsert=(self.parent.parent.parent.parent.parent.parent.parent.children[0].children[1].children[7].children[4])
                priceToInsert=(self.parent.parent.parent.parent.parent.parent.parent.children[0].children[1].children[7].children[3])
                quantityToInsert=(self.parent.parent.parent.parent.parent.parent.parent.children[0].children[1].children[7].children[1])
                                                                                    #===========>is the second boxlayout(middle Boxlayout)
                
                
                productDetailsToInsert=self.getSelectedProduct(getIdOfSelectedProduct)


                nameToInsert.text=f"{productDetailsToInsert[0]}"
                priceToInsert.text=f"{productDetailsToInsert[1]}"
            except AttributeError as e:
                date = datetime.now()
                ms = (f'''[operation_window APP]: {date}
{e}
\n''')
                f = open('operation_windowApp-loggmessages.txt','a')
                f.write(ms)
                
            
        else:
            pass
        return super().apply_selection(rv, index, is_selected)
    
    def getSelectedProduct(self,id):
       
        '''this function is used to fetch all the products from the database and 
        insert them into the product window,
        which either based on search or all the products
        '''
        try:
           
            with closing(get_db_connection()) as mydb:
                "peform transactions"
                selectProduct = f"SELECT product_name,product_selling_price,product_quantity from products WHERE product_id ={id}"
                cursor = mydb.cursor()
                cursor.execute(selectProduct)
                product = cursor.fetchone()
                mydb.close()

                product[0] #this is use to throw an exception if the there is no name with the product searched
                prodQuantity=product[2]
                if int(prodQuantity)<=0:
                    product=('[color=#ff0000]Out of stock[/color]', 00.00,)
            
                return product
        except Exception as e:
            date = datetime.now()
            ms = (f'''[operation_window APP]: {date}
{e}
\n''')
            f = open('operation_windowApp-loggmessages.txt','a')
            f.write(ms)
            product=('[color=#ff0000]No product[/color]', 00.00,)
            return product
            
    
    


    

        


class OperationWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(OperationWindow,self).__init__(**kwargs)
        self.companyName=str(self.fetchCompanyDetails()[1])
        self.companyTell=str(self.fetchCompanyDetails()[2])
        self.companyLocation=str(self.fetchCompanyDetails()[3])

        
        

        
        # print(self.getProductRuningOutOfStock())
        self.populateProductOutOfStockView()
        self.generateBill()

        # initializing the switch button to be active
        self.ids.switchId.active=True
   
        self.searchProductsButtonFunction()

    def get_db_connection(self):
        return sqlite3.connect('BERMS.db')
    
    def searchProductsButtonFunction(self,*args, **kwargs):
        productName= (self.ids.searchTextId.text).strip()
        listOfproducts=self.fetchAllProducts(productName=productName)
        self.ids.recycle_view_id.data =[{'text':str(f"{x[0] }      {x[2] } ")} for x in listOfproducts]
        self.ids.recycle_view_id.refresh_from_data()
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
        if buttonClicked =="clear":
            okButton.bind(on_press=self.clearButton)
        if buttonClicked =="undo":
            okButton.bind(on_press=self.undoButton)
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

        self.ids.OperatorScreenManagerId.current="homeScreen"

        ''' 
        this makes the page to slide from the 
        left when the daily report button is clicked
        '''
        self.ids.homeScreenId.manager.transition.direction='right'
        
        
    
    def changeToDailyReportPage(self):
        '''
        change to the Daily report window page function
        '''
        self.ids.OperatorScreenManagerId.current="DailyReportScreen"

        '''
        this makes the page to slide from the right when the
        daily report button is clicked
        '''
        self.ids.DailyReportScreenId.manager.transition.direction='left'

        
    
    
    def fetchAllProducts(self,productName):
        self.productName=productName
        '''this function is used to fetch all the products from the database and 
        insert them into the product window,
        which either based on search or all the products
        '''
        try:
            with closing(get_db_connection()) as mydb:
                "peform transactions"
            
                if self.productName=='':
                    selectAllProducts = "SELECT * from products;"
                    cursor = mydb.cursor()
                    cursor.execute(selectAllProducts)
                    listOfAllProducts1 = cursor.fetchall()
                    return listOfAllProducts1
                else:
                    productToSearchName=str(self.productName+'%')
                    selectAllProducts = f" SELECT * FROM products WHERE product_name LIKE '{productToSearchName}';"
                    cursor = mydb.cursor()
                    cursor.execute(selectAllProducts)
                    listOfAllProducts1 = cursor.fetchall()
                    
                    listOfAllProducts1[0] #this is use to throw an exception if the there is no name with the product searched
                    mydb.close()
                    return listOfAllProducts1
        except Exception as e:
            
            listOfAllProducts1=[(0, '2345', 'No product with that name', 5.0, 6.0, 56, 'vegetables'),]
            self.loggingMessage('operation_window',e)
            return listOfAllProducts1
        finally:
            mydb.close()
            

    def addToCart(self):
        productName=(self.ids.productToPurchaseName.text).strip()
        productPrice=(self.ids.productToPurchasePrice.text).strip()
        productQuantity=(self.ids.productToPurchaseQuantity.text).strip()

        # making sure that the product quantity is an integer value
        try:
            self.ids.productQuantityErrorMessage.text=''
            int(productQuantity)#this is use to catch non interger exceptions

            if productName=="[color=#ff0000]No product[/color]" or productPrice=="0.00" or productName=='[color=#ff0000]Out of stock[/color]' or productName=='':
                
                # clearing the fills
                self.ids.productToPurchaseName.text=''
                self.ids.productToPurchasePrice.text=''
                self.ids.productToPurchaseQuantity.text='1'
                pass
            else:
                self.generateBill()
                # clearing the fills
                self.ids.productToPurchaseName.text=''
                self.ids.productToPurchasePrice.text=''
                self.ids.productToPurchaseQuantity.text='1'
                
        except Exception as e:
            
            self.ids.productQuantityErrorMessage.text="Enter Integer value as quantity"
            self.loggingMessage('operation_window',e)
            



    def clearButton(self,instance):
        self.popup.dismiss()
        self.ids.productToPurchaseName.text=''
        self.ids.productToPurchasePrice.text=''
        self.ids.productToPurchaseQuantity.text='1'

    def undoButton(self,instance):
        self.popup.dismiss()
        try:
            # Getting the text of the bill area
            billToUpdate =self.ids.billTextId.text

            # spiliting the bill products into list of porducts so that we can remove the last one
            pList =billToUpdate.split("\n")
            # getting the last product to remove  price and quantity in order to update the total cost
        
            productToRemove = pList[-1]
            pRemoveListObject=productToRemove.split()
            pRemovePrice = float(pRemoveListObject[1])
            pRemoveQuantity = float(pRemoveListObject[2])
            pToRemoveTotalCost = float(pRemovePrice * int(pRemoveQuantity))
            updatedTotalCost= float((self.ids.productTotalPriceId.text).strip())-pToRemoveTotalCost

            # removing the last products
            pList.remove(pList[-1])
            # converting the list back to string
            updatedBill = f''' 
\t{self.companyName}
\ttell:{self.companyTell}
\tlocation: {self.companyLocation}
\t
\tProduct\t\tPrice\t\tQt             
\t-----------------------------------\t\t'''
            # using indexing to get each product and edit it
            for productIndex in range(7,len(pList)):
                # converting each string of the products into a list to be able to get access to 
                # their name,price and quantity
                convertedList= pList[productIndex].split('\t')
                name_= str(convertedList[1])
                price_=str(convertedList[3])
                quantity_ = str(convertedList[5])

                # adding the products that are not removed to the bill again
                updatedBill = updatedBill + f'\n\t{name_}\t\t{price_}\t\t{quantity_}'

            # updating the bill fied with the new bill
            self.ids.billTextId.text=updatedBill
            # updating the total cost with the new total
            self.ids.productTotalPriceId.text= str(updatedTotalCost)
        except Exception as e:
            self.loggingMessage('operation_window',e)
            pass
        
        

    def populateProductOutOfStockView(self):
        dataList = self.getProductRuningOutOfStock()
        dataToPutIntoView = []
        outOfStockNumber= 0
        runingOutOfStockNumber=0
        for data in dataList:
            if int(data[1]) == 0:
                dataToPutIntoView.append({'text':f'[color=ff0000]{data[0]}[/color]'})
                outOfStockNumber+=1
            else:
                dataToPutIntoView.append({'text':f'[color=008000]{data[0]}[/color]'})
                runingOutOfStockNumber+=1
        
        if len(dataToPutIntoView)==0:
            self.ids.outOfStockRecycleViewId.data=[{'text':f'[color=0000FF]No product is runing out of stock[/color]'}]
        else:
            self.ids.outOfStockRecycleViewId.data=dataToPutIntoView

        self.ids.totalProductOfStock.text=f'{outOfStockNumber}'
        self.ids.totalProductRuningOutOfStock.text=f'{runingOutOfStockNumber}'
        
    
    def getProductRuningOutOfStock(self):
       
        '''this function is used to fetch all the products from the database and 
        insert them into the product window,
        which either based on search or all the products
        '''
        try:                          
            mydb=sqlite3.connect("BERMS.db")
            
            with closing(get_db_connection()) as mydb:
                "peform transactions"
                selectAllProducts = "SELECT product_name,product_quantity from products WHERE product_quantity < 5"
                cursor = mydb.cursor()
                cursor.execute(selectAllProducts)
                listOfAllProductsRuningOut = cursor.fetchall()
                listOfAllProductsRuningOut[0] #this is use to throw an exception if the there is no name with the product searched
                mydb.close()
                return listOfAllProductsRuningOut
        except Exception as e:
            # listOfAllProductsRuningOut=[(404, '2345', 'No product with that name', 5.0, 6.0, 56, 'vegetables'),]
            listOfAllProductsRuningOut=[]
            return listOfAllProductsRuningOut
        finally:
            mydb.close()


            
    def generateBill(self):
        pName =(self.ids.productToPurchaseName.text).strip()
        pAmount =(self.ids.productToPurchasePrice.text).strip()
        pQuantity =(self.ids.productToPurchaseQuantity.text).strip()

        productsTotalPrice = '0.00'
        if (str(pName)=='') or (str(pName)=="No product"):
            bill = f''' 
\t{self.companyName}
\ttell:{self.companyTell}
\tlocation: {self.companyLocation}
\t
\tProduct\t\tPrice\t\tQt             
\t-----------------------------------\t\t'''
            self.ids.productTotalPriceId.text=productsTotalPrice
            
        else:
            priviewsTotalCost=float((self.ids.productTotalPriceId.text).strip())
            newAddedCost =float(float(pAmount))* int(pQuantity)
            productsTotalPrice =f'{priviewsTotalCost+newAddedCost}'

            bill=self.ids.billTextId.text + f'\n\t{pName}\t\t{pAmount}\t\t{pQuantity}' 


        self.ids.productTotalPriceId.text=productsTotalPrice
        self.ids.billTextId.text=bill
        
    def finalizeButton(self):
        self.ids.folderCreationError.text=''
        isGenerateBill= self.ids.switchId.active
        # create a folder that contain todays date and save a .doc file contianing the sales of that day
        try:
            # making the main directory for the sales
            os.mkdir(f"SALES RECORDS FOLDER")

        except FileExistsError:

            # making a sub directory for each year
            try:
                today= date.today()
                year = today.strftime('%Y')
                os.mkdir(F'SALES RECORDS FOLDER/{year}')
                print("the year folder is creates successfully")
                
            except FileExistsError:
                # if the year directory exist the create a directory for each month
                try:
                    todaysMonth= date.today()
                    month = todaysMonth.strftime("%B")
                    os.mkdir(f"SALES RECORDS FOLDER/{year}/{month}")
                    
                except FileExistsError:
                    # if month folder exist then save the file in it
                    try:
                        pathToSaveFile = f"SALES RECORDS FOLDER/{year}/{month}"
                        dayOfOperation= datetime.now()
                        nameOfFile = dayOfOperation.strftime("%d-%m-%Y__time_%H-%M-%S")

                        filepath =f"{pathToSaveFile}/{nameOfFile}.txt"
                        file = open(filepath,'w+')
                        file.write(f'{self.ids.billTextId.text}\n\n\t{self.ids.costLableId.text} {self.ids.productTotalPriceId.text}')
                        file.close()

                        #this is where the printing of the document is done
                        try:
                            if isGenerateBill==True or str(isGenerateBill)== 1:
                                path =os.getcwd() # this is the path to the current location
                                # getting the file
                                filelocation= path +f'\{filepath}'

                                # start printing
                                self.ids.productTotalPriceId.text='0.00'
                                win32api.ShellExecute(0,'print',filelocation,None,'.',0)
                            else:
                                self.ids.productTotalPriceId.text='0.00'
                                

                        except Exception as e:
                            self.loggingMessage('operation_window',e)
                            self.ids.folderCreationError.text=f"An error occurred in printing file "

                    except Exception as e:
                        self.loggingMessage('operation_window',e)
                        self.ids.folderCreationError.text=f"An error occurred in creating document file "

                    
                except PermissionError as e:
                    self.loggingMessage('operation_window',e)
                    self.ids.folderCreationError.text=f"Your Operation System as denied you a pemission to create a '{month} folder' ."
                    
                except Exception as e:
                    self.loggingMessage('operation_window',e)
                    self.ids.folderCreationError.text=f"An error occurred in creating '{month} folder "



            except PermissionError as e:
                self.loggingMessage('operation_window',e)
                self.ids.folderCreationError.text=f"Your Operation System as denied you a pemission to create a 'SALES RECORDS FOLDER' ."

            except Exception as e:
                self.loggingMessage('operation_window',e)
                self.ids.folderCreationError.text=f"An error occurred in creating SALES RECORDS FOLDER "


        except PermissionError as e:
            self.loggingMessage('operation_window',e)
            self.ids.folderCreationError.text=f"Your Operation System as denied you a pemission to create a SALES RECORDS FOLDER ."
            
        except Exception as e:
            self.loggingMessage('operation_window',e)
            self.ids.folderCreationError.text=f"An error occurred in creating SALES RECORDS FOLDER "
        
            
        billupdate = f''' 
\t{self.companyName}
\ttell:{self.companyTell}
\tlocation: {self.companyLocation}
\t
\tProduct\t\tPrice\t\tQt             
\t-----------------------------------\t\t'''
        
        # saving the sold product to the sales table
        # and updating the products sold
        soldProducts = ((self.ids.billTextId.text).split('\n'))[7:] # this is how they will look like ['\topera\t\t800.0\t\t1', '\tsoneyy\t\t7777.0\t\t1', '\tfood\t\t150.0\t\t1']
      
        
        for prod in soldProducts:
            prod = prod.lstrip('\t') # ['soneyy\t\t7777.0\t\t1']['opera\t\t800.0\t\t1']['food\t\t150.0\t\t1']
            details = prod.split("\t\t")
            '''this contains the name,price and quantity of the products sold'''
            productName= details[0]
            productPrice=details[1]
            productQuantity=details[2]
                


            try:
                mydb=sqlite3.connect("BERMS.db",timeout=90.0)
                "getting the initial quantity of each product bought"
                getInitialProductQuantity= f"SELECT product_quantity,product_cost_price,product_selling_price from products where product_name='{productName}';"
                cursor = mydb.cursor()
                cursor.execute(getInitialProductQuantity)
                initialQuantity=cursor.fetchone()
                    
                  

                
                'updating the quantity of the product bought'
                updatedQuantity= int(initialQuantity[0])-int(productQuantity)
                
                udpateProduct = f"update products SET product_quantity={updatedQuantity} where product_name='{productName}';"
                cursor.execute(udpateProduct)
                mydb.commit()

                'adding to the sales table the sold products'
                profitMade =float(initialQuantity[2])-float(initialQuantity[1])
                soldDate =datetime.now()
                day = soldDate.strftime('%d %b %Y')
                month = soldDate.strftime('%b %Y')
                soldQuery = f"insert into sales (product_name,quantity_sold,profit_made,date,month) values('{productName}',{int(productQuantity)},{profitMade},'{day}','{month}');"
                
                cursor.execute(soldQuery)
                mydb.commit()
            
                
                
            except Exception as e:
                self.loggingMessage('operation_window',e)
                
            
        'reupdating the bill area'
        self.ids.billTextId.text=billupdate

        'refreshing the out of stock data'
        self.ids.outOfStockRecycleViewId.refresh_from_data()
        self.populateProductOutOfStockView()


    def fetchCompanyDetails(self):
            '''this function is used to update a categories give its id,
            '''
            try:
                mydb= sqlite3.connect('BERMS.db')
                query = "select * from company;"
                cursor = mydb.cursor()
                cursor.execute(query)
                details = cursor.fetchone()
                mydb.close()
                return details #(1,name,tell)
            except Exception as e:
                self.loggingMessage('operation_window',e)
                pass
    

# INSTANCE OF THE MAIN APP
class OperatorApp(App):
    def build(self):
        self.title ="BE.RMS"
        
        return OperationWindow()
    
if __name__ =="__main__":
    OperatorApp().run()






















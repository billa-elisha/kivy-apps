from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ObjectProperty,BooleanProperty
import mysql.connector as DbConnector
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.textinput import TextInput




        
        
        # TextInput.keyboard_on_key_down(self, window, keycode, text, modifiers)
        # return super().keyboard_on_key_down(window, keycode, text, modifiers)

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
            print('selection change to {0}'.format(rv.data[index]))
            getIdOfSelectedProduct = int(str(rv.data[index]['text'])[0])
            print(getIdOfSelectedProduct)
            print(self.ids.recycle_view_id)
            # print(OperationWindow.populateThePurchaseFields(self))
        else:
            # print('selection remove for {0}'.format(rv.data[index]))
            pass
        return super().apply_selection(rv, index, is_selected)
    
    

# class RecycleViewDataSuply:
#     user ='root'
#     dbpassword = '@#mysql@#'
#     host ='localhost'
#     database = "BE_RETAIL_MANAGEMENT_DATABASE"
#     def __init__(self,productName):
#         self.productName=productName
    
#     def fetchAllProducts(self):
#         '''this function is used to fetch all the products from the database and 
#         insert them into the product window,
#         which either based on search or all the products
#         '''
#         try:
#             mydb = DbConnector.connect(user=self.user, password=self.dbpassword,
#                                         host=self.host,
#                                         database=self.database
#                                         )
#             # print(self.ids.searchTextId.text,'text from inputxt')
            
#             if self.productName=='':
#                 selectAllProducts = "SELECT * from products"
#                 cursor = mydb.cursor()
#                 cursor.execute(selectAllProducts)
#                 listOfAllProducts = cursor.fetchall()
#                 print("this products is coming because the search box is empty")
#                 return listOfAllProducts
#             else:
#                 productToSearchName=str(self.productName+'%')
#                 selectAllProducts = f" SELECT * FROM products WHERE product_name LIKE '{productToSearchName}';"
#                 cursor = mydb.cursor()
#                 print(selectAllProducts)
#                 cursor.execute(selectAllProducts)
#                 listOfAllProducts = cursor.fetchall()
#                 print("this products is coming because the search box is  not empty")
#                 print(listOfAllProducts)
#                 return listOfAllProducts
#         except Exception as e:
#             print("This exception is coming from the fetchallproducts function",e)#==

# class CustomTextInputBox(TextInput):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
        
#     def keyboard_on_key_up(self, window, keycode):
#         if self.text=='':
#             '''
#             The listOfProducts will contain all the products in the system

#             '''
#             listOfproducts =CustomTextInputBox().keyboard_on_key_up(window=None, keycode=None)
#             self.data =[{'text':str(f"{x[0] }      {x[2] } ")} for x in listOfproducts]
            

            # listOfproducts =RecycleViewDataSuply(productName='').fetchAllProducts()
            
#         else:
#             '''
#             The listOfProducts will contain all the products your search for in the system
#             '''
#             listOfproducts=RecycleViewDataSuply(productName=self.text).fetchAllProducts()
            
#         return listOfproducts
    
# class ProductsRecycleView(RecycleView):
#     '''the recycle view class to contain the products data'''
#     def __init__(self,**kwargs):
#         super(ProductsRecycleView,self).__init__(**kwargs)

#     def dataToPopulateInRecycleView(self,):
#         listOfproducts =CustomTextInputBox().keyboard_on_key_up(window=None, keycode=None)
#         self.data =[{'text':str(f"{x[0] }      {x[2] } ")} for x in listOfproducts]
#         return self.data
    
    
     

    

        


class OperationWindow(BoxLayout):
    '''THIS IS THE MAIN PAGE OF THE APP'''
    

    def __init__(self, **kwargs):
        super(OperationWindow,self).__init__(**kwargs)

        # self.ids.searchTextId.keyboard_on_key_up(self,keycode)

   
        self.searchProductsButtonFunction()
    def searchProductsButtonFunction(self,*args, **kwargs):
        productName= (self.ids.searchTextId.text).strip()
        listOfproducts=self.fetchAllProducts(productName=productName)
        self.ids.recycle_view_id.data =[{'text':str(f"{x[0] }      {x[2] } ")} for x in listOfproducts]
        self.ids.recycle_view_id.refresh_from_data()
        

    

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

        
    def populateThePurchaseFields(self):
        t=self.ids.p.text
        return  t
    
    def fetchAllProducts(self,productName):
        user ='root'
        dbpassword = '@#mysql@#'
        host ='localhost'
        database = "BE_RETAIL_MANAGEMENT_DATABASE"
    
        self.productName=productName
        '''this function is used to fetch all the products from the database and 
        insert them into the product window,
        which either based on search or all the products
        '''
        try:
            mydb = DbConnector.connect(user=user, password=dbpassword,
                                        host=host,
                                        database=database
                                        )
            # print(self.ids.searchTextId.text,'text from inputxt')
            
            if self.productName=='':
                selectAllProducts = "SELECT * from products"
                cursor = mydb.cursor()
                cursor.execute(selectAllProducts)
                listOfAllProducts = cursor.fetchall()
                print("this products is coming because the search box is empty")
                return listOfAllProducts
            else:
                productToSearchName=str(self.productName+'%')
                selectAllProducts = f" SELECT * FROM products WHERE product_name LIKE '{productToSearchName}';"
                cursor = mydb.cursor()
                print(selectAllProducts)
                cursor.execute(selectAllProducts)
                listOfAllProducts = cursor.fetchall()
                print("this products is coming because the search box is  not empty")
                print(listOfAllProducts)
                return listOfAllProducts
        except Exception as e:
            print("This exception is coming from the fetchallproducts function",e)#==

        

    

            
    
   
    

# INSTANCE OF THE MAIN APP
class OperatorApp(App):
    def build(self):
        self.title ="BE.RMS"
        
        return OperationWindow()
    
if __name__ =="__main__":
    OperatorApp().run()































# class CustomTextInputBox(TextInput):
    #     def __init__(self, **kwargs):
    #         super().__init__(**kwargs)
    #         print(OperationWindow.d)
    #     def keyboard_on_key_up(self,window,keycode):
    #         productName=self.text
            
    #         print(productName)
    #         if productName=='':
    #             allProducts=self.fetchAllProducts()
    #             # self.ids.recycle_view_id.data =[{'text':str(f"{x[0] }      {x[2] } ")} for x in allProducts]
    #             # self.ids.recycle_view_id.refresh_from_data()

    #     def fetchAllProducts(self):
            
    #         '''this function is used to fetch all the products from the database and 
    #         insert them into the product window,
    #         which either based on search or all the products
    #         '''
    #         user ='root'
    #         dbpassword = '@#mysql@#'
    #         host ='localhost'
    #         database = "BE_RETAIL_MANAGEMENT_DATABASE"
    #         try:
    #             mydb = DbConnector.connect(user=user, password=dbpassword,
    #                                         host=host,
    #                                         database=database
    #                                         )
    #             # print(self.ids.searchTextId.text,'text from inputxt')
                
                
    #             selectAllProducts = "SELECT * from products"
    #             cursor = mydb.cursor()
    #             cursor.execute(selectAllProducts)
    #             listOfAllProducts = cursor.fetchall()
    #             print("this products is coming because the search box is empty")
    #             return listOfAllProducts
    #             # print('empty textbox')
    #             # .searchProductsButtonFunction(self)
    #         except Exception as e:
    #             print(e)

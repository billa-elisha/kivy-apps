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

import sys
sys.path.insert(0,r'D:\\dev\\BE.RMS\\utilities')



class SelectableRecycleBoxLayout(FocusBehavior,LayoutSelectionBehavior,RecycleBoxLayout):
    """IT ADDS selection behavior and focus behavior to the view"""
    pass
# THIS CLASS is use to create a selectable label for the recycleview class
class SelectableLabel(RecycleDataViewBehavior,Label):
    """IT ADDS selection behavior and focus behavior to the view"""
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
        else:
            print('selection remove for {0}'.format(rv.data[index]))
        return super().apply_selection(rv, index, is_selected)

# the recycle view class to contain the products data
class ProductsRecycleView(RecycleView):
    # class variables
    user ='root'
    dbpassword = '@#mysql@#'
    host ='localhost'
    database = "BE_RETAIL_MANAGEMENT_DATABASE"
    def __init__(self,**kwargs):
        super(ProductsRecycleView,self).__init__(**kwargs)
        listOfproducts =self.fetchAllProducts()
        self.data =[{'text':str(f"{x[0] }      {x[2] } ")} for x in listOfproducts]
        self.fetchAllProducts()



        # this function is used to fetch all the products from the database in insert them into the product 
        # window when we search for products
        # database connection variables
        
    def fetchAllProducts(self):
        try:
            mydb = DbConnector.connect(user=self.user, password=self.dbpassword,
                                        host=self.host,
                                        database=self.database
                                        )
            selectAllProducts = "SELECT * FROM products;"
            cursor = mydb.cursor()
            cursor.execute(selectAllProducts)
            listOfAllProducts = cursor.fetchall()
            print(listOfAllProducts)
            return listOfAllProducts
        except Exception as e:
            print(e)

    


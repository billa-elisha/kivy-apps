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
            # print('selection remove for {0}'.format(rv.data[index]))
            pass
        return super().apply_selection(rv, index, is_selected)
    
    



class ProductsRecycleView(RecycleView):
    '''the recycle view class to contain the products data'''
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
     

    def refresh_from_data(self, *largs, **kwargs):
        self.data =[{'text':'billaaa' }]
        return super().refresh_from_data(*largs, **kwargs)

       
        
    def fetchAllProducts(self):
        '''this function is used to fetch all the products from the database and 
        insert them into the product window'''
        try:
            mydb = DbConnector.connect(user=self.user, password=self.dbpassword,
                                        host=self.host,
                                        database=self.database
                                        )
            selectAllProducts = "SELECT * FROM products;"
            cursor = mydb.cursor()
            cursor.execute(selectAllProducts)
            listOfAllProducts = cursor.fetchall()
            # print(listOfAllProducts)
            return listOfAllProducts
        except Exception as e:
            print(e)#=================================>

    
class CustomTextInputBox(TextInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        
    def keyboard_on_key_up(self, window, keycode):
        d = ProductsRecycleView()
        d.data=[{'text':' '}]
        print(self.text)


class OperationWindow(BoxLayout):
    '''THIS IS THE MAIN PAGE OF THE APP'''
    def __init__(self, **kwargs):
        super(OperationWindow,self).__init__(**kwargs)
     
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

    
   
    

# INSTANCE OF THE MAIN APP
class OperatorApp(App):
    def build(self):
        self.title ="BE.RMS"
        
        return OperationWindow()
    
if __name__ =="__main__":
    OperatorApp().run()
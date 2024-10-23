from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ObjectProperty
from kivy.uix.recycleview import RecycleView
import mysql.connector as DbConnector


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
class CategoryRecycleView(RecycleView):
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.data=[{"text":'Electronics'},{"text":'Vergetables'},{"text":'Fruites'}]

    pass




class AdministrationPage(BoxLayout):
    def __init__(self, **kwargs):
        super(AdministrationPage,self).__init__(**kwargs)
        self.ids.errorMessagesId.text=''

        # self.categorylistId = ObjectProperty(None)

        # calling functions
        self.populateCategoryRecycleView()

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

    def addCategory(self):
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
            catName = self.ids.categoryTextId.text
            insertCategories = f"insert into categories values(cat_id,'{catName}');"
            cursor = mydb.cursor()
            cursor.execute(insertCategories)
            mydb.commit()
            mydb.close()

            # calling the fetch function
            self.populateCategoryRecycleView()

            # resetting the input field to nothing
            self.ids.categoryTextId.text=''
            # refreshing the recycle view
            self.ids.categorylistId.refresh_from_data()

            print("add function")
        except Exception as e:
            print(e)
            
        
    
    
    def updateCategory(self):
        self.ids.errorMessagesId.text=''
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
                catId = int(self.ids.productToDeletOrUpdate.text)
                
                # checking if the user has enter the new name of not
                newCatName=self.ids.categoryTextId.text
                if newCatName!="":
                    try:
                        updateCat = f"update categories SET category_name='{newCatName}' where cat_id={catId};"
                        print(updateCat)
                        cursor = mydb.cursor()
                        cursor.execute(updateCat)
                        mydb.commit()
                        mydb.close()
                    except:
                        self.ids.errorMessagesId.text="am having an issue in trying to update your category"

                    # calling the fetch function
                    self.populateCategoryRecycleView()

                    # resetting the input fields to nothing
                    self.ids.categoryTextId.text=''
                    self.ids.productToDeletOrUpdate.text=''
                    # refreshing the recycle view
                    self.ids.categorylistId.refresh_from_data()
                else:
                    self.ids.errorMessagesId.text="Please provide the new category name you want to update with"

            except Exception as e:
                self.ids.errorMessagesId.text="The id must not be empty and it should be a number in order to update"

                
        except Exception as e:
            self.ids.errorMessagesId.text="An issue occured in connecting the database"
            
    def deleteCategory(self):
        self.ids.errorMessagesId.text=''
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
                catId = int(self.ids.productToDeletOrUpdate.text)
                
                try:
                    deleteCat = f"delete from categories where cat_id={catId};"
                    cursor = mydb.cursor()
                    cursor.execute(deleteCat)
                    mydb.commit()
                    mydb.close()
                except:
                    self.ids.errorMessagesId.text="am having an issue in trying to delete your category"

                # calling the fetch function
                self.populateCategoryRecycleView()

                # resetting the input fields to nothing
                self.ids.categoryTextId.text=''
                self.ids.productToDeletOrUpdate.text=''
                # refreshing the recycle view
                self.ids.categorylistId.refresh_from_data()
                
            except Exception as e:
                self.ids.errorMessagesId.text="The id must not be empty and it should be a number in order to delete"

                
        except Exception as e:
            self.ids.errorMessagesId.text="An issue occured in connecting the database"
            
            
        
    
    

        
    



class AdministrationApp(App):
    def build(self):
        return AdministrationPage()
    
if __name__=="__main__":
    AdministrationApp().run()
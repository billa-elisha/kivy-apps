from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import  ObjectProperty
# imports for creating a fixed login window which is not resizeable
from kivy.config import Config
import mysql.connector as DbConnector




# setting the size of the page
Config.set('graphics', 'resizable', '0') 
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '600')

# The login page class
class LogInWindow(BoxLayout):
    '''
    this are variables that are in the kivy file
    which points to lables and input fills which will 
    be used to get their entry values
    '''
    userName = ObjectProperty(None)
    password = ObjectProperty(None)
    notAdminErrorMessage = ObjectProperty(None)
    userNameErrorMessage = ObjectProperty(None)
    userPasswordErrorMessage = ObjectProperty(None)

    # database connection variables
    user ='root'
    dbpassword = '@#mysql@#'
    host ='localhost'
    database = "BE_RETAIL_MANAGEMENT_DATABASE"

    # fetching user data from the database
    def fetchUserData(self):
        '''this is used to fetch user data from the database using name of the user.
        it returns
        1. the user data or none is there is no user with that name
        '''
        try:
            mydb = DbConnector.connect(user=self.user, password=self.dbpassword,
                                        host=self.host,
                                        database=self.database
                                        )
            fetchOneUserData = "SELECT name,password,designation FROM users WHERE name=%s"
            cursor = mydb.cursor()
            cursor.execute(fetchOneUserData,(self.userName.text,))
            userData = cursor.fetchone()
            return userData
        except:
            print('there is an exeption')
        
    # login validation function
    def validateLogin(self, isAdmin, *args, **kwargs):
        '''
        this function is used to varify and validate the login details
        of the user
        '''
        # clearing all the error messages 
        self.notAdminErrorMessage.text = ''
        self.userNameErrorMessage.text = ''
        self.userPasswordErrorMessage.text = ''
        

        fetchUserData = self.fetchUserData() # This is a tuple containing (name,password,designation) or None
        if fetchUserData==None:
            self.userNameErrorMessage.text ="User name is not found!"
        # validating the password and checking designation status
        else:
            # invalid password
            if self.password.text != fetchUserData[1]:
                self.userPasswordErrorMessage.text ="You entered wrong password"
            # for valid password
            else:
                # check of disignation wherther admin or operator
                if (str(isAdmin) == "False") and (fetchUserData[2]=='operator'):
                    # LOG IN THE OPERATING WINDOW
                    print("loging into the operator page")#======================================>
                    # clearing the input text after validation is done
                    self.userName.text = ''
                    self.password.text = ''

                # Not an admin error message
                elif (str(isAdmin)== "True") and (fetchUserData[2]=='operator'):
                    self.notAdminErrorMessage.text ="Please your are not an admin"
                    self.ids.admin.active=False

                # admin but loging into the operating window
                elif (str(isAdmin)== "False") and (fetchUserData[2]=='admin'):
                    print("admin but looging into the operating window")#==================================>
                    # clearing the input text after validation is done
                    self.userName.text = ''
                    self.password.text = ''

                # an admin loging into the admin window
                else:
                    self.ids.admin.active=False
                    print('loging into the admin window as an admin')
                    # clearing the input text after validation is done
                    self.userName.text = ''
                    self.password.text = ''

        # print(fetchUserData)
    
        
        
        


class LogInApp(App):
    def build(self):

        self.title ="BE.RMS"
        return LogInWindow()
    
if __name__=="__main__":
    LogInApp().run()
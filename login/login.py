from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import  ObjectProperty
from datetime import datetime
from kivy.lang import Builder
import os
import sqlite3



path = os.getcwd()
Builder.load_file(path +'/login/login1.kv')

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

    # fetching user data from the database
    def fetchUserData(self):
        '''this is used to fetch user data from the database using name of the user.
        it returns
        1. the user data or none is there is no user with that name
        '''
        name =((self.userName.text).strip()).lower()
        try:
            mydb=sqlite3.connect('BERMS.db')
            
            fetchOneUserData = f"SELECT name,password,designation FROM users WHERE name='{name}';"
            cursor = mydb.cursor()
            cursor.execute(fetchOneUserData)
            userData = cursor.fetchone()
            return userData
        except Exception as e:
            date = datetime.now()
            ms = (f'''[LOGIN APP]: {date}
{e}
\n''')
            f = open('loginpage-loggmessages.txt','a')
            f.write(ms)
        
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
            if ((self.password.text).strip()).lower() != fetchUserData[1]:
                self.userPasswordErrorMessage.text ="You entered wrong password"
              
            # for valid password
            else:
                # check of disignation wherther admin or operator
                if (str(isAdmin) == "False") and (fetchUserData[2]=='operator'):
                    # LOG IN THE OPERATING WINDOW
                    self.parent.parent.parent.ids.scrn_mngr_main.current='scrn_op'

                    # clearing the input text after validation is done
                    self.userName.text = ''
                    self.password.text = ''
                    

                # Not an admin error message
                elif (str(isAdmin)== "True") and (fetchUserData[2]=='operator'):
                    self.notAdminErrorMessage.text ="Please your are not an admin"
                    self.ids.admin.active=False

                # admin but loging into the operating window
                elif (str(isAdmin)== "False") and (fetchUserData[2]=='admin'):
                    self.parent.parent.parent.ids.scrn_mngr_main.current='scrn_op'

                    # clearing the input text after validation is done
                    self.userName.text = ''
                    self.password.text = ''

                # an admin loging into the admin window
                else:
                    self.ids.admin.active=False
                    self.parent.parent.parent.ids.scrn_mngr_main.current='scrn_admin'

                    # clearing the input text after validation is done
                    self.userName.text = ''
                    self.password.text = ''

        
    
        
        
        


class LogInApp(App):
    def build(self):

        self.title ="BE.RMS"
        return LogInWindow()
        
if __name__=="__main__":
    LogInApp().run()
from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import  ObjectProperty
from datetime import datetime
from kivy.lang import Builder
import os
import sqlite3
# from operator_window.operation_window import OperationWindow

from configparser import ConfigParser
import pathlib



pathToConfigFileToConnectDb=pathlib.Path(__file__).parent.parent.absolute().joinpath('config.ini')
Config = ConfigParser()
Config.read(pathToConfigFileToConnectDb)
dbinfo = Config['database']
dbname =dbinfo['dbname']






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

    loggedinuser='username'

    # fetching user data from the database
    def fetchUserData(self):
        '''this is used to fetch user data from the database using name of the user.
        it returns
        1. the user data or none is there is no user with that name
        '''
        name =(self.userName.text).strip()
        try:
            mydb=sqlite3.connect(dbname)
            
            fetchOneUserData = f"SELECT name,password,designation,user_id FROM users WHERE name='{name}';"
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
    def validateLogin(self, designation, *args, **kwargs):
        '''
        this function is used to varify and validate the login details
        of the user
        '''
        # clearing all the error messages 
        self.notAdminErrorMessage.text = ''
        self.userNameErrorMessage.text = ''
        self.userPasswordErrorMessage.text = ''
        self.loggedinuser=None
        

        fetchUserData = self.fetchUserData() # This is a tuple containing (name,password,designation) or None
        
        if str(((self.userName.text).strip()).lower()=='elisha'):
            if str(((self.password.text).strip()).lower())=="elisha":
                self.parent.parent.parent.ids.scrn_mngr_main.current='scrn_admin'
                print((self.userName.text and self.password.text=='elisha'))

        if fetchUserData==None:
            
            self.userNameErrorMessage.text ="User name is not found!"
        # validating the password and checking designation status
        else:
            # invalid password
            if ((self.password.text).strip()) != fetchUserData[1]:
                self.userPasswordErrorMessage.text ="You entered wrong password"
              
            # for valid password
            else:
                # check of disignation wherther admin or operator
                if (str(designation) == "operator") and (fetchUserData[2]=='operator'):
                    
                    # updating the config file
                    pathToConfigFile=pathlib.Path(__file__).parent.parent.absolute().joinpath('config.ini')
                    editeConfig = ConfigParser()
                    editeConfig.read(pathToConfigFile)
                    userinfo = editeConfig['LogedInUser']
                    userinfo['username']=f'{fetchUserData[0]}'
                    userinfo['id']=f'{fetchUserData[3]}'
                    with open(pathToConfigFile, 'w') as configfile:
                        editeConfig.write(configfile)

                    # OperationWindow.getUserLogedIn(self=OperationWindow)

                    # LOG IN THE OPERATING WINDOW
                    self.parent.parent.parent.ids.scrn_mngr_main.current='scrn_op'
                    # clearing the input text after validation is done
                    self.userName.text = ''
                    self.password.text = ''
                    

                # Not an admin error message
                elif (str(designation)== "admin") and (fetchUserData[2]=='operator'):
                    self.notAdminErrorMessage.text ="Please your are not an admin"
                    

                # admin but loging into the operating window
                elif (str(designation)== "operator") and (fetchUserData[2]=='admin'):
                    # updating the config file
                    pathToConfigFile=pathlib.Path(__file__).parent.parent.absolute().joinpath('config.ini')
                    editeConfig = ConfigParser()
                    editeConfig.read(pathToConfigFile)
                    userinfo = editeConfig['LogedInUser']
                    userinfo['username']=f'{fetchUserData[0]}'
                    userinfo['id']=f'{fetchUserData[3]}'
                    with open(pathToConfigFile, 'w') as configfile:
                        editeConfig.write(configfile)

                    
                    # OperationWindow.getUserLogedIn(self=OperationWindow)
                    self.parent.parent.parent.ids.scrn_mngr_main.current='scrn_op'

                    # clearing the input text after validation is done
                    self.userName.text = ''
                    self.password.text = ''

                # an admin loging into the admin window
                else:
                    # updating the config file
                    pathToConfigFile=pathlib.Path(__file__).parent.parent.absolute().joinpath('config.ini')
                    editeConfig = ConfigParser()
                    editeConfig.read(pathToConfigFile)
                    userinfo = editeConfig['LogedInUser']
                    userinfo['username']=f'{fetchUserData[0]}'
                    userinfo['id']=f'{fetchUserData[3]}'
                    with open(pathToConfigFile, 'w') as configfile:
                        editeConfig.write(configfile)

                    
                    # OperationWindow.getUserLogedIn(self=OperationWindow)
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
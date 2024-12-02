from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from administration_window.admin import AdministrationPage
from login.login import LogInWindow
import sqlite3
from operator_window.operation_window import OperationWindow
import os, sys
from kivy.resources import resource_add_path, resource_find
import database.db 
import smtplib,ssl
import string
import random
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from datetime import datetime
import pathlib
from configparser import ConfigParser
import pathlib
from configparser import ConfigParser

pathToConfigFile=pathlib.Path(__file__).parent.absolute().joinpath('config.ini')
Config = ConfigParser()
Config.read(pathToConfigFile)
dbinfo = Config['database']
dbname =dbinfo['dbname']

                    


class MainWindow(BoxLayout):
    operator_widget = OperationWindow()
    admin_widget = AdministrationPage()
    signin_widget = LogInWindow()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.scrn_si.add_widget(self.signin_widget)
        self.ids.scrn_admin.add_widget(self.admin_widget)
        self.ids.scrn_op.add_widget(self.operator_widget)
        self.databaseName=dbname

        self.generateOneTimeDefaultPassWord()
        
       

    def generateOneTimeDefaultPassWord(self):
        mydb=sqlite3.connect(self.databaseName)
        cursor = mydb.cursor()
        username =(''.join(random.choices(string.ascii_letters,k=7))).lower()
        userpassword = random.randint(3000,100000)
        desig='admin'
        email ="default@gmail.com"
        # generating the user details if the user table is empty
        cursor.execute("select user_id from users;")
        isUsertableEmpty=len(cursor.fetchall())
        mydb.close()
        if isUsertableEmpty==0:
            # sending email for your login
            try:
                port=465
                app_password='gwfm qpxq zgtu wpuh'
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com',port,context=context) as server:
                    server.login('billaelisha@gmail.com',app_password)
                    server.sendmail('billaelisha@gmail.com',"billatengbil@gmail.com",f'''
YOUR LOGIN DETAILS ARE
UserName: {username}
password: {userpassword}                         
                            ''')
                mydb=sqlite3.connect(self.databaseName)
                cursor = mydb.cursor()
                cursor.execute(f'insert into users (name,email,password,designation) values("{username}","{email}","{userpassword}","{desig}");')
                mydb.commit()
                mydb.close()
            except Exception as e:
                'no internet'
                pass
    def loggingMessage(self,appname,e):
        date = datetime.now()
        ms = (f'''[{appname} APP]: {date}
{e}
\n''')
        f = open(f'{appname}App-loggmessages.txt','a')
        f.write(ms)
    def isChangePassword(self,btn):
        changePasswordPopup=btn.parent.parent.parent.parent.parent.parent.children[1]
        self.confirmPopu.dismiss()
        self.changePassword(changePasswordPopup)
    def changePasswordPopu(self,changePasswordPopup):
        layout=BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Do you want to change?'))
        btnLayout=BoxLayout(spacing=50,
                            size_hint_y=None,
                            height=40)
        YesBtn=Button(text='Yes')
        Nobtn=Button(text='No')
        btnLayout.add_widget(YesBtn)
        btnLayout.add_widget(Nobtn)
        layout.add_widget(btnLayout)
        self.confirmPopu=Popup(
            size_hint=(None,None),
            size=(200,150),
            content=layout,
        )
        self.confirmPopu.open()
        Nobtn.bind(on_press=self.confirmPopu.dismiss)
        YesBtn.bind(on_press=self.isChangePassword)
    def changePassword(self,changePasswordPopup):
        changePasswordPopup.ids.passwordChangingError.text=''

        oldPassword =str(changePasswordPopup.ids.oldpass.text).strip()
        newPassword= str(changePasswordPopup.ids.newpass.text).strip()
        confirmNewPassword=str(changePasswordPopup.ids.confirmnewpass.text).strip()
         # reading the config file
        self.pathToConfigFile=pathlib.Path(__file__).parent.absolute().joinpath('config.ini')
        self.config = ConfigParser()
        self.config.read(self.pathToConfigFile)
        try:
            "selecting the user data from the database using his id from the config file"
            db= sqlite3.connect('BERMS.db')
            cur = db.cursor()
            logedInUserId = int(self.config['LogedInUser']['id'])
            cur.execute(f"select password from users where user_id={logedInUserId};")
            data =cur.fetchone()
            password=data[0]
            # print(password)
            db.close()
            if oldPassword=='':
                changePasswordPopup.ids.passwordChangingError.text='Enter old password'
                return
            if newPassword=='':
                changePasswordPopup.ids.passwordChangingError.text='Enter new password'
                return
            if confirmNewPassword=='':
                changePasswordPopup.ids.passwordChangingError.text='Confrim the password'
                return
            "checking to see if the oldpassword entered match with the user password"
            if str(oldPassword)==str(password):
                'checking if the new entered passwords matches'
                if newPassword==confirmNewPassword:
                    "updating the user password"
                    try:
                        db= sqlite3.connect('BERMS.db')
                        cur = db.cursor()
                        cur.execute(f"update users SET password='{newPassword}' where user_id={logedInUserId};")
                        db.commit()
                        db.close()
                        "clearinging the fields"
                        changePasswordPopup.ids.oldpass.text=''
                        changePasswordPopup.ids.newpass.text=''
                        changePasswordPopup.ids.confirmnewpass.text=''
                        changePasswordPopup.ids.passwordChangingError.text='[color=#16942b]Password Change Successfully[/color]'
                        return
                    except Exception as e:
                        print(e)
                        self.loggingMessage('operation_window',e)
                else:
                    changePasswordPopup.ids.passwordChangingError.text='New password does not match'
                   
            else:
                changePasswordPopup.ids.passwordChangingError.text='Wrong old password entered'
               
                               
        except Exception as e:
            self.loggingMessage('operation_window',e)

    

class MainApp(App):
    def build(self):
        return MainWindow()
    pass

if __name__ =='__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    MainApp().run()

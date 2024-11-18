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



class MainWindow(BoxLayout):
    operator_widget = OperationWindow()
    admin_widget = AdministrationPage()
    signin_widget = LogInWindow()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.scrn_si.add_widget(self.signin_widget)
        self.ids.scrn_admin.add_widget(self.admin_widget)
        self.ids.scrn_op.add_widget(self.operator_widget)
        self.databaseName='BERMS.db'
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


class MainApp(App):
    def build(self):
        return MainWindow()
    pass

if __name__ =='__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    MainApp().run()

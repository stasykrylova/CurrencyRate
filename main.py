from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import sqlite3
import plyer


class MainWindow(Screen):
    password_db = ''

    def into_sys(self):
        if self.user_name.text != "":
            if self.user_password.text != "":
                self.password_db = self.check(self.user_name.text)
                if self.password_db[0][0] != '':

                    if self.password_db[0][0] == self.user_password.text:
                        print("Вы вошли в систему!")
                    else:
                        plyer.notification.notify(title='Внимание!', message="Неправильный пароль!")
                else:
                    plyer.notification.notify(title='Внимание!', message="Пользователя с таким именем не существует!")
            else:
                plyer.notification.notify(title='Внимание!', message="Пароль должен быть заполнен!")
        else:
            plyer.notification.notify(title='Внимание!', message="Логин должен быть заполнен!")

    def add_user(self):
        con = sqlite3.connect('user.db')
        cur = con.cursor()
        cur.execute(""" INSERT INTO id (user,password)
                VALUES (?,?)
        """, (self.user_name.text, self.user_password.text)
                    )
        con.commit()
        con.close()

    @staticmethod
    def check(user_name):
        con = sqlite3.connect('user.db')
        cur = con.cursor()
        sql = "SELECT password FROM id WHERE user = ?"
        cur.execute(sql, [user_name])
        result = cur.fetchall()
        con.commit()
        con.close()
        return result


class Registration(Screen):
    pass


class Manager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")


class MainApp(App):

    def build(self):
        con = sqlite3.connect('user.db')
        cur = con.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS id(
            user text,
            password text)
            """)
        con.commit()
        con.close()
        return kv


if __name__ == "__main__":
    app = MainApp()
    app.run()

# Можно как тестовые акции покупка по прогнозу\продажа по прогнозу

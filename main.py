from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition
from kivy.lang import Builder
import sqlite3
import plyer


class MainWindow(Screen):
    password_db = ''

    def authorise(self):
        if self.user_name.text != "":
            if self.user_password.text != "":
                data_db = self.check(self.user_name.text)
                if data_db:
                    if data_db[0][1] == self.user_password.text:
                        print("Вы вошли в систему!")
                        self.new_page_open(data_db[0][2])
                    else:
                        plyer.notification.notify(title='Внимание!', message="Неправильный пароль!")
                else:
                    plyer.notification.notify(title='Внимание!', message="Пользователя с таким именем не существует!")
            else:
                plyer.notification.notify(title='Внимание!', message="Пароль должен быть заполнен!")
        else:
            plyer.notification.notify(title='Внимание!', message="Логин должен быть заполнен!")

    def register(self):
        if self.user_name.text != "":
            if self.user_password.text != "":
                user_pas_db = self.check(self.user_name.text)
                if not user_pas_db:
                    self.add_user(self.user_name.text, self.user_password.text)
                    plyer.notification.notify(title='Успех!',
                                              message="Пользователь зарегестрирован! Теперь войдите в систему!")
                    self.user_name.text = ""
                    self.user_password.text = ""
                else:
                    plyer.notification.notify(title='Внимание!', message="Пользователь уже зарегестрирован!")
            else:
                plyer.notification.notify(title='Внимание!', message="Пароль должен быть заполнен!")
        else:
            plyer.notification.notify(title='Внимание!', message="Логин должен быть заполнен!")

    @staticmethod
    def add_user(user_name, user_password):
        con = sqlite3.connect('user.db')
        cur = con.cursor()
        cur.execute(""" INSERT INTO id (user,password)
                VALUES (?,?)
        """, (user_name, user_password)
                    )
        con.commit()
        con.close()

    @staticmethod
    def check(user_name):
        con = sqlite3.connect('user.db')
        cur = con.cursor()
        sql = "SELECT * FROM id WHERE user = ?"
        cur.execute(sql, [user_name])
        result = cur.fetchall()
        con.commit()
        con.close()
        return result

    def new_page_open(self, code):
        if code == 100:
            self.manager.transition = RiseInTransition(duration=0.5)
            self.manager.current = 'menu_usr'
        elif code == 200:
            self.manager.transition = RiseInTransition(duration=0.5)
            self.manager.current = 'menu_red'
        elif code == 300:
            self.manager.transition = RiseInTransition(duration=0.5)
            self.manager.current = 'menu_adm'


class MenuWindowForAdministrator(Screen):
    pass


class MenuWindowForRedactor(Screen):
    pass


class AddingUser(Screen):

    def add_user(self):
        if self.login.text == '' or self.password.text == '' or self.role.text == '':
            plyer.notification.notify(title='Внимание!', message="Необходимо заполнить все поля!")
        elif self.role.text != "ученик" and self.role.text != "редактор" and self.role.text != "администратор":
            plyer.notification.notify(title='Внимание!',
                                      message="Роль должна быть ученик, редактор или администратор!")
        else:
            choices_dict = {'ученик': 100, 'редактор': 200, 'администратор': 300}
            role = choices_dict.get(self.role.text)
            con = sqlite3.connect('user.db')
            cur = con.cursor()
            try:
                cur.execute(""" INSERT INTO id (user,password,role)
                                VALUES (?,?,?)
                        """, (self.login.text, self.password.text, role)
                            )
                plyer.notification.notify(title='Успех!', message="Пользователь добавлен!")
                self.manager.transition = RiseInTransition(duration=0.5)
                self.manager.current = 'menu_adm'
            except sqlite3.IntegrityError:
                plyer.notification.notify(title='Внимание!', message="Пользователь уже существует!")
            con.commit()
            con.close()


class MenuWindowForUser(Screen):
    pass


class AddingMaterial(Screen):
    def add_material(self):
        if self.title.text == '' or self.text.text == '':
            plyer.notification.notify(title='Внимание!', message="Все поля должны быть заполнены!")
        else:
            con = sqlite3.connect('user.db')
            cur = con.cursor()
            try:
                cur.execute(""" INSERT INTO materials (title,material)
                                        VALUES (?,?)
                                """, (self.title.text, self.text.text)
                            )
                plyer.notification.notify(title='Успех!', message="Материал добавлен!")
                self.title.text = ''
                self.text.text = ''
            except sqlite3.IntegrityError:
                plyer.notification.notify(title='Внимание!', message="Попробуйте еще раз, что-то пошло не так!")
            con.commit()
            con.close()


class ReadingMaterial(Screen):
    result = []
    i = 0
    n = len(result)

    def get_materials(self):
        con = sqlite3.connect('user.db')
        cur = con.cursor()
        sql = "SELECT * FROM materials"
        cur.execute(sql)
        self.result = cur.fetchall()
        con.commit()
        con.close()
        if self.result:
            self.n = len(self.result)
            self.title.text = self.result[self.i][1]
            self.text.text = self.result[self.i][2]
            self.i += 1
        else:
            self.title.text = "Пока нет материалов"
            self.text.text = " "

    def change_text(self):
        if self.i < self.n:
            self.title.text = self.result[self.i][1]
            self.text.text = self.result[self.i][2]
            self.i += 1

        else:
            self.i = 0
            self.title.text = self.result[self.i][1]
            self.text.text = self.result[self.i][2]
            self.i += 1


class Calculator(Screen):
    def calculate(self, calculation):
        if calculation:
            try:
                self.display.text = str(eval(calculation))
            except Exception:
                self.display.text = "Ошибка"


class Manager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")


class MainApp(App):

    def build(self):
        con = sqlite3.connect('user.db')
        cur = con.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS id(
            USER text,
            password text,
            role int NOT NULL DEFAULT 100,
            PRIMARY KEY (USER)
            FOREIGN KEY (role) REFERENCES roles(ID)
            )
            """)
        cur.execute(""" CREATE TABLE IF NOT EXISTS materials(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    title text NOT NULL,
                    material text NOT NULL
                    )
                    """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS roles(
            ID int,
            role text,
            PRIMARY KEY (ID)
            )
            """)
        try:
            cur.execute(""" INSERT INTO roles (role,id)
                    VALUES ("administrator", 300), ("user", 100), ("redactor", 200)
            """)
        except sqlite3.IntegrityError:
            pass
        con.commit()
        con.close()
        return kv


if __name__ == "__main__":
    app = MainApp()
    app.run()

# Можно как тестовые акции покупка по прогнозу\продажа по прогнозу

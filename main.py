import mysql.connector
import tkinter as Tkinter
import csv
import yaml

# Creating a GUI, Grid
class View:
    def __init__(self):
        self.selected = []
        self.db = DBHandler()
        self.table_names = self.db.show_tables()
        print(self.table_names)

    def render_table(self):
        id = 0
        root = Tkinter.Tk()
        root.title('Simon Balázs - MySQL GUI CSV EXPORTER')
        root.geometry("500x250")
        for table in self.table_names:
            var = Tkinter.IntVar()
            Tkinter.Checkbutton(root, variable = var).grid(row = id,column = 2,)
            Tkinter.Label(root, text = table, borderwidth=1, font=("Helvetica", 18) ).grid(row = id, column = 3)
            self.selected.append(var)
            id = id + 1
        def check():
            for st, na in zip(self.selected, self.table_names):
                if st.get() == 1:
                    users = self.db.get_user(na[0])
                    with open('./' + na[0] + '.csv', "w") as f:
                        writer = csv.writer(f)
                        for row in users:
                            writer.writerow(row)

        Tkinter.Button(root, text='Save', command = check, font=("Helvetica", 18)).grid(row = 10, column= 2)
        Tkinter.Button(root, text='Quit', command = root.quit, font=("Helvetica", 18)).grid(row = 10, column= 3)

        print(self.selected)
        root.mainloop()

# Connecting to MySQL Database.
class DBHandler:
    def __init__(self):

        # Connection credentials.
        self.config = self.load_config()
        self.connection = mysql.connector.connect(
            host = self.config.get('mysql_host'),
            user = self.config.get('mysql_user'),
            passwd = self.config.get('mysql_password'),
            auth_plugin = "mysql_native_password",
            database= self.config.get('mysql_db'),
            port = self.config.get('mysql_port')
        )
        self.cursor = self.connection.cursor()

# Getting connection credentials from config.yaml.
    def load_config(self):
        with open("config.yaml", 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

# Creating test tables.
    def test(self):
        self.cursor.execute("CREATE TABLE students(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, dob DATE );")
        self.cursor.execute("CREATE TABLE class(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL);")

# Inserting test data to test tables.
    def adduser(self):
        self.cursor.execute("insert into students (name, birthday) values ('My Name is A', '1991-08-01')")
        self.cursor.execute("insert into students (name, birthday) values ('My Name is B', '1992-08-02')")
        self.cursor.execute("insert into students (name, birthday) values ('My Name is C', '1993-08-03')")
        self.cursor.execute("insert into students (name, birthday) values ('My Name is D', '1994-08-04')")
        self.cursor.execute("insert into students (name, birthday) values ('My Name is E', '1995-08-05')")
        self.cursor.execute("insert into students (name, birthday) values ('My Name is F', '1996-08-06')")
        self.cursor.execute("insert into students (name, birthday) values ('My Name is G', '1997-08-07')")
        self.cursor.execute("INSERT INTO class  (name) VALUES ('Class1')")
        self.cursor.execute("INSERT INTO class  (name) VALUES ('Class2')")
        self.cursor.execute("INSERT INTO class  (name) VALUES ('Class3')")
        self.cursor.execute("INSERT INTO class  (name) VALUES ('Class4')")

        self.connection.commit()

    def get_user(self, table_name):
        self.cursor.execute("select * from " + table_name)
        return self.cursor.fetchall()

    def show_tables(self):
        self.cursor.execute("show tables")
        return self.cursor.fetchall()

view = View()
view.render_table()

###
# Application to create a #to-do List using MySQL database
###

import mysql.connector
from mysql.connector import errorcode
from datetime import date

def getConnection():
    try:
        file = open('DatabaseConnection/credentials.txt', 'r')

        config = {}

        lines = file.readlines()
        for line in lines:
            (key, value) = line.strip().split('=')
            config[key] = value
        cnx = mysql.connector.connect(user=config['username'], password=config['password'], host='localhost',database='PythonLearning')
        return cnx
    except Exception as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

def closeConnection(cxn):
    if cxn.is_connected():
        cxn.close()

def insertTask(taskDescription):
    try:
        maxid = 0
        cxn = getConnection()
        tableCursor = cxn.cursor()
        tableCursor.execute("select max(id) from ToDoList")
        max_id = tableCursor.fetchone()
        for id in max_id:
            maxid = id
        maxid += 1

        today = date.today()
        # dd/mm/YY
        d1 = today.strftime("%m/%d/%Y")
        sql = "INSERT INTO ToDoList (id, task, date, status) VALUES (%s, %s, %s, %s)"
        val = (maxid, taskDescription,str(d1),'PEND')
        tableCursor.execute(sql, val)
        cxn.commit()
        print(tableCursor.rowcount, "Task Added.")

    except Exception as err:
            print(err)
    finally:
        closeConnection(cxn)


if __name__ == '__main__':

    cont = True
    while cont:
        option = int(input("Please select an option -\n 1. Insert Task. \n 2. exit \n ---> "))
        if option == 1:
            task_description = input("Please enter the task description -- ")
            insertTask(task_description)
            continue
        if option == 2:
            cont = False


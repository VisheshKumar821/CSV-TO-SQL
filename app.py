import time
import mysql.connector
import csv

def csvtolist(filename):
    name = filename.split(".")
    name = name[0]
    dictionary = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        for i in range(len(fields)):
            fields[i] = fields[i].strip()
        for i in reader:
            dictionary.append(i)
        all_data = [[i[items] for items in fields] for i in dictionary]
    return all_data, fields, name

def typecheck(item, i):
    if item[i].strip().isdigit():
        item[i] = int(item[i])
    else:
        item[i] = str(item[i].strip())
username = input("Enter the username for the SQL:>>")

passkey = input("Enter the password for the SQL:>>")
db = mysql.connector.connect(host="localhost", user=username, password=passkey, database="mysql")
cursor = db.cursor(buffered=True)
t = False
print("Hi,\nI have created this project in which you have to paste your csv file,\nand it will convert it into sql data,\nand write queries to it.")
time.sleep(3)
print()

def sql_runner():
    global t
    while t == True:
        if t == True:
            try:
                i = input("SQL (back() for menu)>>")
                if t == False:
                    break
                elif i == "back()":
                    print(i)
                    t = False
                    break
                else:
                    if t == False:
                        break
                    else:
                        try:
                            cursor.execute(i)
                            for rows in cursor.fetchall():
                                print(rows)
                        except Exception as e:
                            if str(f"{e}") == "'NoneType' object is not subscriptable":
                                print("None")
                            else:
                                print(f"Error : {e}")
                db.commit()
            except:
                t = False
        else:
            break

def sql_writer(fieldname, all_data, fields):
    for item in all_data:
        for i in range(len(item)):
            typecheck(item, i)
    variables = [i for i in fields]  # type: ignore

    data1 = all_data[0]

    for i in data1:
        if type(i) == int:
            variables[data1.index(i)] += " INT,"
        elif type(i) == float:
            variables[data1.index(i)] += " FLOAT,"
        else:
            variables[data1.index(i)] += " VARCHAR({}),".format(input(f"What's the maximum length you want to put in '{variables[data1.index(i)]}' \n>> "))

    variables.append("Primary key ({})".format(input(f"What's the primary key here? {str([i for i in fields])} \n>> ")))  # type: ignore

    calling = "%s" * (len(fields) + 1)  # type: ignore
    try:
        types = ""
        for i in variables:
            types += i
        cursor.execute(f'CREATE TABLE {fieldname} (' + types + ');')
    except Exception as e:
        if str(f"{e}") == "'NoneType' object is not subscriptable":
            print(None)
        else:
            print(f"Error: {e}")
        end_choice = input("File name is in use, kindly use some different name or leave the choice to go to SQL \n>> ")
        if end_choice == "":
            sql_runner()
        else:
            fieldname = end_choice
            cursor.execute(f'CREATE TABLE {fieldname} (' + types + ');')

    new_call = ""
    for i in range(len(calling)):
        if i == len(calling) - 2 or i == len(calling) - 1:
            pass
        else:
            new_call += calling[i]

    new_call = new_call.replace("%s", "{},", new_call.count("%s") - 1)

    for item in all_data:
        cursor.execute(f"INSERT INTO {fieldname} VALUES {tuple(item)};")
        db.commit()
    time.sleep(3)
    print("Done!")
    time.sleep(1)
    print("Now You can access this table in the database")
    print()
    sql_runner()

while True:
    if t == False:
        UserChoice = input("Please enter your Choice (1) CSV to SQL, (2) SQL writer (quit() to exit the program)\n>> ")
        if UserChoice == "quit()":
            exit()
        elif UserChoice == "1":
            print("Make sure that your csv file is in the same directory as app.py ")
            time.sleep(3)
            print()
            file = input("Enter the File Name \n>> ")
            all_data, fields, filename = csvtolist(file)
            sql_writer(filename, all_data, fields)
        elif UserChoice == "2":
            t = True
            sql_runner()
        else:
            print("Invalid Input")
    else:
        pass

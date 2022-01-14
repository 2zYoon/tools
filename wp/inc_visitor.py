# Increases the number of visitors provided by WP statistics
# required
#   - mysqlclient

import sys
import os
import datetime
import MySQLdb as mysql

HOWTOUSE = \
'''\
python(3) <COUNT> <CONFIG> <DB_USERNAME> <DB_PASSWORD>
    <COUNT>         Count to increase (integer)
    <CONFIG>        Path of config file
    <DB_USERNAME>   Username of DB
    <DB_PASSWORD>   Password of DB
'''

def check_argv(argv):
    if len(argv) < 5:
        print("ERROR: Too few arguments")
        print(HOWTOUSE)
        return 1

    if not argv[1].isdigit():
        print("ERROR: Invalid argument(COUNT)")
        print(HOWTOUSE)
        return 1

    if not os.path.isfile(argv[2]):
        print("ERROR: No such file")
        print(HOWTOUSE)
        return 1
    
    return 0

def main(argv):
    # argv check
    if check_argv(argv):
        return

    # configuration

    ADDR = ""
    PORT = ""
    DB_NAME = ""
    TABLE_NAME = ""   
    INSERT_TODAY = ""

    with open(argv[2]) as f:
        config = list(map(lambda s: s.strip(), f.readlines()))
        for i in config:
            c = i.split(' ')
            if c[0] == "ADDR:PORT":
                ADDR, PORT = c[1].split(":")
            elif c[0] == "DB_NAME":
                DB_NAME = c[1]
            elif c[0] == "TABLE_NAME":
                TABLE_NAME = c[1]
            elif c[0] == "INSERT_TODAY":
                INSERT_TODAY = c[1]

    if ADDR == "":
        print("INFO: No ADDR is provided, set to default (localhost)")
        ADDR = "localhost"
    if PORT == "":
        print("INFO: No PORT is provided, set to default (3306)")
        PORT = "3306"
    if DB_NAME == "":
        print("INFO: No DB_NAME is provided, set to default (wordpress)")
        DB_NAME = "wordpress"
    if TABLE_NAME == "":
        print("INFO: No TABLE_NAME is provided, set to default (wp_statistics_visitor)")
        TABLE_NAME = "wp_statistics_visitor"
    if INSERT_TODAY == "":
        print("INFO: No INSERT_TODAY is provided, set to default (yes)")
        INSERT_TODAY = "yes"
    if INSERT_TODAY != "yes" and INSERT_TODAY != "no":
        print("INFO: Invalid INSERT_TODAY is provided, set to default (yes)")
        INSERT_TODAY = "yes"

    print("CONFIGURATION:\n\tADDR:PORT   {}:{}\n\tDB_NAME     {}\n\tTABLE_NAME  {}\n\tINSERT_TODAY  {}".format(ADDR, PORT, DB_NAME, TABLE_NAME, INSERT_TODAY))

    # DB connection
    try:
        db = mysql.connect(host=ADDR,
                    port=int(PORT),
                    user=argv[3],
                    passwd=argv[4],
                    db=DB_NAME,
                    charset="utf8")
        cursor = db.cursor()
        print("INFO: Connected to DB successfully")

    except mysql._exceptions.OperationalError:
        print("ERROR: DB connection failed")
        print("Try to check configuration or username/password")
    
    # use current timestamp to avoid record duplication
    now = str(datetime.datetime.now().timestamp())

    # insert records
    try:
        for i in range(int(argv[1])):
            cmd = '''INSERT INTO `{}` (`ID`, `last_counter`, `referred`, `agent`, `ip`, `user_id`) VALUES (NULL, '{}', 'localhost', '{}', '127.0.0.1', 0)'''.format(
                    TABLE_NAME,
                    datetime.datetime.now().strftime("%Y-%m-%d") if INSERT_TODAY == "yes" else "2000-01-01",
                    now + "_" + str(i)
                )
            cursor.execute(cmd)

        db.commit()
        print("INFO: {} items inserted successfully".format(argv[1]))

    except:
        db.rollback()
        print("ERROR: Insertion failed, changes are rolled back")

    

if __name__ == "__main__":
    main(sys.argv)
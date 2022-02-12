# DB access version

import sys
import yaml
import MySQLdb as mysql

config = dict()
with open("dbconfig.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
db = mysql.connect(host=config['DB']['HOST'],
                port=config['DB']['PORT'],
                user=config['DB']['USER'],
                passwd=config['DB']['PASSWD'],
                db=config['DB']['NAME'],
                charset="utf8")
cursor = db.cursor()


while 1:
    # 0: cat
    # 1: type
    # 2: subtype
    mode = input("> ").split(" ")


    with open("input.txt", "r") as f:
        items = f.readlines()
        for i in items:
            name = i[:i.find("(★")].strip()
            score = i.count("★")
            comment = i[i.find("★)")+2:].strip()

            query = "insert into eat values ('{}', '{}', '{}', '{}', {}, '{}', NULL)".format(
                mode[0],
                mode[1],
                mode[2],
                name,
                score,
                comment
            )
            cursor.execute(query)
        db.commit()        
         
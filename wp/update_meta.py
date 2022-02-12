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

cursor.execute("select distinct cat, type, subtype from eat")
a = cursor.fetchall()

for i in a:
    cursor.execute("insert ignore into eat_meta values (NULL, '{}', '{}', '{}', NULL)".format(i[0], i[1], i[2], i[0], i[1], i[2]))
db.commit()
print("done.")
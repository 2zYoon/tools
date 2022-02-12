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

target_table = sys.argv[1]
target_col = sys.argv[2]
target_id = sys.argv[3]
target_string = sys.argv[4]
target_string_toset = sys.argv[5]

cursor.execute("select {}, {} from eat".format(target_col, target_id))
a = cursor.fetchall()

update = []
for i in a:
    if i[0].find(target_string) != -1:
        update.append([i[0].replace(target_string, target_string_toset), i[1]])

for i in update:
    q = "update eat set {} = '{}' where {} = {}".format(
        target_col,
        i[0],
        target_id,
        i[1])
    cursor.execute(q)
db.commit()

print("done. Updated {} item(s).".format(len(update)))
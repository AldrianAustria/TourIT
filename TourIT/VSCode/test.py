import pymysql

with open("loc.txt") as file:
    value = file.readlines()

con = pymysql.connect(host="192.168.1.4", user="root", passwd="", database="tourit")
cursor = con.cursor()

query = "UPDATE location SET `loc`=%s WHERE `id`=1"

cursor.execute(query, (value,))
con.commit()

cursor.close()
con.close()
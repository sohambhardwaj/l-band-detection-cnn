import pymysql
connection = pymysql.connect(host='localhost', user = 'root', db='db')
cursor = connection.cursor()
cursor.execute("desc test")
query=cursor.fetchall()
print(query)
connection.commit()
connection.close
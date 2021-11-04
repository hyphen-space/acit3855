import mysql.connector

db_conn = mysql.connector.connect(host="kafka3855.westus2.cloudapp.azure.com", user="root", password="password", database="events")

db_cursor = db_conn.cursor()
db_cursor.execute('''
                  DROP TABLE ticket_purchase, music_event
                  ''')

db_conn.commit()
db_conn.close()
import mysql.connector

db_conn = mysql.connector.connect(host="kafka3855.westus2.cloudapp.azure.com", user="root", password="password", database="events")

db_cursor = db_conn.cursor()

db_cursor.execute('''
        CREATE TABLE ticket_purchase
        (id INT NOT NULL AUTO_INCREMENT,
        purchaser VARCHAR(250) NOT NULL,
        eventDate VARCHAR(100) NOT NULL,
        seat VARCHAR(100) NOT NULL,
        price FLOAT(2) NOT NULL,
        numTickets INTEGER NOT NULL,
        date_created VARCHAR(100) NOT NULL,
        CONSTRAINT ticket_pk PRIMARY KEY (id))
    ''')

db_cursor.execute('''
          CREATE TABLE music_event
          (id INT NOT NULL AUTO_INCREMENT, 
           venue VARCHAR(250) NOT NULL,
           capacity INTEGER NOT NULL,
           eventDate VARCHAR(100) NOT NULL,
           headliner VARCHAR(250) NOT NULL,
           openingAct VARCHAR(250) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT event_pk PRIMARY KEY (id))
          ''')

db_conn.commit()
db_conn.close()

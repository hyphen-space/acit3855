import sqlite3

conn = sqlite3.connect('venue.sqlite')

c = conn.cursor()
c.execute('''
        CREATE TABLE ticket_purchase
        (id INTEGER PRIMARY KEY ASC,
        purchaser VARCHAR(250) NOT NULL,
        eventDate VARCHAR(100) NOT NULL,
        seat VARCHAR(100) NOT NULL,
        price FLOAT(2) NOT NULL,
        numTickets INTEGER NOT NULL,
        date_created VARCHAR(100) NOT NULL)
    ''')

c.execute('''
          CREATE TABLE music_event
          (id INTEGER PRIMARY KEY ASC, 
           venue VARCHAR(250) NOT NULL,
           capacity INTEGER NOT NULL,
           eventDate VARCHAR(100) NOT NULL,
           headliner VARCHAR(250) NOT NULL,
           openingAct VARCHAR(250) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()

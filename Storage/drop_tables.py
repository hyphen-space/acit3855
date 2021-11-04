import sqlite3

conn = sqlite3.connect('venue.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE ticket_purchase
          ''')
c.execute('''
          DROP TABLE music_event
          ''')


conn.commit()
conn.close()

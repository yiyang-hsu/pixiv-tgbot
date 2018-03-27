# import sqlite3

# conn = sqlite3.connect('tgbzs.db')

# c = conn.cursor()
# c.execute('''CREATE TABLE USERINFO
#        (USERID TEXT PRIMARY KEY    NOT NULL,
#        ALIAS           TEXT    NOT NULL,
#        FIRSTNAME           TEXT    NOT NULL,
#        LASTNAME           TEXT    NOT NULL,
#        INDEX          INT     NOT NULL);
#        CREATE TABLE IMAGES
#        (ID TEXT PRIMARY KEY    NOT NULL,
#        NAME           TEXT    NOT NULL,
#        LINK           TEXT    NOT NULL,
#        URL           TEXT    NOT NULL);''')
# conn.commit()
# conn.close()
import sqlite3

conn = sqlite3.connect('mydb.db')
c = conn.cursor()


def add_db_url(url_hash, url):
    try:
        c.execute("INSERT INTO hash_url (hash, url) VALUES ('{}','{}')".format(url_hash, url))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Already exists in the database")


def select_url_db(url_hash):
    c.execute("SELECT url FROM hash_url WHERE hash = '{}'".format(url_hash))
    url = c.fetchone()
    return url[0]


def select_hash_db():
    mass = []
    c.execute("SELECT hash FROM hash_url")
    u_hash = c.fetchone()
    while u_hash is not None:
        mass.append('<li>'+str(u_hash[0])+'</li>')
        u_hash = c.fetchone()
    return mass
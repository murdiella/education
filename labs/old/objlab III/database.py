import psycopg2 as pscg

cred = open("credentials.txt", 'r')
conn = pscg.connect(f"{cred.read()}")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS test (id serial PRIMARY KEY, num integer, data varchar);")
cur.execute('INSERT INTO test (num, data) VALUES (%s, %s)', (10, 'Aircraft'))
cur.execute('SELECT * FROM test;')
cur.fetchone()
conn.commit()
cur.close()

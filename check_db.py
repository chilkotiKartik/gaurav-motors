import os, sqlite3
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hms.db')
print(f'DB path: {db_path}')
print(f'Exists: {os.path.exists(db_path)}')
print(f'Size: {os.path.getsize(db_path)} bytes')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cursor.fetchall()]
print(f'Tables ({len(tables)}): {tables}')

if 'user' in tables:
    cursor.execute('SELECT * FROM user')
    rows = cursor.fetchall()
    print(f'\nUsers ({len(rows)}):')
    for r in rows:
        print(f'  id={r[0]}, username={r[1]}, email={r[2]}, role={r[4]}')
else:
    print('NO user table!')

conn.close()

import sqlite3 as sq
import matplotlib.pyplot as plt
import numpy as np

database_name = "table_2022_12_25_13_55_28"

y = []
x = []

db = sq.connect('../state.db')
cursor = db.cursor()
cursor.execute(f'SELECT * FROM {database_name}')
rows = cursor.fetchall()
initial_time = rows[0][4]
print(rows)
for row in rows:
    y.append(row[1])
    x.append(row[4]-initial_time)

plt.plot(x, y)
plt.xlabel("time (s)")
plt.ylabel("frequency (hz)")
plt.show()


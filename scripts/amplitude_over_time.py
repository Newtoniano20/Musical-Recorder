import sqlite3 as sq
import matplotlib.pyplot as plt
import numpy as np

database_name = "table_2022_12_25_13_51_10"

y = []
x = []

db = sq.connect('../state.db')
cursor = db.cursor()
cursor.execute(f'SELECT * FROM {database_name}')
rows = cursor.fetchall()
initial_time = rows[0][4]
for row in rows:
    y.append(row[2])
    x.append(row[4]-initial_time)

plt.plot(x, y)
plt.xlabel("time (s)")
plt.ylabel("amplitude (dB)")
plt.show()


import numpy as np
from scamp import *
import numpy
import time
import sqlite3 as sq
import json

s = Session()
violin = s.new_part('violin')
midi_numbers = np.arange(12, 112)

table_name = "table_2022_12_26_20_30_43"
db = sq.connect('../state.db')
cursor = db.cursor()
cursor.execute(f'SELECT * FROM {table_name}')
rows = cursor.fetchall()
initial_time = rows[0][4]
print(rows)
with open('../src/notes.json') as f:
    notes = json.load(f)
    freq = []
    for key, value in notes.items():
        freq.append(float(key))

print(freq)
prev = initial_time-1
_id = 0
for row in rows:
    _id += 1
    last_freq = 0
    next_freq = freq[1]
    for index, frequency in enumerate(freq):
        upper = (next_freq + frequency) / 2
        bottom = (last_freq + frequency) / 2
        if upper > row[1] > bottom:
            print(f"{_id}: Playing note {midi_numbers[index]} with a frequency: {row[1]}, which was interpreted as a {frequency}")
            violin.play_note(midi_numbers[index], 0.8, row[4]-prev)
            break
        elif index < (len(freq)-1):
            last_freq = frequency
            next_freq = freq[index+2]
    prev = row[4]

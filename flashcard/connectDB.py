import csv
import sqlite3

# kết nối đến cơ sở dữ liệu SQLite
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# tạo bảng nếu chưa tồn tại
cursor.execute('''CREATE TABLE IF NOT EXISTS study_card 
                (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                 word TEXT, 
                 flash_card_id INTEGER,
                 meaning TEXT)''')

flashcard_id = 100
# đọc dữ liệu từ tệp CSV
with open('data/data2/test.txt', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # bỏ qua hàng tiêu đề
    for row in reader:
        # chèn dữ liệu vào bảng SQLite
        cursor.execute('INSERT INTO study_card (word, flash_card_id, meaning) VALUES (?, ?, ?)',
                       (row[0], flashcard_id, row[1]))

# lưu các thay đổi vào cơ sở dữ liệu
conn.commit()

# đóng kết nối với cơ sở dữ liệu
conn.close()

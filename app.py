import sqlite3
import os

# إنشاء قاعدة البيانات
conn = sqlite3.connect('Project_607_DB.sqlite')
cursor = conn.cursor()

# 1. جدول التقارير اليومية (إضافة 103 تقارير تجريبية لتعود اللوحة للعمل)
cursor.execute('''CREATE TABLE IF NOT EXISTS Daily_Reports (Report_No INTEGER PRIMARY KEY, Date TEXT, Activities TEXT, Challenges TEXT)''')
for i in range(1, 104):
    cursor.execute("INSERT OR IGNORE INTO Daily_Reports VALUES (?, ?, ?, ?)", (i, '2026-11-16', f'أعمال اليوم {i}', 'لا توجد'))

# 2. جدول المراحل المالية
cursor.execute('''CREATE TABLE IF NOT EXISTS Payment_Phases (Phase_No INTEGER PRIMARY KEY, Phase_Date TEXT, Gross_Amount REAL, Advance_Deduction REAL, Retention_Deduction REAL, Net_Amount REAL, Status TEXT)''')
phases_data = [
    (1, '2026-09-30', 170000000.0, 20000000.0, 13376000.0, 140182991.21, 'Paid'),
    (2, '2026-10-30', 0.0, 0.0, 0.0, 0.0, 'Pending'),
    (6, '2027-02-30', 180000000.0, 0.0, 14000000.0, 157491948.96, 'Pending')
]
cursor.executemany('INSERT OR IGNORE INTO Payment_Phases VALUES (?, ?, ?, ?, ?, ?, ?)', phases_data)

# 3. جدول خريطة الحوائط
cursor.execute('''CREATE TABLE IF NOT EXISTS Wall_Execution_Sequence (Exec_Sequence INTEGER PRIMARY KEY, Wall_Name TEXT, Direction TEXT, Current_Status TEXT)''')
walls_data = [
    (1, 'الحائط 2', 'الجنوب', 'مكتمل'), (2, 'الحائط 3', 'جنوب الوسط', 'مكتمل - معالجة تعشيش'),
    (3, 'الحائط 5', 'الوسط', 'قيد التنفيذ'), (4, 'الحائط 4', 'شمال الوسط', 'القسم الأول مكتمل'),
    (5, 'الحائط 1', 'الشمال', 'مكتمل')
]
cursor.executemany('INSERT OR IGNORE INTO Wall_Execution_Sequence VALUES (?, ?, ?, ?)', walls_data)

# 4. جدول الكميات (BOQ)
cursor.execute('''CREATE TABLE IF NOT EXISTS BOQ_Items (Item_No TEXT PRIMARY KEY, Description TEXT, Unit TEXT, Total_Qty REAL, Executed_Qty REAL, Remaining_Qty REAL)''')
boq_data = [
    ('104', 'أعمال الحفر', 'م³', 3750.0, 443.0, 3307.0), ('404', 'الحوائط', 'م³', 83.0, 0.0, 83.0),
    ('409', 'حديد التسليح', 'طن', 100.0, 65.0, 35.0)
]
cursor.executemany('INSERT OR IGNORE INTO BOQ_Items VALUES (?, ?, ?, ?, ?, ?)', boq_data)

conn.commit()
conn.close()
print("✅ تم إنشاء قاعدة البيانات الشاملة (103 تقارير + الجداول المالية) بنجاح!")

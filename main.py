from pathlib import Path

from data_loader import load_school_data

school = load_school_data(Path("data"))

print("Всього учнів:", school.total_students)
boys, girls = school.gender_percent()
print(f"Хлопці: {boys:.1f}%  Дівчата: {girls:.1f}%")
print(f"Середня кількість учнів у класі: {school.average_class_size:.1f}")
big = school.largest_class()
small = school.smallest_class()
print(f"Максимум: {big.student_count} у класі {big.name}")
print(f"Мінімум: {small.student_count} у класі {small.name}")
# Streamlit-застосунок: статистика та графіки школи (Сценарій 1)
from pathlib import Path

import matplotlib.pyplot as plt
import streamlit as st

from data_loader import load_school_data
from models.school import MAX_GRADE, School

# шлях до папки data відносно цього файлу
DATA_DIR = Path(__file__).parent / "data"


def show_statistics(school: School) -> None:
    # статистика, пункт 2
    col1, col2, col3 = st.columns(3)  # три колонки поруч
    boys, girls = school.gender_percent()
    col1.metric("Всього учнів", school.total_students)
    col2.metric("Хлопці", f"{boys:.1f}%")
    col3.metric("Дівчата", f"{girls:.1f}%")

    st.metric("Середня кількість учнів у класі", f"{school.average_class_size:.1f}")

    biggest = school.largest_class()
    smallest = school.smallest_class()
    st.write(f"**Максимум:** {biggest.student_count} учнів у класі {biggest.name}")
    st.write(f"**Мінімум:** {smallest.student_count} учнів у класі {smallest.name}")


def show_charts(school: School) -> None:
    # пункт 3, графіки

    # 3а. стовпчиковий графік: учні по паралелях
    st.subheader("Кількість учнів по паралелях")
    by_grade = school.students_by_grade()
    fig, ax = plt.subplots()  # fig = "аркуш", ax = "сам графік на аркуші"
    ax.bar(list(by_grade.keys()), list(by_grade.values()))  # (позиції по X, висоти стовпчиків)
    ax.set_xlabel("Паралель")
    ax.set_ylabel("Кількість учнів")
    ax.set_xticks(list(by_grade.keys()))  # показати всі числа 1..11 на осі X
    st.pyplot(fig)  # вивести графік на сторінку Streamlit

    # 3б. стовпчиковий графік: середня кількість учнів по вертикалях
    st.subheader("Середня кількість учнів у класі по вертикалях")
    by_letter = school.average_size_by_letter()
    fig, ax = plt.subplots()
    ax.bar(list(by_letter.keys()), list(by_letter.values()))
    ax.set_xlabel("Вертикаль")
    ax.set_ylabel("Середня кількість учнів")
    st.pyplot(fig)

    # 3в. лінійний графік: кількість учнів за роком народження
    st.subheader("Кількість учнів за роком народження")
    by_year = school.students_by_birth_year()
    fig, ax = plt.subplots()
    ax.plot(list(by_year.keys()), list(by_year.values()), marker="o")  # лінія з точками
    ax.set_xlabel("Рік народження")
    ax.set_ylabel("Кількість учнів")
    ax.set_xticks(list(by_year.keys()))
    st.pyplot(fig)

    # 3г. scatter: середня оцінка кожного класу
    st.subheader("Середня оцінка учнів по класах")
    sorted_classes = school.classes_sorted()
    names = [c.name for c in sorted_classes]  # підписи по X: 1А, 1Б, 2А...
    grades = [c.average_grade for c in sorted_classes]  # значення по Y
    fig, ax = plt.subplots(figsize=(10, 4))  # ширший графік, бо підписів багато
    ax.scatter(names, grades)  # scatter = окремі точки без ліній
    ax.set_xlabel("Клас")
    ax.set_ylabel("Середня оцінка")
    plt.setp(ax.get_xticklabels(), rotation=90)  # повернути підписи, щоб не накладались
    st.pyplot(fig)


def show_promotion() -> None:
    # пункти 4-5: переведення на рік вперед і перевірка

    # завантажуємо свіжу школу, щоб не змінювати ту, що показана вище
    school = load_school_data(DATA_DIR)

    # запам'ятовуємо стан до переведення
    old_classes = school.classes
    old_names = [c.name for c in old_classes]
    old_total = school.total_students
    graduated = [c for c in old_classes if c.grade == MAX_GRADE]  # випускні класи

    school.promote_all()  # саме переведення

    # пункт 5, статистика після переведення
    st.subheader("Статистика після переведення")
    show_statistics(school)

    # таблиця: як змінилась назва кожного класу
    st.subheader("Як змінилися класи")
    rows = [
        {"Було": name, "Стало": c.name if c in school.classes else "закінчив школу"}
        for name, c in zip(old_names, old_classes)
    ]
    st.table(rows)

    # перевірка коректності
    st.subheader("Перевірка коректності")
    graduated_students = sum(c.student_count for c in graduated)
    grades_after = [c.grade for c in school.classes]

    checks = {
        "Випускні класи зникли, учнів стало менше рівно на їх кількість":
            school.total_students == old_total - graduated_students,
        "Кількість класів зменшилась на кількість випускних":
            len(school.classes) == len(old_classes) - len(graduated),
        "1 класу більше немає": 1 not in grades_after,
    }
    for description, passed in checks.items():
        if passed:
            st.success(description)
        else:
            st.error(description)


st.title("Статистика школи")

school_now = load_school_data(DATA_DIR)

st.header("Загальна інформація")
show_statistics(school_now)

st.header("Графіки")
show_charts(school_now)

st.header("Переведення на рік вперед")
if st.checkbox("Перевести всі класи на рік вперед"):
    show_promotion()
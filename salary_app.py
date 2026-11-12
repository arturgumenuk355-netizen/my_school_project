# режим командного рядка: розрахунок зарплат працівників школи (Сценарій 2)
import csv
from pathlib import Path

from data_loader import load_school_data
from models.employees import Director, Guard, Teacher
from models.school import School

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_FILE = DATA_DIR / "salaries.csv"  # сюди збережено таблицю

# базові ставки
DIRECTOR_RATE = 15000
TEACHER_RATE = 12000
GUARD_RATE = 11000


def add_employees(school: School) -> None:
    school.add_employee(Director("Панько", "Світлана", "Олексіївна", DIRECTOR_RATE,
                                 teaching_experience=25, management_experience=10))
    school.add_employee(Teacher("Козацька", "Олена", "Вадимівна", TEACHER_RATE,
                                teaching_experience=12))
    school.add_employee(Teacher("Тиндик", "Станіслав", "Іванович", TEACHER_RATE,
                                teaching_experience=20))
    school.add_employee(Teacher("Лубенко", "Лілія", "Сергіївна", TEACHER_RATE,
                                teaching_experience=5))
    school.add_employee(Guard("Бондар", "Олексій", "Іванович", GUARD_RATE,
                              total_experience=8))


def print_table(rows: list[dict[str, str | float]]) -> None:
    # вивід таблиці в консоль
    print(f"{'ПІБ':<32}{'Посада':<12}{'Ставка':>10}{'Зарплата':>12}")
    print("-" * 66)
    for row in rows:
        print(f"{row['ПІБ']:<32}{row['Посада']:<12}{row['Базова ставка']:>10.2f}{row['Зарплата']:>12.2f}")


def save_to_csv(rows: list[dict[str, str | float]], path: Path) -> None:
    # збереження таблиці у CSV
    # utf-8-sig для нормальної робити Excel з укр. літерами
    with open(path, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))  # заголовки з ключів словника
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    # той же об'єкт School, що й у Сценарії 1
    school = load_school_data(DATA_DIR)
    add_employees(school)

    rows = school.salary_table()  # розрахунок зарплат
    print_table(rows)
    save_to_csv(rows, OUTPUT_FILE)
    print(f"\nТаблицю збережено у файл: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
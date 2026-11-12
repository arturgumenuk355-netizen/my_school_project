import csv
from pathlib import Path
from models.school import School
from models.school_class import SchoolClass
from models.student import Student

def load_classes(path: Path) -> dict[tuple[int, str], SchoolClass]:
    classes : dict[tuple[int, str], SchoolClass] = {}

    with open(path, encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            grade = int(row["grade"])
            letter = row["letter"].strip()
            classes[(grade, letter)] = SchoolClass(grade, letter)

    return classes

def load_students(path: Path, classes: dict[tuple[int, str], SchoolClass]) -> None:
    with open(path, encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = (int(row["grade"]), row["letter"].strip())

            student = Student(
                last_name=row["last_name"].strip(),
                first_name=row["first_name"].strip(),
                middle_name=row["middle_name"].strip(),
                birth_year=int(row["birth_year"]),
                gender=row["gender"].strip().lower(),
                avg_grade=float(row["avg_grade"]),
            )
            classes[key] .add_student(student) #клас знаходиться за ключем

def load_school_data(data_dir: Path) -> School:
    classes = load_classes(data_dir / "classes.csv")
    load_students(data_dir / "students.csv", classes)
    return School("Моя школа", list(classes.values()))

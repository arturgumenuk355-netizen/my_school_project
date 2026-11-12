from models.employees import Employee
from models.school_class import SchoolClass

MALE = "ч"
FEMALE = "ж"

MAX_GRADE = 11  # остання паралель у школі


class School:
    # статистичні дані

    def __init__(self, name: str, classes: list[SchoolClass]) -> None:
        self.name: str = name
        self.classes: list[SchoolClass] = classes
        self.employees: list[Employee] = []  # працівники (Сценарій 2)

    @property
    def total_students(self) -> int:
        # к-сть учнів у школі
        return sum(c.student_count for c in self.classes)

    def gender_percent(self) -> tuple[float, float]:
        # % хлопів і дівчат
        total = self.total_students
        if total == 0:  # захист від ділення на нуль
            return 0.0, 0.0
        boys = sum(1 for c in self.classes for s in c.students if s.gender == MALE)
        girls = sum(1 for c in self.classes for s in c.students if s.gender == FEMALE)
        return boys / total * 100, girls / total * 100

    @property
    def average_class_size(self) -> float:
        # avg к-сть учнів у класі
        if not self.classes:
            return 0.0
        return self.total_students / len(self.classes)

    def largest_class(self) -> SchoolClass:
        # клас з макс. к-тю учнів
        return max(self.classes, key=lambda c: c.student_count)

    def smallest_class(self) -> SchoolClass:
        # клас з мін. к-тю учнів
        return min(self.classes, key=lambda c: c.student_count)

    # 3. дані для графіків

    def students_by_grade(self) -> dict[int, int]:
        # к-ть по паралелях
        result: dict[int, int] = {}
        for c in self.classes:
            result[c.grade] = result.get(c.grade, 0) + c.student_count
        return dict(sorted(result.items()))

    def average_size_by_letter(self) -> dict[str, float]:
        # к-ть по вертикалях
        sizes: dict[str, list[int]] = {}
        for c in self.classes:
            sizes.setdefault(c.letter, []).append(c.student_count)
        return {letter: sum(v) / len(v) for letter, v in sorted(sizes.items())}

    def students_by_birth_year(self) -> dict[int, int]:
        # к-ть за роком народження
        result: dict[int, int] = {}
        for c in self.classes:
            for s in c.students:
                result[s.birth_year] = result.get(s.birth_year, 0) + 1
        return dict(sorted(result.items()))

    def classes_sorted(self) -> list[SchoolClass]:
        # класи впорядковані за числом і буквою
        return sorted(self.classes, key=lambda c: (c.grade, c.letter))

    # 4. переведення на рік вперед

    def promote_all(self) -> None:
        # спочатку прибрано 11 клас, потім іншим +1
        # не можна щоб 11 клас став би 12-м
        self.classes = [c for c in self.classes if c.grade < MAX_GRADE]
        for school_class in self.classes:
            school_class.promote()  # метод класу: grade += 1

    # 5. працівники та зарплати (Сценарій 2)

    def add_employee(self, employee: Employee) -> None:
        # додати працівника до школи
        self.employees.append(employee)

    def salary_table(self) -> list[dict[str, str | float]]:
        # таблиця зарплат: один рядок (словник) на працівника
        # calculate_salary() у кожного об'єкта своя (поліморфізм), тут просто викликаємо
        return [
            {
                "ПІБ": e.full_name,
                "Посада": e.position,
                "Базова ставка": e.base_salary,
                "Зарплата": round(e.calculate_salary(), 2),
            }
            for e in self.employees
        ]
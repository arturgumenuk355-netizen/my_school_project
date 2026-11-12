from models.person import Person


class Student(Person):  # Student наслідує Person (ПІБ уже є в батька)
    def __init__(self,
                 last_name: str,
                 first_name: str,
                 middle_name: str,
                 birth_year: int,
                 gender: str,
                 avg_grade: float,
                 ) -> None:
        super().__init__(last_name, first_name, middle_name)  # передаємо ПІБ батьку
        self.birth_year = birth_year
        self.gender = gender
        self.avg_grade = avg_grade

    def __str__(self) -> str:  # вигляд об'єкта в print
        return f"{self.full_name} ({self.birth_year} {self.gender} {self.avg_grade})"



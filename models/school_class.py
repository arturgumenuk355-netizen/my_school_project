from models.student import Student

class SchoolClass:
    def __init__(self, grade: int, letter: str) -> None:
        self.grade = grade #паралелі (1,2,3...)
        self.letter = letter #вертикалі (A,Б,В)
        self.students: list[Student] = []

    @property
    def name(self) -> str:
        return f"{self.grade}{self.letter}"

    def add_student(self, student: Student) -> None:
        self.students.append(student)

    @property
    def student_count(self) -> int:
        return len(self.students)

    @property
    def average_grade(self) -> float:
        #avg оцінка класу
        if not self.students:
            return 0.0
        return sum(s.avg_grade for s in self.students) / len(self.students)

    def promote(self) -> None: #переведення на рік вперед
        self.grade += 1

    def __str__(self) -> str:
        return f" Клас {self.name}: {self.student_count} учнів"


from abc import ABC, abstractmethod

from models.person import Person

class Employee(Person, ABC):
    # клас працівника школи, наслідує ПІБ від Person

    position: str = "Працівник"  # назва посади у кожного своя

    def __init__(self,
                 last_name: str,
                 first_name: str,
                 middle_name: str,
                 base_salary: float,
                 ) -> None:
        super().__init__(last_name, first_name, middle_name)  # передаємо ПІБ батьку
        self.base_salary = base_salary  # базова ставка

    @abstractmethod
    def calculate_salary(self) -> float:
        # у кожної посади своя формула розрахунку зп
        ...

    def __str__(self) -> str:
        return f"{self.position}: {self.full_name}"


class Director(Employee):
    # директор ставка, педагогічний стаж і стаж керування
    position = "Директор"

    def __init__(self,
                 last_name: str,
                 first_name: str,
                 middle_name: str,
                 base_salary: float,
                 teaching_experience: int,
                 management_experience: int,
                 ) -> None:
        super().__init__(last_name, first_name, middle_name, base_salary)
        self.teaching_experience = teaching_experience  # педагогічний стаж, роки
        self.management_experience = management_experience  # стаж керування, роки

    def calculate_salary(self) -> float:
        # ставка * пед. стаж / 50 + стаж керування * 500
        return self.base_salary * self.teaching_experience / 50 + self.management_experience * 500


class Teacher(Employee):
    # вчитель ставка і педагогічний стаж
    position = "Вчитель"

    def __init__(self,
                 last_name: str,
                 first_name: str,
                 middle_name: str,
                 base_salary: float,
                 teaching_experience: int,
                 ) -> None:
        super().__init__(last_name, first_name, middle_name, base_salary)
        self.teaching_experience = teaching_experience  # педагогічний стаж, роки

    def calculate_salary(self) -> float:
        # ставка * пед. стаж / 30
        return self.base_salary * self.teaching_experience / 30


class Guard(Employee):
    # охоронець ставка і загальний досвід роботи
    position = "Охоронець"

    def __init__(self,
                 last_name: str,
                 first_name: str,
                 middle_name: str,
                 base_salary: float,
                 total_experience: int,
                 ) -> None:
        super().__init__(last_name, first_name, middle_name, base_salary)
        self.total_experience = total_experience  # загальний досвід, роки

    def calculate_salary(self) -> float:
        # ставка + загальний досвід * 250
        return self.base_salary + self.total_experience * 250
class Person:
   #базовий клас для всіх людей у школі

    def __init__(self, last_name: str, first_name: str, middle_name: str) -> None:
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name

    @property
    def full_name(self) -> str:  # ПІБ
        return f"{self.last_name} {self.first_name} {self.middle_name}"
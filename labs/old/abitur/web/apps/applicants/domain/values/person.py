from dataclasses import dataclass
from datetime import date


@dataclass
class Person:
    firstname: str
    lastname: str
    birthdate: date
    middlename: str = ""

    @property
    def fullname(self):
        if self.middlename:
            return f"{self.lastname} {self.firstname} {self.middlename}"
        else:
            return f"{self.lastname} {self.firstname}"

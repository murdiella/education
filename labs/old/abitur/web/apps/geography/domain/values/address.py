from dataclasses import dataclass


@dataclass
class Address:

    region: str = ""
    district: str = ""
    city: str = ""
    township: str = ""
    zipcode: str = ""
    street: str = ""
    house: str = ""
    building: str = ""
    apartment: str = ""

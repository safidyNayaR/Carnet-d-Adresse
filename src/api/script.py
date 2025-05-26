import re
import string
from pathlib import Path
from pprint import pprint

from tinydb import TinyDB, where

class User:

    DB = TinyDB(Path(__file__).resolve().parent/ "db.json", indent=4)

    def __init__(self, first_name, last_name, phone_number="", address=""):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address

    def __repr__(self):
        return f"User({self.first_name}, {self.last_name})"

    def __str__(self) -> str:
        return f"{self.full_name}\n{self.phone_number}\n{self.address}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def db_instance(self):
        return User.DB.get((where('first_name') == self.first_name) & (where('last_name') == self.last_name))
    
    def exists(self):
        return bool(self.db_instance)
    
    def delete(self) -> list[int]:
        if self.exists():
            return User.DB.remove(doc_ids=[self.db_instance.doc_id])

    def _checks(self):
        self._check_phone_number
        self._check_names

    def _check_phone_number(self):
        phone_number = re.sub(r"[+()\s]*", "", self.phone_number)
        if not phone_number.isdigit() or len(phone_number) < 10:
            raise ValueError(f"Numéro téléphone {self.phone_number} invalide.")

    def _check_names(self):
        characteres = string.punctuation + string.digits

        for char in self.first_name + self.last_name:
            if char in characteres:
                raise ValueError(f"Le nom {self.full_name} est invalide.")

    def save(self):
        User.DB.insert(self.__dict__)


def get_all_users():
    return [User(**user) for user in User.DB.all()]       


if __name__ == "__main__":
    Roche = User(first_name="Germain", last_name="Pires")
    print(Roche.delete())
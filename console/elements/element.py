from abc import ABC


class Element(ABC):
    def __init__(self, is_occupied=False, name=""):
        self.is_occupied = is_occupied
        self.name = name

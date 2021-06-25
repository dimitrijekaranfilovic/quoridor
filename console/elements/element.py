from abc import ABC


class Element(ABC):
    def __init__(self, is_occupied=False):
        self.is_occupied = is_occupied

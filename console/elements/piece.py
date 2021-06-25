from console.elements.element import Element


class Piece(Element):
    def __init__(self, is_occupied=False, name=""):
        super(Piece, self).__init__(is_occupied)
        self.name = name

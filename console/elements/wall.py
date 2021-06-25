from console.elements.element import Element


class Wall(Element):
    def __init__(self, is_occupied=False):
        super(Wall, self).__init__(is_occupied)

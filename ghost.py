from tile import Tile


class Ghost(Tile):

    def __init__(self, pos: tuple, image: str, groups) -> None:
        super().__init__(pos, image, groups)

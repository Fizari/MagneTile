from mt_tile import Tile_Movement


class History_Step:
    cluster = []
    neighbors_moves = []  # Tile_Movement list

    def __init__(self, cluster):
        self.cluster = cluster
        self.neighbors_moves = []

    def add_move(self, tile, dest):
        self.neighbors_moves.append(Tile_Movement(tile, dest))

    def add_moves(self, moves):
        self.neighbors_moves = self.neighbors_moves + moves


class History:
    steps = []

    def __init__(self):
        self.steps = []

    def get_current_step(self):
        if self.steps == []:
            return None
        else:
            return self.steps[-1]

    def undo_last_step(self):
        return self.steps.pop()

    def add_new_step(self, cluster):
        self.steps.append(History_Step(cluster))

    def add_tile_movements_to_current_step(self, moves):
        curr = self.get_current_step()
        if curr:
            self.get_current_step().add_moves(moves)

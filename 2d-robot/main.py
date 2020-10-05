import enum
from enum import Enum
from typing import Callable
from typing import Dict
from typing import List
from typing import Tuple

from graphics import GraphWin
from graphics import Point
from graphics import Polygon
from graphics import Rectangle
from graphics import Text


class Facing(Enum):
    LEFT = enum.auto()
    UP = enum.auto()
    RIGHT = enum.auto()
    DOWN = enum.auto()


class State:
    def __init__(self, win: GraphWin, grid_dim: Tuple[int, int],
                 start: Tuple[int, int], facing: Facing):
        grid_rows, grid_cols = grid_dim
        if grid_rows == 0 or grid_cols == 0:
            raise ValueError("grid must be at least 1x1")
        self.grid = [[0 for _ in range(grid_cols)] for _ in range(grid_rows)]
        self.grid[start[0]][start[1]] = 1

        self.win = win
        self.facing = facing

    def num_of_cols(self) -> int:
        '''
        Returns the number of columns in the grid
        '''
        return len(self.grid[0])  # count length of first row

    def num_of_rows(self) -> int:
        '''
        Returns the number of rows in the grid
        '''
        return len(self.grid)

    def direction(self) -> Facing:
        '''
        Returns "L" if the robot is facing left,
        "R" if the robot is facing right, "U" if the robot is facing up,
        and "D" if thr robot is facing down.
        '''
        return self.facing

    def robot_position(self) -> Tuple[int, int]:
        '''
        Returns the row and the column of the robot (in that order)
        '''
        for r, row in enumerate(self.grid):
            for c, col in enumerate(row):
                if col == 1:
                    pos = (r, c)
        return pos

    def robot_row(self) -> int:
        '''
        Returns the row of the robot (use robot_position() function)
        '''
        r, _ = self.robot_position()
        return r

    def robot_col(self) -> int:
        '''
        Returns the column of the robot (use robot_position() function)
        '''
        _, c = self.robot_position()
        return c

    def turn_right(self) -> Facing:
        '''
        Make the robot turn 90 degrees to the right by changing the variable
        facing
        '''
        switch = {Facing.LEFT: Facing.UP, Facing.UP: Facing.RIGHT,
                  Facing.RIGHT: Facing.DOWN, Facing.DOWN: Facing.LEFT}
        self.facing = switch[self.facing]
        return self.facing

    def turn_left(self) -> Facing:
        '''
        Make the robot turn left 90 degrees by changing the variable facing
        '''
        switch = {Facing.LEFT: Facing.DOWN, Facing.UP: Facing.LEFT,
                  Facing.RIGHT: Facing.UP, Facing.DOWN: Facing.RIGHT}
        self.facing = switch[self.facing]
        return self.facing

    def can_move_forward(self) -> bool:
        '''
        Returns true if the robot can move forward, and false if the way is
        blocked (no more spaces to move)
        '''
        nr, nc = self.robot_next_position()
        return (nr >= 0 and nr < self.num_of_rows() and
                nc >= 0 and nc < self.num_of_cols())

    def move_forward(self):
        '''
        Moves the robot forward in the direction he is facing.
        Prints "unable to move" if the way is blocked
        '''
        if not self.can_move_forward():
            print("unable to move")
        else:
            r, c = self.robot_position()
            nr, nc = self.robot_next_position()
            self.grid[r][c] = 0
            self.grid[nr][nc] = 1

    def robot_next_position(self) -> Tuple[int, int]:
        dr, dc = self.move_switch()[self.facing]
        r, c = self.robot_position()
        nr = r + dr
        nc = c + dc

        return (nr, nc)

    def move_switch(self):
        switch = {Facing.LEFT: (0, -1), Facing.UP: (-1, 0),
                  Facing.RIGHT: (0, 1), Facing.DOWN: (1, 0)}
        return switch

    def display_grid(self):
        '''
        Displays the current grid in the graphics window
        '''
        for r in range(self.num_of_rows()):
            for c in range(self.num_of_cols()):
                square = Rectangle(Point(20 * c, 20 * r),
                                   Point(20 * c + 20, 20 * r + 20))
                square.draw(self.win)
                square.setFill('white')
                if self.grid[r][c] == 1:
                    if self.facing == Facing.RIGHT:
                        robot = Polygon(Point(20 * c, 20 * r),
                                        Point(20 * c + 20, 20 * r + 10),
                                        Point(20 * c, 20 * r + 20))
                    elif self.facing == Facing.LEFT:
                        robot = Polygon(Point(20 * c + 20, 20 * r),
                                        Point(20 * c, 20 * r + 10),
                                        Point(20 * c + 20, 20 * r + 20))
                    elif self.facing == Facing.UP:
                        robot = Polygon(Point(20 * c, 20 * r + 20),
                                        Point(20 * c + 20, 20 * r + 20),
                                        Point(20 * c + 10, 20 * r))
                    elif self.facing == Facing.DOWN:
                        robot = Polygon(Point(20 * c, 20 * r),
                                        Point(20 * c + 20, 20 * r),
                                        Point(20 * c + 10, 20 * r + 20))
                    robot.draw(self.win)
                    robot.setFill('black')

    def close(self):
        self.win.close()


Keybindings = Dict[List[str], Tuple[Callable[[State], bool], str]]


def setup(keybinds: Keybindings):
    '''
    Initializes the graphics and the list representing the grid
    '''
    rows, cols = (4, 9)
    start = (0, 4)

    # figure out reasonable height and width of the graphics window
    grid_height = 0
    row_scale = rows * 20
    if row_scale < 350:
        grid_height = 350
    else:
        grid_height = row_scale

    grid_width = 0
    col_scale = cols * 20
    if col_scale < 350:
        grid_width = 350
    else:
        grid_width = col_scale

    # set up initial window
    win = GraphWin("Robot", grid_width, grid_height, autoflush=False)
    win.setBackground("green")

    help_str = '\n'.join(map(lambda item: 'Press {keys} to {desc}'.format(
        keys=', '.join(item[0]), desc=item[1][1]), keybinds.items()))
    help_text = Text(Point(win.getWidth()/2, win.getHeight()/5*4), help_str)
    help_text.setFill("white")
    help_text.draw(win)

    return State(win, (rows, cols), start, Facing.RIGHT)


def keybind_close(state: State) -> bool:
    state.win.close()
    return True


def keybind_turn_right(state: State) -> bool:
    state.turn_right()
    return False


def keybind_turn_left(state: State) -> bool:
    state.turn_left()
    return False


def keybind_move_forward(state: State) -> bool:
    state.move_forward()
    return False


def main():
    keybinds = {('q'): (keybind_close, 'stop'),
                ('l', 'Right'): (keybind_turn_right, 'turn right 90 degrees'),
                ('h', 'Left'): (keybind_turn_left, 'turn left 90 degrees'),
                ('k', 'Up'): (keybind_move_forward, 'move forward 1 space')}
    state = setup(keybinds)

    '''
    The driver of the program. Takes user input through keys
    and manipulates the robot appropriately.
    '''
    end = False
    while not end:
        state.display_grid()
        key = state.win.getKey()
        for k, v in keybinds.items():
            if key in k:
                end = v[0](state)
                break


if __name__ == '__main__':
    main()

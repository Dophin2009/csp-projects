from enum import Enum
from typing import List

from graphics import GraphWin
from graphics import Point
from graphics import Polygon
from graphics import Rectangle
from graphics import Text


class Facing(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class State:
    def __init__(self, win: GraphWin, grid: List[List[int]], facing: Facing):
        self.win = win
        self.grid = grid
        self.facing = facing

    def getNumberOfColumns(self) -> int:
        '''
        Returns the number of columns in the grid
        '''
        return len(self.grid[0])  # count length of first row

    def getNumberOfRows(self) -> int:
        '''
        Returns the number of rows in the grid
        '''
        return len(self.grid)

    def getDirection(self) -> Facing:
        '''
        Returns "L" if the robot is facing left,
        "R" if the robot is facing right, "U" if the robot is facing up,
        and "D" if thr robot is facing down.
        '''
        return self.facing

    def getRobotPosition(self):
        '''
        Returns the row and the column of the robot (in that order)
        '''

        return

    def getRobotRow(self):
        '''
        Returns the row of the robot (use getRobotPosition() function)
        '''

        return

    def getRobotColumn(self):
        '''
        Returns the column of the robot (use getRobotPosition() function)
        '''
        return

    def turnRight(self):
        '''
        Make the robot turn 90 degrees to the right by changing the variable
        facing
        '''
        pass  # delete this line

    def turnLeft(self):
        '''
        Make the robot turn left 90 degrees by changing the variable facing
        '''
        pass  # delete this line

    def canMoveForward(self):
        '''
        Returns true if the robot can move forward, and false if the way is
        blocked (no more spaces to move)
        '''

        return

    def moveForward(self):
        '''
        Moves the robot forward in the direction he is facing.
        Prints "unable to move" if the way is blocked
        '''
        print()

    def displayGridSquares(self):
        '''
        Displays the current grid in the graphics window
        '''
        for r in range(self.getNumberOfRows()):
            for c in range(self.getNumberOfColumns()):
                square = Rectangle(Point(20*c, 20*r),
                                   Point(20*c+20, 20*r+20)).draw(self.win)
                square.setFill('white')
                if self.grid[r][c] == 1:
                    # draw robot
                    if self.facing == 'R':
                        robot = Polygon(Point(), Point(),
                                        Point()).draw(self.win)
                        robot.setFill('black')
                    elif self.facing == 'L':
                        robot = Polygon(Point(), Point(),
                                        Point()).draw(self.win)
                        robot.setFill('black')
                    elif self.facing == 'U':
                        robot = Polygon(Point(), Point(),
                                        Point()).draw(self.win)
                        robot.setFill('black')
                    elif self.facing == 'D':
                        robot = Polygon(Point(), Point(),
                                        Point()).draw(self.win)
                        robot.setFill('black')


def setup():
    '''
    Initializes the graphics and the list representing the grid
    '''

    # grid is a list of lists. Each list corresponds to a row of squares.
    grid = [[0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    facing = Facing.RIGHT

    # figure out reasonable height and width of the graphics window
    gridHeight = 0
    if len(grid) * 20 < 350:
        gridHeight = 350
    else:
        gridHeight = len(grid)*20

    gridWidth = 0
    if len(grid[0]) * 20 < 350:
        gridWidth = 350
    else:
        gridWidth = len(grid[0])*20

    # set up initial window
    win = GraphWin("Robot", gridWidth, gridHeight, autoflush=False)
    win.setBackground("green")
    directionText = Text(Point(win.getWidth()/2, win.getHeight()/5*4),
                         "Press right arrow or 'r' to turn right 90 degrees\n"
                         "Press left arrow or 'l' to turn left 90 degrees\n"
                         "Press up arrow or 'u' to move forward 1 space\n"
                         "Press 's' to stop")
    directionText.setFill("white")
    directionText.draw(win)

    return State(win, grid, facing)


def main():
    state = setup()

    '''
    The driver of the program. Takes user input through keys
    and manipulates the robot appropriately.
    '''
    end = False
    while not end:
        state.displayGridSquares()
        key = state.win.getKey()  # waits for user key press
        if key == 'q':  # if user presses 's' key, closes window
            end = True
            state.win.close()
        elif key == 'l' or key == "Right":
            state.turnRight()
        elif key == "h" or key == "Left":
            state.turnLeft()
        elif key == 'k' or key == "Up":
            state.moveForward()


if __name__ == '__main__':
    main()

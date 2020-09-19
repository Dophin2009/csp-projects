# For Loop Lab

1.  Create a new folder in your workspace called "For Loop Lab". Within
    it, create a new python file named "ForLoopExamples".

2.  Type the following lines of code in and run the code.

        import random
        for i in range(10):
           randNum = random.randint(0,9)
           print(randNum)

    a.  What is the output?

            2
            3
            6
            1
            7
            5
            2
            0
            4
            3

    b.  What is `randNum` in the above code and what is its purpose?

        `randNum` is a variable storing the integer returned by
        `random.randint`.

    c.  What does `random.randint(0, 9)` do?

        It returns a random integer between 0 and 9, inclusive.

    d.  Change the parameter of the `range()` function to 1, 5, and 20
        and run the code each time. Based on this output, what do you
        think the `range()` function does?

        It creates an interator of integers from 0 up to and excluding
        the value of the argument.

3.  The `for` loop in Python uses the range function and it iterates
    (perform a repeated function) over a certain number of values. Type
    the following code:

        for i in range(10):
            print(i)

    a.  What is the output?

            0
            1
            2
            3
            4
            5
            6
            7
            8
            9

    b.  What seems to be happening to the variable `i`?

        It is increased by 1 each iteration.

4.  Now change the range function code and compare the new outputs. Take
    notice of how the output changes when you change the parameter in
    the range() function.

        range(5)

        range(5, 10)

        range(0, 10, 3)

        range(-10, -100, -30)

    a.  What does the range function do with one, two, and three
        parameters, respectively (Try other values to confirm your
        theory)? Explain the role of each parameter (1st, 2nd and 3rd
        within the parentheses)

        With one argument, iteration starts from 0 up to and excluding
        the value of the argument. With two arguments, iteration starts
        from the value of the first argument up to and excluding the
        value of the second argument. With three arguments, the first
        two arguments serve the same functionality as when only two
        arguments are passed, and the third argument is the step size.

5.  A `for` loop can have many uses. Take some time to try to write code
    to do the following tasks. Copy and paste your code segment below
    each.

    a.  Print out all even numbers from 0 to 100 forwards then 100 to 0
        backwards:

            for i in range(0, 101, 2):
                print(i)
            for i in range(100, -1, -2):
                print(i)

    b.  Print out all odd numbers from 1 to 99 forwards then 99 to 1
        backwards:

            for i in range(1, 100, 2):
                print(i)
            for i in range(99, 0, -2):
                print(i)

    c.  Use a `for` loop inside of a `for` loop to print 5 rows of 5
        `*`'s (as shown below)':

            for i in range(5):
                for j in range(5):
                    print('*', end='')
                print()

    d.  Use a `for` loop inside of a `for` llop to modify the pattern
        from c:

            for i in range(5):
                for j in range(i + 1):
                    print('*', end = '')
                print()

6.  Create a new python file in the same folder called Shapes.py (like
    you did in step 1). Now we will be using a library called
    graphics.py. Download this file from the Unit 1 folder in Schoology.

7.  In `Shapes.py`, type the following:

        from graphics import *
        import random

        win = GraphWin("Shapes", 600, 600)
        win.setBackground(color_rgb(255, 0, 0))
        win.getMouse()

    Run your code. `GraphWin()` is a function that creates the window to
    be the given size 600x600 with the title "Shapes". `win` is a
    variable that is used to change the settings of the graphics window.
    `setBackground()` is a function that sets the background color.
    Change these numbers `(255, 0, 0)` around to see if you can get more
    colors. `getMouse()` is a function that pauses the graphics window
    until the user clicks the mouse. Without this line of code, the
    window will open and immediately close, since the program would end.

    a.  Can you think of something else that could keep the program from
        finishing? (Hint: we used it in our Nim game)

        An infinite loop.

8.  The graphics window is like a giant canvas on which we can draw
    shapes and colors. We tell the computer where to draw shapes through
    the use of a coordinate system. In most computer graphic
    applications, the origin is at the top left of the window with
    positive x to the right, and positive y down.

    Now we will add a circle object onto our canvas at the center of the
    window. Type the following code after `setBackground()` and
    **before** `getMouse()`:

        c1 = Circle(Point(300, 300), 10)
        c1.setFill("white")
        c1.setOutline("white")
        c1.draw(win)

    Change the "white" to different colors. Explore which colors are
    available and which are not.

    a.  What does `setFill()` do?

        It sets the fill color of the circle.

    b.  What does `setOutline()` do?

        It sets the color of the outline of the circle.

    c.  Change the numbers 300, 300. What changes about the circle?
        Change the number 10. What changes about the circle?

        The position and size of the circle change.

9.  Add the following lines of code below the `c1.draw(win)` command.

        for x in range(300):
            c1.move(1, 1)
            win.redraw()
         update(30)
         print(c1.getP1(), c1.getP2())

    a.  Try to modify the code to make the circle move in random
        directions.

    b.  Adjust the `update(30)` command. Change it to `update(1)` and
        `update(1000)`.

        The number of frames updated per second.

    c.  `c1` is the variable representing the circle. A circle in
        graphics is drawn using two points, the top left and bottom
        right points of a box. The circle is inscribed within the box.
        Try using if statements to make the object bounce off the
        boundaries. You can use the line of code `c1.getP1().getX()` to
        get the number representing the x coordinate and
        `c1.getP1.getY()` to get the number representing the y
        coordinate.

10. Try to recreate the following picture. When you are satisfied, copy
    and paste the main body of your code here:

        from graphics import (Circle, color_rgb, GraphWin, Point)

        size = 600
        win = GraphWin("Shapes", size, size)
        win.setBackground(color_rgb(255, 0, 0))

        for i in range(0, size + 1, 100):
            c = Circle(Point(i, size - i), 60)
            c.setFill("white")
            c.setOutline("black")
            c.draw(win)

        for i in range(0, size + 1, 60):
            c = Circle(Point(i, i), 30)
            c.setFill("green")
            c.setOutline("black")
            c.draw(win)

        win.getMouse()

11. Now, create your own picture. Try using for loops, the random
    function, and variables. Try to make things move around the screen
    also. Post your code here:

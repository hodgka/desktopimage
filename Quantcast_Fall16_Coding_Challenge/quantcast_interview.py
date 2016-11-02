'''
Quantcast Coding Challenge Solution - October 25, 2016
Alec Hodgkinson
Rensselaer Polytechnic Institute (RPI)

Coded in Python 2.7 according to the PEP8 Styleguide.
'''

import argparse
import sys
import re


ALPHABET = {k: i for i, k in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}
OPERATIONS = set(['+', '-', '/', '*'])


def parse_arguments():
    '''
    helper function to parse CLA's and remove them from global scope
    Returns:
        An ArgumentParser object
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("input_fname")
    parser.add_argument("output_fname", nargs="?")
    return parser.parse_args()


def parse_grid(fname):
    '''
    parse input file and populate a grid object
    Arguments:
        fname - name of the input file
    Returns:
        A fully populated grid object
    '''
    with open(fname, 'r') as f:
        data = f.read()
        lines = data.strip().split('\n')
        assert(len(lines) > 1)
        try:
            n, m = map(int, lines[0].split())
        except:
            raise Exception("Invalid input file.\
                            Must have grid size in first line.")

        lines = lines[1:]
        try:
            grid = Grid(lines, m, n)
        except:
            return None
    return grid


def label_to_xy(label):
    '''
    Helper function to get position from grid label
    i.e. "C152" -> (2, 151)
    Arguments:
        label - grid label for a cell
    Returns:
        - A tuple with the the coordinates of the cell if it is a valid label
          or a tuple (-1, -1) i.e. not in the grid
    '''
    # needed by both cell and grid classes, so I made it into its own function
    # checks if the first character is a letter, and the rest are numbers
    regex = re.compile(r"[A-Z]{1}\d*")
    if regex.match(label):
        x = ALPHABET[label[0]]
        y = int(label[1:]) - 1
        return (x, y)
    return(-1, -1)


class Cell:
    '''
    Cell class to hold the value of cell, coordinates, and where it 'points' to
    Constructor:
        data - a string with the data to be populated
        x - an int with the cell's x position
        y - an int with the cell's y position
    Properties:
        type - type of the cell, can take on values: value, cell, or expression
        values - a float, string, or list of strings depending on cell type
        pointer_x - x coordinate of cell being pointed to by current cell
        pointer_y - y coordinate of cell being pointed to by current cell
            pointer_x,y are -1, -1 unless type is cell
    Representation:
        The current value stored in values
    '''
    # this should really be a struct or something. oh well
    def __init__(self, data, x, y):
        self.x = x
        self.y = y
        self.values = data.split(' ')
        if len(self.values) > 1:
            self.type = "expression"
            # create dictionary of locations of child cells
            self.children = {i: label_to_xy(x) for i, x in
                             enumerate(self.values)}
            # expressions don't point anywhere
            self.pointer_x = -1
            self.pointer_y = -1
        else:
            try:
                # type, value, and where it points to(floats point nowhere)
                self.type = "value"
                self.values = float(self.values[0])
                self.pointer_x = -1
                self.pointer_y = -1
            except:
                # Type and where it points to. Leave values as list of strings.
                self.type = "cell"
                self.pointer_x, self.pointer_y = label_to_xy(self.values[0])

    def __repr__(self):
        '''
        Representation:
            The current value stored in values
        '''
        # uncomment below to change repr to list with value and coords
        # return str([self.values, self.x, self.y])
        return str(self.values)


class Grid(object):
    '''
    Grid class to hold table of cells
    Constructor:
        data - a list of strings with data from each line of input file
        m - an int with the grid's size
        n - an int with the grid's size
    Properties:
        grid - table of cells
        m - size of grid
        n - size of grid
        visited_cells - dictionary that is used like a stack.
    '''
    def __init__(self, data, m, n):
        self.grid = [[0] * n for x in range(m)]
        self.m = m
        self.n = n
        self.visited_cells = {}  # basically just a stack
        y = 0
        for i in range(len(data)):
            if i % n == 0 and i != 0:
                y += 1
            x = i % n
            temp_cell = Cell(data[i], x, y)
            self.grid[y][x] = temp_cell

    def __repr__(self):
        '''
        Representation:
            table of values of each cell that has been converted to a string
        '''
        values = [[0]*self.n for x in range(self.m)]
        for i in range(len(self.grid)):
                values[i] = self.grid[i]
        return str(values)

    def evaluate_reverse_polish_notation(self, expression):
        '''
        Evaluats a list that is in reverse polish notation
        Arguments:
            Expression - a list of floats and strings in RPN
        Returns:
            A single float with the value of the expression
        '''
        # expression can be a float  or a list, so need to check
        try:
            n = len(expression)
            stack = [0]*n
            index = 0
            for i in range(n):
                current = expression[i]
                if current not in OPERATIONS:
                    current = float(current)

                index -= 1
                if current == "*":
                    stack[index - 1] *= stack[index]
                elif current == "/":
                    try:
                        stack[index - 1] /= stack[index]
                    except:
                        return None
                elif current == "+":
                    stack[index - 1] += stack[index]
                elif current == "-":
                    stack[index - 1] -= stack[index]
                else:
                    index += 1
                    stack[index] = current
                    index += 1
            return stack[0]
        except:
            return expression

    def evaluate_cell(self, current_cell):
        '''
        Recursive function to evaluate current cell and all of its children
        Arguments:
            current_cell - A reference to the cell you would like to evaluate
        Returns:
            A float with the value of the current cell.
            Evaluates all child cells
        '''
        # Base Case. No more pointers to follow
        if current_cell.type == "value":
            return current_cell.values

        # Recurse on Cell
        if current_cell.type == "cell":
            # detect cycle
            if current_cell in self.visited_cells:
                return current_cell.values
            self.visited_cells[current_cell] = True
            # update child
            current_cell.values = self.evaluate_cell(self.grid
                                                     [current_cell.pointer_x]
                                                     [current_cell.pointer_y])
            # remove from visited "stack"
            del self.visited_cells[current_cell]
            return current_cell.values

        # Recurse on expression
        if current_cell.type == 'expression':
            # detect cycle
            if current_cell in self.visited_cells:
                return current_cell.values
            self.visited_cells[current_cell] = True

            temp = []
            # convert expression to list of floats and operations
            # ['A1', 'A2', '+', '3', '/'] -> [3, 4, '+', 3 '/']
            for value in current_cell.values:
                if value in OPERATIONS:
                    temp.append(value)
                elif value.isdigit():
                    temp.append(float(value))
                else:
                    # value is a cell label, so evaluate that cell
                    x, y = label_to_xy(value)
                    temp.append(self.evaluate_cell(self.grid[x][y]))

            # modify current cell's value and evaluate the cell
            current_cell.values = temp
            current_cell.values = self.evaluate_reverse_polish_notation(
                current_cell.values)
            current_cell.type = 'value'
            # remove current cell from stack
            del self.visited_cells[current_cell]
            return current_cell.values

    def evaluate(self):
        '''
        Driver function to evaluate every cell in the grid
        No Arguments
        No Return Value
        '''
        for row in self.grid:
            for cell in row:
                self.evaluate_cell(cell)

    def output(self):
        '''
        Condenses the values of cells in grid down to a single list. Will raise
        an exception if there is an invalid value. You can alter the
        functionality of the program to include cyclic dependencies as lists
         of their labels.
        i.e. if "A1" has a cyclic dependencies, include ["A1"] in output list.

        No Arguments
        Returns:
            List of cell values in the grid
        '''
        values = []
        for row in self.grid:
            for cell in row:

                if type(cell.values) is list:
                    raise ValueError("Encountered Cyclic Dependency")
                if cell.values is None:
                    # Can probably call this sooner
                    raise ZeroDivisionError("Invalid Value: None")
                values.append(cell)
        return values

    def get_cyclic_dependencies(self):
        '''

        Make list of cyclic dependencies
        No Arguments
        Returns:
            List of cell objects
        '''
        dependencies = []
        for row in self.grid:
            for cell in row:
                if type(cell.values) is list:
                    dependencies.append(cell)
        return dependencies


if __name__ == "__main__":
    # for timing how long it takes to run
    # import timeit
    # start = timeit.default_timer()

    args = parse_arguments()
    grid = parse_grid(args.input_fname)
    if grid is not None:
        grid.evaluate()

        # try:  # uncomment this for alternative functionality
        #         and indent starting here
        output = grid.output()

        # print or print and write to file
        print grid.n, grid.m
        if not args.output_fname:
            for i in output:
                print "{0:.5f}".format(float(i.values))
        else:
            for i in output:
                print "{0:.5f}".format(float(i.values))
            # with open(args.output_fname, 'w') as f:
            #     f.write("{} {}\n".format(grid.n, grid.m))
            #     for value in output:
            #         f.write("{0:.5f}\n".format(float(value.values)))

        # indent to here
        ############################
        # ALTERNATIVE FUNCTIONALITY#
        ############################
        # except(ValueError):
        #     # print or print and write to file
        #     if not args.output_fname:
        #         print "Cyclic Dependency detected."
        #         output = grid.get_cyclic_dependencies()
        #         print "List of Cells with Cyclic Dependency:\n", output
        #     else:
        #         print "Cyclic Dependency detected."
        #         output = grid.get_cyclic_dependencies()
        #         print "List of Cells with Cyclic Dependency:\n", output
        #
        #         with open(args.output_fname, 'w') as f:
        #             f.write("Cyclic Dependency detected.\n\
        #             List of Cells with Cyclic Dependency:\n\
        #             {}".format(output))
        # except(ZeroDivisionError):
        #     raise ZeroDivisionError("Invalid input. Cannot divide by zero.")

    # stop = timeit.default_timer()
    # print "Time to run: ", stop-start

    # basic tests for RPN
    # print grid.evaluate_reverse_polish_notation([1, 0, '/'])
    # print grid.evaluate_reverse_polish_notation([10, -2, '/', 55, '+'])

    # # just using this to generate an arbitrarily long test set to see speed
    # # can run a file with 1,000,000 lines in 38 seconds.
    # with open('test12.txt', 'w') as f:
    #     f.write("100 1\n1\n1\n")
    #     for i in range(2, 100):
    #         if i % 3 == 0:
    #             f.write('A{} 1 -\n'.format(i))
    #         else:
    #             f.write('A{} 1 +\n'.format(i))

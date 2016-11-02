import sys
import argparse

# alphabet = {'A': 1, 'B': 2, ... }
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alphabet = {k: i for i, k in enumerate(alphabet)}
operations = set(['+', '-', '*', '/'])


def get_coords(label):
    # needed for both cell and grid classes
    # helper to get position from label i.e. 'A1' -> (0, 0)
    if label.isdigit() or label == 'None':
        return (-1, -1)
    x = alphabet[label[0]]
    y = int(label[1:]) - 1
    return (x, y)


class Cell:
    # this should really be a struct or something. oh well
    def __init__(self, data, x, y):
        self.x = x
        self.y = y
        self.values = data.split(' ')
        if len(self.values) > 1:
            self.type = "expression"
            # get 1st ind from alphabet dict, and 2nd from rest of numbers
            self.values = [Cell(v, get_coords(v)[0], get_coords(v)[1]) if
                           v not in operations else v for v in self.values]
            self.pointer_x = -1
            self.pointer_y = -1

        else:
            try:
                # type, value, and where it points to (floats point nowhere)
                self.type = "value"
                self.values = float(self.values[0])
                self.pointer_x = -1
                self.pointer_y = -1
            except:
                # type and where it points to
                self.type = "cell"
                self.pointer_x, self.pointer_y = get_coords(self.values[0])

    def __repr__(self):
        # return str([self.values, self.x, self.y])
        return str(self.values)


class Grid(object):

    def __init__(self, values, m, n):
        self.grid = [[0] * n for x in range(m)]
        self.m = m
        self.n = n
        self.visited_cells = {}  # basically just a stack
        self.cycle = False
        y = 0
        for i in range(len(values)):
            if i % n == 0 and i != 0:
                y += 1
            x = i % n
            temp_cell = Cell(values[i], x, y)
            self.grid[y][x] = temp_cell

    def __repr__(self):
        values = [[0]*self.n for x in range(self.m)]
        for i in range(len(self.grid)):
                values[i] = self.grid[i]
        return str(values)

    def evaluate_reverse_polish_notation(self, expression):
        # expression is a float sometimes, so need to check
        try:
            ops = set(['+', '-', '*', '/'])
            n = len(expression)
            stack = [0]*n
            index = 0
            for i in range(n):
                current = expression[i]
                if current not in ops:
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

    def evaluate(self, current):
        if self.cycle:
            # self.visited_cells = {}
            raise StopIteration("Cyclic reference: {}".format(current.values))

        # Base Case. No more pointers to follow
        if current.type == "value":
            return current.values

        # recurse and follow pointers
        if current.type == "cell":
            if current in self.visited_cells:
                self.cycle = True
            self.visited_cells[current] = True
            current.values = self.evaluate(self.grid[current.pointer_x]
                                                    [current.pointer_y])
            # remove from visited "stack"

            print self.visited_cells
            # del self.visited_cells[current.values]
            return current.values

        # recurse and follow pointers of each cell in expression
        if current.type == 'expression':
            if current in self.visited_cells:
                self.cycle = True
            self.visited_cells[current] = True
            temp = []
            for value in current.values:
                if value in operations:
                    temp.append(value)
                elif value.isdigit():
                    temp.append(float(value))
                else:
                    temp.append(self.evaluate(value))
            current.values = temp
            current.values = self.evaluate_reverse_polish_notation(
                current.values)
            # del self.visited_cells[current]
            current.type = 'value'
            return current.values

    def output(self):
        values = []
        for i in self.grid:
            for j in i:
                values.append(j)
        return values


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    return parser.parse_args()


def parse_file(fname):
    with open(fname, 'r') as f:
        data = f.read()
        lines = data.strip().split('\n')
        n, m = map(int, lines[0].split())
        lines = lines[1:]
        grid = Grid(lines, m, n)
    return grid


if __name__ == "__main__":
    args = parse_arguments()
    grid = parse_file(args.filename)
    for i in range(len(grid.grid)):
        for j in range(len(grid.grid[i])):
            # print j
            grid.evaluate(grid.grid[i][j])
    # grid.evaluate(grid.grid[0][1])
    print grid.output()
    # testing reverse polish notation evaluation
    # print grid.evaluate_reverse_polish_notation([1, 0, '/'])
    # print grid.evaluate_reverse_polish_notation([10, -2, '/', 55, '+'])

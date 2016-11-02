import argparse
import re
from math import ceil, sqrrt


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('grid_fname')
    parser.add_argument('dict_fname')
    return parser.parse_args()


def make_board(fname):
    with open(fname, 'r') as f:
        data = f.read()
        data = data.split('\n')
        n = int(data[0])
        layers = [layer.split() for layer in data[1:]]
        board = Board()
        board.insert(layers)
    return board


def make_trie(dict_file, grid_file):
    # cheap way to prune search tree
    with open(grid_file) as g:
        alphabet = g.read()
        alphabet = ''.join(set(filter(str.isalpha, alphabet)))

    with open(dict_file) as f:
        data = f.read()
        words = data.split('\n')

        # skip word if first 3 letters aren't in the grid
        # to prune search tree early
        prune_regex = re.compile('[' + alphabet + ']{3,}$', re.I).match
        words = filter(prune_regex, words)

        root = TrieNode(None, '')
        for word in words:
            current_node = root
            for letter in word:
                # between 'A', ... 'Z', '['
                # should always be, but just to be safe...
                if 65 <= ord(letter) < 91:
                    next_node = current_node.children[ord(letter) - 65]
                    # node wasn't in trie, so put it in
                    if next_node is None:
                        next_node = TrieNode(current_node, letter)
                    current_node = next_node
            current_node.isWord = True
    return root


def search(grid, dictionary):
    size = grid.size
    queue = []
    valid_words = []
    for x in range(-size + 1, size):
        for y in range(-size + 1, size):
            # outside of grid
            if abs(x) + abs(y) >= size:
                break
            c = grid.hexagons[(x, y)].value
            node = dictionary.children[ord(c) - 65]
            if node is not None:
                queue.append((x, y, c, node))
    while queue:
        x, y, s, node = queue[0]
        queue.pop(0)
        for dx, dy in ((1, 0), (1, -1), (0, -1), (-1, -1),
                       (-1, 0), (-1, 1), (0, 1), (1, 1)):
            x_2, y_2 = x + dx, y + dy
            if abs(x) < size and abs(y) < size and abs(x) + abs(y) < size:
                s_temp = grid.hexagons[(x2, y2)]
                s_2 = s + s_temp
                node_2 = node.children[ord(s_temp) - 65]
                if node_2 is not None:
                    if node_2.isWord:
                        valid_words.append(s_2)
                    queue.append((x_2, y_2, s_2, node_2))
    return valid_words


class Hex:

    def __init(self, value, x, y):
        self.value = None
        self.x = 0
        self.y = 0
        self.neighbors = {(0, 1): None,
                          (1, 0): None,
                          (1, -1): None,
                          (0, -1): None,
                          (-1, 0): None,
                          (-1, 1): None}

    def __repr(self):
        return '({0}, {1}, {2})'.format(self.value, self.x, self.y)


class Board:

    def __init__(self):
        self.size = 0
        # hexagons get hashed by (x,y) tuple, and store hexagon as value
        self.hexagons = {}
        # isn't same size as grid, but doesn't matter if we only look in grid.
        self.visited = {(i, j): False for i in range(self.size)
                        for j in range(self.size)}
        # neighboring directions
        self.dx = [0, 1, 1, 0, -1, -1]
        self.dy = [1, 0, -1, -1, 0, 1]

    def insert(self, layers):
        # feels slightly less sloppy doing this than making calls to methods
        # in the constructor
        # TODO should probably rename this something else to be more clear
        # TODO should implement testing and error handling
        self.size = len(layers)
        index = 0
        for layer in layers:
            for value in layer:
                x, y = self.number_to_grid_coord(index)
                temp_hex = Hex(value, x, y)
                self.hexagons[(x, y)] = temp_hex
                self.update_neighbors(temp_hex)
                index += 1
        return self.hexagons[(0, 0)]

    def number_to_grid_coord(self, n):
        # TODO CLEAN THIS UP
        """Convert a number to its coordinates in the hexagonal coordinate system

            Args:
                number: A number assigned to a hexagon

            Returns:
                Coordinates of the number in the hexagonal coordinate system as
                a tuple.
        """

        # dx = [0, -1, -1, 0, 1, 1, 0]
        # dy = [1, 0, -1, -1, 0, 1, 1]

        # NUMBER OF HEXAGONS IN A HONEYCOMB LATTICE OF RADIUS N+1 IS GIVEN BY
        # THE SEQUENCE OEIS003215 => 3n^2 + 3n + 1
        if n == 0:
            return (0, 0)
        else:
            dist = int(ceil((-3 + sqrt(-3 + 12 * n)) / 6))
        # highest index in previous level given by OEIS003215
        max_in_prev_layer = 3 * (dist - 1) * (dist - 1) + 3 * (dist - 1) + 1
        # number of nodes between previous level and current node
        level_shift = number - max_number_prev_level
        diagonal = int(ceil(level_shift / float(distance)))
        diagonal_shift = diagonal * distance - level_shift

        start = diagonal % 6
        end = diagonal % 6 + 2
        # diagonal_coordinates = tuple(self.dx[start:end])
        diagonal_coordinates = tuple(
            [coord * distance for coord in self.dx[start:end]])

        start = diagonal - 1
        end = diagonal + 1
        # diagonal_shift_coordinates = tuple(self.dy[start:end])
        diagonal_shift_coordinates = tuple(
            [coord * diagonal_shift for coord in self.dy[start:end]])

        res = tuple(map(operator.add, diagonal_coordinates,
                        diagonal_shift_coordinates))
        res = tuple([
            int(diagonal_coordinates[i] + diagonal_shift_coordinates[i])
            for i in range(len(diagonal_coordinates))])
        # res = tuple([int(coord) for coord in res])

        return res

    def get_neighbors(self, hex):
        return [x[1] for x in hex.neighbors.items() if x.value is not None]

    def update_neighbors(self, h):
        if h is None:
            print "Invalid hexagon, h=None"
            return
        x, y = h.x, h.y
        # updates current hexagon's neighbors
        for i in range(6):
            # need to check to avoid KeyError
            if (x + self.dx[i], y + self.dy[i]) in self.hexagons:
                neighbors[(self.dx[i], self.dy[i])] = self.hexagons[
                    (x + self.dx[i], y + self.dy[i])]
        surrounding_neighbors = self.get_neighbors(h)
        # going in the reverse direction just negates self.dx[i], self.dy[i]
        for neighbor in surrounding_neighbors:
            neighbor.neighbors[(-self.dx[i], -self.dy[i])] = h
        return h

    def check_board(word, current_ind, r, c, word_len):
        if current_ind == word_len - 1:
            return True
        ret = False
        for i in range(6):
            new_col = c + self.dx[i]
            new_row = r + self.dy[i]
            if abs(new_col) >= self.size - 1 or abs(new_row) >= self.size or
            new_col + new_row >= self.size and
            not visited[(new_row, new_col)]
            and word[current_ind + 1] == board[new_row][new_col]:
                    current_ind += 1
                    visited[(new_row, new_col)] = True
                    ret = check_board(word, current_ind,
                                      new_row, new_col, word_len)
                    if ret:
                        break
                    visited[(new_row, new_col)] = False
        return ret


# class Node:
#     # Trie node implementation borrowed from pythonfiddle
#     # http://pythonfiddle.com/python-trie-implementation/
#
#     def __init__(self):
#         self.word = None
#         self.nodes = {}
#
#     def __repr__(self):
#         return self.word
#
#     def get_all_words(self):
#         all_words = []
#         # get words from children nodes
#         for key, node in self.nodes.iteritems():
#             if node.word is not None:
#                 all_words.append(node.word)
#             # append list of child words
#             all_words += node.get_all_words()
#         return all_words
#
#     def insert(self, word, string_pos=0):
#         current_letter = word[string_pos]
#         if current_letter not in self.nodes:
#             self.nodes[current_letter] = Node()
#         if string_pos + 1 == len(word):
#             self.nodes[current_letter].word = word
#         else:
#             self.nodes[current_letter].insert(word, string_pos + 1)
#
#         return True
#
#     def get_all_with_prefix(self, prefix, string_pos):
#         x = []
#         for key, node in self.nodes.iteritems():
#             if string_pos >= len(prefix) or key == prefix[string_pos]:
#                 if node.word is not None:
#                     x.append(node.word)
#                 if node.nodes != {}:
#                     if string_pos + 1 <= len(prefix):
#                         x += node.get_all_with_prefix(prefix, string_pos + 1)
#                     else:
#                         x += node.get_all_with_prefix(prefix, string_pos)
#         return x
#
#
# class Trie:
#     # Trie implementation borrowed from pythonfiddle
#     # http://pythonfiddle.com/python-trie-implementation/
#
#     def __init__(self):
#         self.root = None
#
#     def insert(self, word):
#         self.root.insert(word)
#
#     def get_all_words(self):
#         return self.root.get_all_words()
#
#     def get_all_with_prefix(self, prefix, string_pos=0):
#         return self.root.get_all_with_prefix(prefix, string_pos)
#


class TrieNode:

    def __init__(self, parent, value):
        self.parent = parent
        self.children = [None] * 26
        self.isWord = False
        if parent is not None:
            # use ascii codes to get correct node
            parent.children[ord(value) - 97] = self


if __name__ == "__main__":
    # parses command line arguments
    # takes the filepath to the grid/board and the filepath to the dictionary
    args = arg_parser()
    # get list of characters that are in the grid

    # builds the board/grid
    grid = parse_board(args.grid_fname)
    # use trie since you don't have to restart search every time
    word_trie = parse_dictionary(args.dict_fname, args.grid_fname)

# def unique_chars(s):
#     d = {}
#     for i in s:
#         if i in d:
#             return False
#         d[i] = 1
#     return True


# print unique_chars("abcdefg")
# print unique_chars('aaa')
# print unique_chars('')


# def rev_string(s):
#     temp = s[-1]
#     s = s[:-1]
#     s = s[::-1]
#     s += temp
#     return s


# print rev_string('abc')
# print rev_string('0')
# print rev_string("00")


# def permuted_strings(s1, s2):
#     from collections import Counter
#     if len(s1) != len(s2):
#         return False
#     d1 = Counter(s1)
#     d2 = Counter(s2)
#     if d1 == d1:
#         return True
#     return False

# print permuted_strings('abc', 'cba')
# print permuted_strings('abc', 'bca')
# print permuted_strings('aaa', 'abbb')
# print permuted_strings('', '')
# print permuted_strings('', 'abc')

# def replace_char(s, c1, c2):
#     scopy = ''
#     for char in s:
#         if char == c1:
#             scopy += c2
#         else:
#             scopy += char
#     return scopy

# print replace_char('a string    with spaces', ' ', '%20')
# print replace_char('a string with    no spaces', ' ', '')
# print replace_char('    ', ' ', '%20')

# version 1, just show all at once
# def string_compression(s):
#     from collections import Counter
#     d = Counter(s)
#     compressed = ''
#     for char in s:
#         if char in d:
#             compressed += char + str(d[char])
#             del d[char]
#     return compressed

# print string_compression('aabcccccaaa')

# def string_compression(s):
#     news = ''
#     i = 0
#     j = 1
#     while i < len(s)-1:
#         if s[i] == s[i+1]:
#             j += 1
#             i += 1
#         else:
#             news += str(s[i]) + str(s[j])
#             j = 1
#             i += 1
#     return news

# print string_compression('aabcccccaaa')

# def rotate_image(img):
#     new_img = []
#     for j in range(len(img[0])):
#         new_line = ''
#         for i in range(len(img)):
#             new_line += img[i][j]
#         new_img.append(new_line)
#     return new_img

# print rotate_image(['abc', 'abc', 'abc'])
# print rotate_image(['1', '1', '1'])

# def make_zero(matrix):
#     coords = {}
#     for i in range(len(matrix)):
#         for j in range(len(matrix[0])):
#             if matrix[i][j] == 0:
#                 coords[(i, j)] = 1
#     if len(coords) >= min(len(matrix), len(matrix[0])):
#         return [[0]*len(matrix[0]) for i in range(len(matrix))]
#     for coord in coords:
#         for i in range(len(matrix)):
#             matrix[i][coord[1]] = 0
#         for j in range(len(matrix[0])):
#             matrix[coord[0]][j] = 0
#     return matrix

# print make_zero([[1, 1, 1, 0], [1, 1, 1, 1]])
# print make_zero([[1, 1, 1, 1], [1, 1, 1, 1]])
# print make_zero([[1, 1, 1, 0], [0, 0, 0, 0]])

# def remove_duplicates(l):
#     cache = {}
#     parent = l.head
#     current = l.next
#     while current is not None:
#         if current in cache:
#             parent.next = current.next
#             del current
#         else:
#             cache[current] = 1
#         parent = current
#         current = current.next
#     return l

# def kth_item(l, k):
#     if k <= 0 or l is None:
#         return None
#     cache = {}
#     length = 0
#     for node in l:
#         cache[length] = node
#         length += 1
#     return cache[length-k]

# def delete_node_in_place(node):
#     if node is None or node.next is None:
#         return None
#     temp = node.next
#     node.value = node.next.value
#     node.next = node.next.next
#     del temp
#     return

# def add_numbers(n1, n2):
#     if n1 is None and n2 is None:
#         return None
#     values = []
#     carry = 0
#     while n1 and n2:
#         s = n1 + n2 + carry
#         if s >= 10:
#             values.append(s % 10)
#             carry = 1
#         else:
#             values.append(s)
#             carry = 0
#         n1 = n1.next
#         n2 = n2.next
#     if carry = 1:
#         values.append(1)
#     values = map(str, values)
#     values.reverse()
#     return int(''.join(values))

# def find_beginning(node):
#     cache = {}
#     noloop = True
#     while node not in cache:
#         cache[node] = 1
#         node = node.next
#     return node

# def is_palindrome(node):
#     vals = ''
#     while node:
#         vals += str(node.value)
#     if vals = vals[::-1]:
#         return True
#     return False

class Stack:
    def __init__(self):
        self.stack = []
        self.size = 0
        self.min = 0

    def min(self):
        return self.min

    def push(self, d):
        self.stack.append(d)
        self.min = min(self.min, d)

    def pop(self):
        self.min = min(self.stack[:-1])
        return self.stack.pop()

    def size(self):
        return self.size


class SetofStacks:
    def __init__(self, capacity):
        self.stacks = [Stack()]
        self.stack_num = 1
        self.capacity = capacity
        self.remaining = [capacity]
        self.min_ind = 0

    def pop(self):
        self.remaining[-1] += 1
        return self.stacks[-1].pop()

    def push(self, d):
        if self.stacks[-1].size() < self.capacity:
            self.stacks[-1].push(d)
            self.remaining[-1] -= 1
        else:
            newstack = Stack()
            newstack.push(d)
            self.stacks.append(newstack)
            self.remaining.append(self.capacity - 1)

    def pop_at(self, index):
        self.remaining[index] += 1
        self.stacks[index].pop

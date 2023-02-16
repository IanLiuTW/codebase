# This is a template for union find with count. The count is the number of sets.
# It uses a dictionary to store the root of each element,
# so it is important to call add() before union() or find().
# The union() function was not optimized.

class UF:
    def __init__(self) -> None:
        self.root = dict()
        self.cnt = 0

    def add(self, x):
        if x not in self.root:
            self.root[x] = x
            self.cnt += 1

    def find(self, x):
        if self.root[x] != x:
            self.root[x] = self.find(self.root[x])
        return self.root[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            self.root[ry] = rx
            self.cnt -= 1

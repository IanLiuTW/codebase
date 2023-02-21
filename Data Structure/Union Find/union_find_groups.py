# This is a template for union find with groups. The groups is the number of sets.
# The union() function was not optimized.

class UF:
    def __init__(self, size) -> None:
        self.root = list(range(size))
        self.groups = size

    def find(self, x):
        if self.root[x] != x:
            self.root[x] = self.find(self.root[x])
        return self.root[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            self.root[ry] = rx
            self.groups -= 1

    def get_groups(self):
        return self.groups

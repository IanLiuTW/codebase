# Disjoint Set Data Structure with Rank and Path Compression

class UnionFind:
    def __init__(self, size):
        self.root = list(range(size))
        self.rank = [0] * size

    def find(self, x):
        if self.root[x] != x:
            self.root[x] = self.find(self.root[x])
        return self.root[x]

    def union(self, x, y):
        x_set, y_set = self.find(x), self.find(y)
        if x_set == y_set:
            return
        if self.rank[x_set] > self.rank[y_set]:
            self.root[y_set] = x_set
        elif self.rank[x_set] < self.rank[y_set]:
            self.root[x_set] = y_set
        else:
            self.root[y_set] = x_set
            self.rank[x_set] += 1

    def connected(self, x, y):
        return self.find(x) == self.find(y)

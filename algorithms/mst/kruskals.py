# LeetCode - 1584. Min Cost to Connect All Points
# https://leetcode.com/problems/min-cost-to-connect-all-points/description/


# Kruskal's Algorithm
class UF:
    def __init__(self, size):
        self.root = list(range(size))

    def find(self, x):
        if self.root[x] != x:
            self.root[x] = self.find(self.root[x])
        return self.root[x]

    def union(self, x, y):
        x_set, y_set = self.find(x), self.find(y)
        if x_set != y_set:
            self.root[y_set] = x_set
            return True
        return False


class Solution:
    def minCostConnectPoints(self, points: list[list[int]]) -> int:
        n = len(points)

        edges = []
        for i in range(n):
            for j in range(i+1, n):
                edges.append(
                    (abs(points[i][0]-points[j][0])+abs(points[i][1]-points[j][1]), i, j)
                )
        edges.sort(key=lambda x: x[0])

        mst_cost, mst_edges = 0, 0
        uf = UF(n)
        for w, a, b in edges:
            if uf.union(a, b):
                mst_cost += w
                mst_edges += 1
                if mst_edges == n-1:
                    break
        return mst_cost

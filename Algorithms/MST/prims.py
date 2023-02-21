# LeetCode - 1584. Min Cost to Connect All Points
# https://leetcode.com/problems/min-cost-to-connect-all-points/description/


from heapq import heappop, heappush


# Prim's Algorithm with Heap
class Solution:
    def minCostConnectPoints(self, points: list[list[int]]) -> int:
        ans = 0

        pts = set(range(len(points)))
        heap = [(0, 0)]

        while pts:
            cost, p1_i = heappop(heap)
            if p1_i not in pts:
                continue

            ans += cost
            pts.remove(p1_i)

            for p2_i in pts:
                heappush(heap, (
                    abs(points[p1_i][0] - points[p2_i][0]) +
                    abs(points[p1_i][1] - points[p2_i][1]),
                    p2_i
                ))

        return ans


# Prim's Algorithm with Dictionary
class Solution:
    def minCostConnectPoints(self, points: list[list[int]]) -> int:
        ans = 0

        pts_dis = {pt_idx: float('inf') for pt_idx in range(len(points))}
        pts_dis[0] = 0

        while pts_dis:
            min_pt_idx = min(pts_dis, key=lambda pt_idx: pts_dis[pt_idx])
            ans += pts_dis[min_pt_idx]
            pts_dis.pop(min_pt_idx)

            for pt_idx in pts_dis:
                pts_dis[pt_idx] = min(
                    pts_dis[pt_idx],
                    abs(points[min_pt_idx][0] - points[pt_idx][0]) +
                    abs(points[min_pt_idx][1] - points[pt_idx][1])
                )

        return int(ans)

# Prim's Algorithm
# LeetCode - 1584. Min Cost to Connect All Points
# https://leetcode.com/problems/min-cost-to-connect-all-points/description/

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

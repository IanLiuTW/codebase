# Readings:
# [Python] Powerful Ultimate Binary Search Template. Solved many problems -
# https://leetcode.com/discuss/general-discussion/786126/Python-Powerful-Ultimate-Binary-Search-Template.-Solved-many-problems

# Binary Search Template
def binary_search(array, target):
    # Boundary: it should cover all possible cases that we need to search
    # Could be [0, n-1], [0, n] etc
    lo, hi = 0, len(array) - 1

    while lo < hi:
        mid = lo + (hi - lo) // 2

        # Condition: this is the part that we need to design according to the problem
        # i.e. array[mid] >= target is equivalent to bisect.bisect_left(array, target)
        # i.e. array[mid] > target is equivalent to bisect.bisect_right(array, target)
        if array[mid] >= target:
            hi = mid
        else:
            lo = mid + 1

    # Return Value: the lo is the minimum index satisfying the condition
    # We have to decide what should be returned. Could be lo, or lo-1, or array[lo]
    return lo


# Binary Search Template - Variation
# This is a variation of the above template where we need to find the maximum value that satisfies the condition
def binary_search_variation(lo, hi, max_val):
    while lo < hi:
        mid = (lo+hi+1)//2
        if mid <= max_val:
            lo = mid
        else:
            hi = mid-1
    return lo


# LeetCode - 1011. Capacity To Ship Packages Within D Days
# https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/
class Solution:
    def shipWithinDays(self, weights: list[int], days: int) -> int:
        def days_needed(capacity):
            cap, days = capacity, 1
            for w in weights:
                if cap < w:
                    cap, days = capacity, days+1
                cap -= w
            return days

        lo, hi = max(weights), sum(weights)
        while lo < hi:
            mid = (lo+hi) // 2
            # Here, we find the smallest capacity that can be shipped in days days or less
            # The result will be the smallest value in the range that satisfies the condition
            if days_needed(mid) <= days:
                hi = mid
            else:
                lo = mid+1
        return lo

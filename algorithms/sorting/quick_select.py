# LeetCode - 215. Kth Largest Element in an Array
# https://leetcode.com/problems/kth-largest-element-in-an-array/description/?envType=study-plan-v2&id=leetcode-75

# Quick Select
# Time Complexity: Best Case: O(n), Average Case: O(n), Worst Case: O(n^2)

from random import randint


class Solution:
    def findKthLargest(self, nums: list[int], k: int) -> int:
        def partition(left, right, pivot):
            nums[pivot], nums[right] = nums[right], nums[pivot]

            cur = left
            for i in range(left, right):
                if nums[i] < nums[right]:
                    nums[cur], nums[i] = nums[i], nums[cur]
                    cur += 1

            nums[right], nums[cur] = nums[cur], nums[right]
            return cur

        def select(left, right, k_smallest):
            if left == right:
                return nums[left]

            pivot = partition(left, right, randint(left, right))
            if pivot == k_smallest:
                return nums[pivot]
            elif pivot < k_smallest:
                return select(pivot+1, right, k_smallest)
            else:
                return select(left, pivot-1, k_smallest)

        return select(0, len(nums)-1, len(nums)-k)

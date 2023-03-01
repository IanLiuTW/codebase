# LeetCode - 912. Sort an Array
# https://leetcode.com/problems/sort-an-array/description/

# Quick Sort
# Time Complexity: Best Case: O(nlogn), Average Case: O(nlogn), Worst Case: O(n^2)

from random import randint


class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        def quick_sort(start, end):
            def partition(start, end, pivot):
                nums[end], nums[pivot] = nums[pivot], nums[end]

                cur = start
                for i in range(start, end):
                    if nums[i] <= nums[end]:
                        nums[i], nums[cur] = nums[cur], nums[i]
                        cur += 1
                nums[cur], nums[end] = nums[end], nums[cur]
                return cur

            if start < end:
                mid = partition(start, end, randint(start, end))
                quick_sort(start, mid-1)
                quick_sort(mid+1, end)

        # Worst Case: O(n^2)
        if len(set(nums)) == 1:
            return nums

        quick_sort(0, len(nums)-1)
        return nums

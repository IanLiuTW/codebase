# LeetCode - 912. Sort an Array
# https://leetcode.com/problems/sort-an-array/description/

# Counting Sort
# Time Complexity: Best Case: O(n+k), Average Case: O(n+k), Worst Case: O(n+k) (k is the range of the input)


class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        def counting_sort(nums):
            cnter = collections.Counter(nums)
            min_, max_ = min(cnter), max(cnter)

            i = 0
            for num in range(min_, max_+1):
                for _ in range(cnter[num]):
                    nums[i] = num
                    i += 1
            return nums

        return counting_sort(nums)

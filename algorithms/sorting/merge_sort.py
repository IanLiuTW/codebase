# LeetCode - 912. Sort an Array
# https://leetcode.com/problems/sort-an-array/description/

# Merge Sort
# Time Complexity: Best Case: O(nlogn), Average Case: O(nlogn), Worst Case: O(nlogn)


class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        def merge(left, right):
            i = j = 0
            merged = []
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1
            merged += left[i:] + right[j:]
            return merged

        def merge_sort(nums):
            if len(nums) <= 1:
                return nums
            mid = len(nums)//2
            left = merge_sort(nums[:mid])
            right = merge_sort(nums[mid:])
            return merge(left, right)

        return merge_sort(nums)

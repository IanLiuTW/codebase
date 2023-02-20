# KMP algorithm
# LeetCode - 28. Find the Index of the First Occurrence in a String
# https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string

def strStr(haystack, needle):
    n, h = len(needle), len(haystack)
    i, j, nxt = 1, 0, [-1]+[0]*n
    while i < n:
        if j == -1 or needle[i] == needle[j]:
            i += 1
            j += 1
            nxt[i] = j
        else:
            j = nxt[j]
    i = j = 0
    while i < h and j < n:
        if j == -1 or haystack[i] == needle[j]:
            i += 1
            j += 1
        else:
            j = nxt[j]
    return i-j if j == n else -1

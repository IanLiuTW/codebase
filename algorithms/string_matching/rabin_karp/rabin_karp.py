# LeetCode - 28. Find the Index of the First Occurrence in a String
# https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string

# Using built-in hash function
import sys


def strStr(haystack, needle):
    n, h = len(needle), len(haystack)
    hash_n = hash(needle)
    for i in range(h-n+1):
        if hash(haystack[i:i+n]) == hash_n:
            return i
    return -1


# Using rolling hash
def strStr(haystack, needle):
    def f(c):
        return ord(c)-ord('A')

    n, h, d, m = len(needle), len(haystack), ord('z')-ord('A')+1, sys.maxsize
    if n > h:
        return -1
    nd, hash_n, hash_h = d**(n-1), 0, 0
    for i in range(n):
        hash_n = (d*hash_n+f(needle[i])) % m
        hash_h = (d*hash_h+f(haystack[i])) % m
    if hash_n == hash_h:
        return 0
    for i in range(1, h-n+1):
        hash_h = (d*(hash_h-f(haystack[i-1])*nd)+f(haystack[i+n-1])) % m
        if hash_n == hash_h:
            return i
    return -1

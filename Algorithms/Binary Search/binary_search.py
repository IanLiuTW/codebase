def binary_search(array, target):
    lo, hi = 0, len(array) - 1  # cloud be [0, n-1], [0, n] etc, depends on problem
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if array[mid] >= target:  # cloud be >=, > or else, depends on problem
            hi = mid
        else:
            lo = mid + 1
    return lo

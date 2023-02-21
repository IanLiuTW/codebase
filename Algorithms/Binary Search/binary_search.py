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

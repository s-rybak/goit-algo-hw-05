def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
    iterations = 0

    while low <= high:
        iterations += 1
        mid = (high + low) // 2

        if arr[mid] < x:
            low = mid + 1

        elif arr[mid] > x:
            high = mid - 1

        else:
            return (iterations, arr[mid])

    if low < len(arr):
        return (iterations, arr[low])
    else:
        return (iterations, None)


arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(binary_search(arr, 2.2))
print(binary_search(arr, 4.9))
print(binary_search(arr, 7))

def insertion_sort(arr):
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):
        key = arr[i]  # Current element to be compared

        # Move elements of arr[0..i-1] that are greater than key
        # to one position ahead of their current position
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]  # Shift elements to the right
            j -= 1
            yield arr

        arr[j + 1] = key  # Place key at its correct position
        yield arr

# ........

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                yield arr

# ........

def merge_sort(arr):
    # Check if the length of the array is greater than 1
    if len(arr) > 1:
        # Calculate the middle index of the array
        mid = len(arr) // 2

        # Split the array into left and right halves
        L = arr[:mid]
        R = arr[mid:]

        # Recursively apply merge_sort to both left and right halves
        yield from merge_sort(L)
        yield from merge_sort(R)

        # Merge the sorted left and right halves back into the original array
        i = j = k = 0
        while i < len(L) and j < len(R):
            # Compare elements from both halves and put the smaller one into the original array
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            yield arr

        # Append any remaining elements from the left and right halves (if any)
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            yield arr
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            yield arr

    return arr  # Return the sorted array

# ............

def quick_sort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1

    if low < high:
        pi = partition(arr, low, high)
        yield from quick_sort(arr, low, pi - 1)
        yield from quick_sort(arr, pi + 1, high)
        yield arr

# .........

def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[i] < arr[left]:
        largest = left

    if right < n and arr[largest] < arr[right]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        yield from heapify(arr, n, largest)



def heap_sort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        yield from heapify(arr, i, 0)
        yield arr

# .....

def insertion_sort_bucket(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def bucket_sort(arr, noOfBuckets=5):
    max_value = max(arr)
    buckets = [[] for _ in range(noOfBuckets)]

    for i in range(len(arr)):
        index = int(arr[i] / max_value * (noOfBuckets - 1))
        buckets[index].append(arr[i])

    output = []
    for i in range(noOfBuckets):
        buckets[i] = insertion_sort_bucket(buckets[i])
        output.extend(buckets[i])
        yield output


# ...........

def counting_sort_radix(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr):
    max_num = max(arr)
    exp = 1

    while max_num // exp > 0:
        counting_sort_radix(arr, exp)  # Call the modified counting_sort_radix
        yield arr
        exp *= 10

    return arr



def counting_sort(arr):
    max_val = max(arr)
    count_arr = [0] * (max_val + 1)

    for number in arr:
        count_arr[number] += 1

    output = []
    for i, count in enumerate(count_arr):
        output.extend([i] * count)
        yield output


# .....

#median and order (quick_select)
def partition(arr, low, high):
    i = low - 1
    pivot = arr[high]

    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def k_smallest(arr, l, r, k):
    if 0 < k <= r - l + 1:
        index = partition(arr, l, r)
        if index - l == k - 1:
            return arr[index]
        if index - l > k - 1:
            return k_smallest(arr, l, index - 1, k)
        return k_smallest(arr, index + 1, r, k - index + l - 1)
    else:
        print("Invalid value of k. Please enter a value within the valid range.")


# arr_str = input("Enter comma-separated elements of the array: ")
# arr = list(map(int, arr_str.split(',')))
# n = len(arr)
# k = int(input(f"Enter the value of k (1 to {n}): "))

# result = k_smallest(arr, 0, n - 1, k)
# if result is not None:
#     print(f"K-th smallest element is {result}")
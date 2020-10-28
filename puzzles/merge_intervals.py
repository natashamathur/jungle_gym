# Given a collection of intervals, merge all overlapping intervals.
# Time to complete: 15 minutes

"""
Example 1:
Input: [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlaps, merge them into [1,6].
"""

"""
Example 2:
Input: [[1,4],[4,5]]
Output: [[1,5]]
Explanation: Intervals [1,4] and [4,5] are considerred overlapping.
"""

# input = [[1,3],[2,6],[8,10],[15,18]]
input = [[1, 4], [4, 5]]


def merge_intervals(input):
    result = []
    place = 0
    ml = len(input)

    while place < ml:
        current, following = input[place], input[place + 1]
        if place < ml - 1 and following[0] <= current[1]:
            result.append([current[0], following[1]])
            place += 2
        else:
            result.append(current)
            place += 1

    return result


print(merge_intervals(input))

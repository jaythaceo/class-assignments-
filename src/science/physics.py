"""
Author: Jason Brooks
Email: jaythaceo@gmail.com
Twitter: @jaythaceo
"""

#testList = [5, 8, 2, 4, 3, 1, 9, 0, 6, 7]
def partition(list, start, end):
    """docstring for partition"""
    pivot = list[end]
    bottom = start - 1
    top = end

    done = 0
    while not done:
        while not done:
            bottom = bottom - 1

            if bottom == top:
                done = 1
                break
            if list[bottom] > pivot:
                list[top] = list[bottom]
                break

        while not done:
            top = top - 1

            if top == bottom:
                done = 1
                break
            if list[top] < pivot:
                list[bottom] = list[top]
                break
    list[top] = pivot
    return top

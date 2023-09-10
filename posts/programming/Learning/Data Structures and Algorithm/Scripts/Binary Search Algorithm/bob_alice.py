def getRightIndex(cards, query, mid):
    mid_number = cards[mid]

    if mid_number == query:
        if mid-1 >= 0 and cards[mid-1] == query:
            return "left"
        else:
            return "found"

    elif mid_number < query:
        return "left"

    else:
        return "right"

def binarySeach(cards, query):
    left, right = 0, len(cards) -1 

    while left <= right:
        mid = left + (right - left) // 2
        r = getRightIndex(cards, query, mid)

        if r == "found":
            return mid

        elif r == "left":
            right = mid + 1
        
        else:
            left = mid - 1
    
    return -1


cards = [8, 8, 6, 6, 6, 6, 6, 6, 3, 2, 2, 2, 0, 0, 0]
query = 6

r = binarySeach(cards, query)
print(r)

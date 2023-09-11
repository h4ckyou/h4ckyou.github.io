def getCommon(array1, array2):
    ptr1, ptr2 = 0, 0

    while ptr1 < len(array1) and ptr2 < len(array2):
        if array1[ptr1] < array2[ptr2]:
            ptr1 += 1
        
        elif array1[ptr1] > array2[ptr2]:
            ptr2 += 1

        else:
            return array1[ptr1]

    return -1


array1 = [2,4]
array2 = [1,2]

r = getCommon(array1, array2)
print(r)

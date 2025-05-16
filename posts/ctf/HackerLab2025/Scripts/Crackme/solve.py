def func(val):
    array = list(val)
    n = len(array)

    for i in range(n // 2):
        # this basically is reversing the string: abcd -> dcba
        c = array[i]
        array[i] = array[n - 1 - i]
        array[n - 1 - i] = c

    return ''.join(array)

original = "321233d6f533532733673325f5570397"
print('HLB2025{' + bytes.fromhex(func(original)).decode() + '}')

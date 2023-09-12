def plusOne(digits):
    digit = int(''.join([str(i) for i in digits]))
    digit += 1
    r = [int(i) for i in str(digit)]

    return r


digits = [9]
r = plusOne(digits)

print(r)

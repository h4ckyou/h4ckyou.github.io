def arrangeCoins(coins):
    rows = [coins]

    if coins == 1:
        return 1

    for i in range(1, coins):
        rows.append(rows[-1] - i)
        
        if i+1 > rows[-1]:
            break
    
    return len(rows[1::])


n = 3
r = arrangeCoins(n)

print(r)

def minCandies(ratings):
    n = len(ratings)
    candies = [1] * n 

    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1

    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)

    total_candies = sum(candies)
    return total_candies

ratings = [1, 0, 2]
r = minCandies(ratings)
print(r)

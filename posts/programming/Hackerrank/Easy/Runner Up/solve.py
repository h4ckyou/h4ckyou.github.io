def getRunnerUp(array, N):
    difference = [(N - j) for j in array]
    maxValue = min(difference)
    exclusiveMax = [i for i in difference if i != maxValue]
    minimum = min(exclusiveMax)
    idx = difference.index(minimum)

    return array[idx]

if __name__ == '__main__':
    n = int(input())
    arr = list(map(int, input().split()))

    result = getRunnerUp(arr, max(arr))
    print(result)

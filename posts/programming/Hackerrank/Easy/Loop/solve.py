if __name__ == '__main__':
    n = int(input())
    array = [i for i in range(n-1+1)]
    
    res = [pow(i, 2) for i in array]

    print("\n".join(map(str, res)))

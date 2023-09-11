class Solution(object):
    def guessNumber(self, n):
        """
        :type n: int
        :rtype: int
        """
        lower, higher = 1, n
        
        while lower <= higher:
            middle = lower + (higher - lower) // 2
            result = guess(middle)
            
            if result == 0:
                return middle
        
            elif result == -1:
                higher = middle - 1
            
            else:
                lower = middle + 1

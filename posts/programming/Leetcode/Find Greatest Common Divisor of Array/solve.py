class Solution:
    def findGCD(self, nums: List[int]) -> int:
        def gcd(a, b):
            if b == 0:
                return a
            else:
                return gcd(b, a % b)
        
        nums.sort()
        a,b = nums[0], nums[len(nums)-1]
        r = gcd(a, b)

        return r

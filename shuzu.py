#1. 两数之和
class Solution:
	def twoSum(self,nums,target):
		n = len(nums)
		for x in range(n):
			a = target - nums[x]
			if a in nums: # 判断a有没有在nums数组里
				y = nums.index(a) # 有的话，那么用index获取到该数字的下标
				if x == y: 
					continue # 同样的数字不能重复用，所以这里如果是一样的数字，那么就不满足条件，跳过
				else: # 否则就返回结果
					return x,y 
					break
			else: 
				continue

#2. 回文数
def isPalindrome(self, x: int) -> bool:
    return str(x)==str(x)[::-1]
 

#3. 整数反转
class Solution:
    def reverse(self, x: int) -> int:
        s = str(x)
        if s[0] == '-':
            x = int('-' + s[1:][::-1])
        else:
            x = int(s[::-1])
        if x >= 2147483647 or x <= -2147483648: # 判断溢出情况
            return 0
        return x

def twoSum(nums, target):
    for i in range(len(nums)):
        for j in range(len(nums)):
            s = nums[i] + nums[j]
            if s == target:
                return [i, j]

def twoSum_updated(nums, target):
    num_dict = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        
        if complement in num_dict:
            return [num_dict[complement], i]
        
        num_dict[num] = i


if __name__ == "__main__":
    nums = [2, 7, 11, 15]
    target = 9
    print(twoSum_updated(nums, target))  # it returns [0, 1]




# Skip parse input on separate file because these are so short
example = [125, 17]
input = map(int, '0 44 175060 3442 593 54398 9 8101095'.split())

def countOutputs(num, blinks):
    if blinks == 0:
        return 1
    
    if num == 0:
        return countOutputs(1, blinks - 1)
    
    strNum = str(num)
    if len(strNum) % 2 == 0:
        # Split and count
        return (countOutputs(int(strNum[:len(strNum)//2]), blinks - 1) + 
                countOutputs(int(strNum[len(strNum)//2:]), blinks - 1))
    
    return countOutputs(num * 2024, blinks - 1)

def countOutputsWithCaching(num: int, blinks: int, cache: dict[tuple[int, int], int]):
    if blinks == 0:
        return 1
    
    if (num, blinks) in cache:
        # print('Cahce hit! ' + str((num, blinks)))
        return cache[(num, blinks)]
    
    if num == 0:
        result = countOutputsWithCaching(1, blinks - 1, cache)
        cache[(num, blinks)] = result
        return result
    
    strNum = str(num)
    if len(strNum) % 2 == 0:
        # Split and count
        result = (countOutputsWithCaching(int(strNum[:len(strNum)//2]), blinks - 1, cache) + 
                countOutputsWithCaching(int(strNum[len(strNum)//2:]), blinks - 1, cache))
        cache[(num, blinks)] = result
        return result
    
    result = countOutputsWithCaching(num * 2024, blinks - 1, cache)
    cache[(num, blinks)] = result
    return result
        
def part1(nums):
    sum = 0
    for num in nums:
        result = countOutputs(num, 25)
        print('num: ' + str(num) + ' result: ' + str(result))
        sum += result
    return sum

def part2(nums):
    sum = 0
    cache = {}
    for num in nums:
        result = countOutputsWithCaching(num, 75, cache)
        print('num: ' + str(num) + ' result: ' + str(result))
        sum += result
    return sum

print(part2(input))
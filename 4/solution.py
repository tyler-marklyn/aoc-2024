def parseInput(filename):
    """ Turn it into a character[][] """
    file = open(filename, 'r')
    result = []
    for line in file:
        result.append(list(line))
    # print(result)
    return result

directions = {
    'upleft': (-1, -1),
    'up': (-1, 0),
    'upright': (-1, 1),
    'left': (0, -1),
    'right': (0, 1),
    'downleft': (1, -1),
    'down': (1, 0),
    'downright': (1, 1)
}

xmas = list('XMAS')

# point is (row, col) to match grid indexing
def checkXmas(index, point, directionName, grid):
    direction = directions.get(directionName)

    if index == 4:
        # print('Found xmas going: ' + directionName)
        return True
    
    if not (0 <= point[0] < len(grid) and 0 <= point[1] < len(grid[0])):
        return False
    
    if (grid[point[0]][point[1]] != xmas[index]):
        return False
    
    # print('Found letter: ' + xmas[index] + ' at ' + str(point) + ' going ' + directionName)
    return checkXmas(
        index + 1, 
        (point[0] + direction[0], point[1] + direction[1]), 
        directionName, 
        grid)

def part1(input):
    xmasCount = 0
    for row, letters in enumerate(input):
        for col in range(len(letters)):
            for direction in directions.keys():
                if checkXmas(0, (row, col), direction, input):
                    xmasCount += 1
    return xmasCount

def checkMasX(point, grid):
    """ Assumes point is the index of an 'A'"""
    for dirName1, dirName2 in [('upleft', 'downright'), ('upright', 'downleft')]:
        dir1 = directions.get(dirName1)
        dir2 = directions.get(dirName2)
        if not (0 <= point[0] + dir1[0] < len(grid) and
                0 <= point[1] + dir1[1] < len(grid[0]) and
                0 <= point[0] + dir2[0] < len(grid) and
                0 <= point[1] + dir2[1] < len(grid[0])):
            return False
        value1 = grid[point[0] + dir1[0]][point[1] + dir1[1]]
        value2 = grid[point[0] + dir2[0]][point[1] + dir2[1]]
        values = [value1, value2]
        if not ('M' in values and 'S' in values):
            return False
    return True

def part2(input):
    masXCount = 0

    for row, letters in enumerate(input):
        for col, letter in enumerate(letters):
            if letter == 'A':
                if checkMasX((row, col), input):
                    masXCount += 1
    
    return masXCount


print(part2(parseInput('input.txt')))
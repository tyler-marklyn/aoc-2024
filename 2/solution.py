def parseInput():
    inputFile = open('input.txt', 'r')
    result = []

    while line := inputFile.readline():
        split = list(map(int, line.split()))
        result.append(split)

    return result

def part1(input):
    safe = 0

    for line in input:
        safeLine = isLineSafe(line)
        if safeLine:
            safe += 1
    
    return safe

def isLineSafe(line):
    increasing = line[1] - line[0] > 0

    for i in range(1, len(line)):
        if ((increasing and not (1 <= line[i] - line[i - 1] <= 3)) or
            (not increasing and not (-3 <= line[i] - line[i-1] <= -1))):
            return False
    
    return True

def part2(input):
    safe = 0

    for line in input:
        if (isLineSafe(line)):
            safe += 1
            continue

        for i in range(len(line)):
            copy = list(line)
            del copy[i]
            if (isLineSafe(copy)):
                safe += 1
                break

    return safe

print(part2(parseInput()))

# Input is a tuple of result, list of nums
type Input = list[tuple[int, list[int]]]

def parseInput(filename) -> Input:
    file = open(filename, 'r')
    result: Input = []
    for line in file:
        firstSplit = line.split(':')
        secondSplit = list(map(int, firstSplit[1].split()))
        result.append((int(firstSplit[0]), secondSplit))
    return result

def checkLine1(line):
    currentSet = { line[1][0] }

    for number in line[1][1:]:
        sums = map(lambda val: number + val, currentSet)
        prods = map(lambda val: number * val, currentSet)
        currentSet = set(sums).union(prods)

    return line[0] in currentSet

def part1(input: Input):
    sum = 0
    for entry in input:
        if checkLine1(entry):
            sum += entry[0]
    return sum

def checkLine2(line):
    currentSet = { line[1][0] }

    for number in line[1][1:]:
        sums = map(lambda val: number + val, currentSet)
        prods = map(lambda val: number * val, currentSet)
        concats = map(lambda val: int(str(val) + str(number)), currentSet)
        currentSet = set(sums).union(prods).union(concats)

    result = line[0] in currentSet
    return result

def part2(input: Input):
    sum = 0
    for entry in input:
        if checkLine2(entry):
            sum += entry[0]
    return sum

print(part2(parseInput('input.txt')))
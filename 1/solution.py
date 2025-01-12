def parseInput():
    inputFile = open('./input.txt', 'r')
    a = []
    b = []

    while line := inputFile.readline():
        split = line.split()
        a.append(int(split[0]))
        b.append(int(split[1]))

    return (a, b)

def part1(a, b):
    a.sort()
    b.sort()
    diffs = [abs(a[i] - b[i]) for i in range(len(a))]
    return sum(diffs)

def part2(a, b):
    frequencyMap = {}
    for item in b:
        frequencyMap[item] = frequencyMap.get(item, 0) + 1

    return sum([item * frequencyMap.get(item, 0) for item in a])

print(part2(*parseInput()))

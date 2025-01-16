import re

# Map from pages to all the pages that must come before them
type PreMap = dict[int, set[int]]

def parseInput(filename: str) -> tuple[PreMap, list[list[int]]]:
    file = open(filename, 'r')

    # Part 1 -- dependencies
    precedenceMapping: PreMap = {}
    while line := file.readline():
        if line == '\n':
            # Reached second part of input
            break

        match = re.fullmatch(r'(\d+)\|(\d+)\n', line)
        before = int(match[1])
        after = int(match[2])
        current = precedenceMapping.get(after, set())
        current.add(before)
        precedenceMapping[after] = current
    
    # Part 2 -- lists of pages
    pageLists = []

    # We've already read the empty line, so this should start
    # with page lists right away.
    while line := file.readline():
        pageLists.append(list(map(int, line.rstrip().split(','))))
    
    return precedenceMapping, pageLists

def checkList(preMap: PreMap, pageList: list[int]):
    disallowed = set()

    for page in pageList:
        if page in disallowed:
            return False
        disallowed |= preMap.get(page, set())

    return True

def part1(preMap, pageLists):
    sum = 0
    for pageList in pageLists:
        if checkList(preMap, pageList):
            sum += pageList[len(pageList) // 2]
    return sum

def deepCopyDictValues(dict: PreMap) -> PreMap:
    copy = {}

    for key, value in dict.items():
        copy[key] = value.copy()

    return copy

def topoSort(nodes: list[int], edges: PreMap) -> list[int]:
    result = []
    noDeps = set()

    for node in nodes:
        if len(edges.get(node, set())) == 0:
            noDeps.add(node)

    edgesCopy = deepCopyDictValues(edges)

    while len(noDeps) > 0:
        next = noDeps.pop()
        result.append(next)
        
        if next in edgesCopy:
            del edgesCopy[next]

        newNoDeps = set()
        for key, value in edgesCopy.items():
            if next in value:
                value.remove(next)
            if len(value) == 0:
                newNoDeps.add(key)
        for node in newNoDeps:
            del edgesCopy[node]
            noDeps.add(node)

    if len(edgesCopy) != 0:
        print('Cycle?!?')

    return result

def fixList(pageList: list[int], preMap: PreMap):
    pageSet = set(pageList)

    miniPreMap = {}
    for page in pageList:
        if page in preMap:
            miniPreMap[page] = preMap[page] & pageSet

    return topoSort(pageList, miniPreMap)

def part2(preMap, pageLists):
    sum = 0
    for pageList in pageLists:
        if not checkList(preMap, pageList):
            fixedList = fixList(pageList, preMap)
            if len(fixedList) != len(pageList):
                print('ERROR! pages: ' + str(pageList) + ' fixed: ' + str(fixedList))
            sum += fixedList[len(fixedList) // 2]
    return sum

parsedMap, parsedLists = parseInput('input.txt')
print(len(parsedLists))
print(part2(parsedMap, parsedLists))

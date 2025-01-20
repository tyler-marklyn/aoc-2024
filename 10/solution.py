# Just parse as a list of lists of ints
def parseInput(filename) -> list[list[int]]:
    file = open(filename, 'r')
    return [list(map(int, line.strip())) for line in file]

def part1(input: list[list[int]]):
    inputHeight = len(input)
    inputWidth = len(input[0])

    # Build mapping from height -> (row, col)
    heightMap: dict[int, set[tuple[int, int]]] = {}

    for irow, row in enumerate(input):
        for icol, char in enumerate(row):
            currentLocs = heightMap.get(char, set())
            currentLocs.add((irow, icol))
            heightMap[char] = currentLocs
    
    # Map from locations to 9s reachable from that location
    reachableMap: dict[tuple[int,int], set[tuple[int, int]]] = {}

    # Mark all 9s as being able to reach only themselves
    for loc9 in heightMap.get(9, set()):
        reachableMap[loc9] = { loc9 }
    
    # Now iterate 8 -> 0 and check neighbors. Reachable is union of
    # reachable of neighbors that are self + 1
    for height in range(8, -1, -1):
        for locheight in heightMap.get(height, set()):
            neighbors = [
                (locheight[0] - 1, locheight[1]),
                (locheight[0], locheight[1] - 1),
                (locheight[0] + 1, locheight[1]),
                (locheight[0], locheight[1] + 1)
            ]
            reachable = set()
            for neighbor in neighbors:
                if (0 <= neighbor[0] < inputHeight and 
                    0 <= neighbor[1] < inputWidth and
                    input[neighbor[0]][neighbor[1]] == height + 1):
                    # Reachable map should be set for all cells with
                    # greater height
                    reachable |= reachableMap[neighbor]
            reachableMap[locheight] = reachable
    
    # Desired output is sum of number of 9s reachable from 0s
    output = sum([len(reachableMap[loc0]) for loc0 in heightMap.get(0, set())])
    return output

def part2(input):
    inputHeight = len(input)
    inputWidth = len(input[0])

    # Build mapping from height -> (row, col)
    heightMap: dict[int, set[tuple[int, int]]] = {}

    for irow, row in enumerate(input):
        for icol, char in enumerate(row):
            currentLocs = heightMap.get(char, set())
            currentLocs.add((irow, icol))
            heightMap[char] = currentLocs
    
    # Start with 0s and go up to 9s. Keep track of how many
    # paths there are from 0 to that cell.
    pathcount: dict[tuple[int, int], int] = {}

    # 0s all have exactly 1 path
    for loc0 in heightMap.get(0, set()):
        pathcount[loc0] = 1

    # Now iterate height in increasing order. Pathcount is sum
    # of neighbors pathcount if neighbor is this - 1
    for height in range(1, 10):
        for locheight in heightMap.get(height, set()):
            neighbors = [
                (locheight[0] - 1, locheight[1]),
                (locheight[0], locheight[1] - 1),
                (locheight[0] + 1, locheight[1]),
                (locheight[0], locheight[1] + 1)
            ]
            paths = 0
            for neighbor in neighbors:
                if (0 <= neighbor[0] < inputHeight and 
                    0 <= neighbor[1] < inputWidth and
                    input[neighbor[0]][neighbor[1]] == height - 1):
                    # pathcount map should be set for all cells with
                    # lesser height
                    paths += pathcount[neighbor]
            pathcount[locheight] = paths
    
    # Desired output is sum of paths that reach 9s
    output = sum([pathcount[loc9] for loc9 in heightMap.get(9, set())])
    return output

print(part2(parseInput('input.txt')))
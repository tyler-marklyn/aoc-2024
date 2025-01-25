def parseInput(filename):
    file = open(filename, 'r')
    result = []
    for line in file:
        result.append(list(line.strip()))
    return result

def part1(input: list[list[str]]):
    cellsToVisit: set[tuple[int, int]] = set()
    
    for row in range(len(input)):
        for col in range(len(input[0])):
            cellsToVisit.add((row, col))
    
    currentScore = 0
    # Pop a cell, visit its whole region, then update current score,
    # and repeat
    while len(cellsToVisit) > 0:
        currentArea = 0
        currentPerimeter = 0
        currentCell = cellsToVisit.pop()
        currentRegion = input[currentCell[0]][currentCell[1]]
        regionToVisit: set[tuple[int, int]] = { currentCell }

        # Visit cell in region
        while len(regionToVisit) > 0:
            currentCell = regionToVisit.pop()
            # It won't be when we first start a new region
            if currentCell in cellsToVisit:
                cellsToVisit.remove(currentCell)

            currentArea += 1

            neighbors: list[tuple[int, int]] = [
                (currentCell[0] - 1, currentCell[1]),
                (currentCell[0], currentCell[1] - 1),
                (currentCell[0] + 1, currentCell[1]),
                (currentCell[0], currentCell[1] + 1)
            ]

            for neighbor in neighbors:
                if (0 <= neighbor[0] < len(input) and 
                    0 <= neighbor[1] < len(input) and
                    input[neighbor[0]][neighbor[1]] == currentRegion):
                    # Valid neighbor in region, ensure it's in the 
                    # list we need to visit in the region if we haven't
                    # visited it yet
                    if neighbor in cellsToVisit:
                        regionToVisit.add(neighbor)
                else: # not valid neighbor in region
                    currentPerimeter += 1
        
        # Finished region, add to score
        currentScore += currentArea * currentPerimeter

    return currentScore

# Use the realization that number of sides == number of corners
# on a region. Therefore, instead of counting perimeter as we 
# visit a region, we instead check for patterns that make corners
def part2(input: list[list[str]]):
    cellsToVisit: set[tuple[int, int]] = set()
    
    for row in range(len(input)):
        for col in range(len(input[0])):
            cellsToVisit.add((row, col))
    
    currentScore = 0
    # Pop a cell, visit its whole region, then update current score,
    # and repeat
    while len(cellsToVisit) > 0:
        currentArea = 0
        currentCorners = 0
        currentCell = cellsToVisit.pop()
        currentRegion = input[currentCell[0]][currentCell[1]]
        regionToVisit: set[tuple[int, int]] = { currentCell }

        # Visit cell in region
        while len(regionToVisit) > 0:
            currentCell = regionToVisit.pop()
            # It won't be when we first start a new region
            if currentCell in cellsToVisit:
                cellsToVisit.remove(currentCell)

            currentArea += 1

            neighbors: list[tuple[int, int]] = [
                (currentCell[0] - 1, currentCell[1]),
                (currentCell[0], currentCell[1] - 1),
                (currentCell[0] + 1, currentCell[1]),
                (currentCell[0], currentCell[1] + 1)
            ]

            for neighbor in neighbors:
                if (0 <= neighbor[0] < len(input) and 
                    0 <= neighbor[1] < len(input) and
                    input[neighbor[0]][neighbor[1]] == currentRegion and
                    neighbor in cellsToVisit):
                    # Valid neighbor in region, ensure it's in the 
                    # list we need to visit in the region if we haven't
                    # visited it yet
                    regionToVisit.add(neighbor)
            
            # Do corners check on neighbors
            currentCorners += countCorners(currentCell, input)
        
        # Finished region, add to score
        currentScore += currentArea * currentCorners

    return currentScore

def countCorners(cell: tuple[int, int], input: list[list[str]]):
    """
    Let the cell be 'X', cells that match it be 'x' and all other 
    values (including those outside the input) be 'o'

    '.' will represent any value

    The following patterns represent an outside corner:
    .o  o.  Xo  oX
    oX  Xo  o.  .o

    The following patterns represent an inside corner:
    ox  xo  Xx  xX
    xX  Xx  xo  ox

    We check each of the 4 "windows" around X to see if it matches
    one of those patterns, if so we count it as a corner
    """
    cellValue = input[cell[0]][cell[1]]

    vert = {
        'up': cell[0] - 1,
        'mid': cell[0],
        'down': cell[0] + 1
    }

    horiz = {
        'left': cell[1] - 1,
        'mid': cell[1],
        'right': cell[1] + 1
    }

    neighbors: dict[str, tuple[int, int]] = {}

    for vertdir, row in vert.items():
        for horizdir, col in horiz.items():
            neighbors[vertdir + horizdir] = (row, col)
    
    neighborMatches: dict[str, bool] = {}
    for dir, location in neighbors.items():
        validLoc = 0 <= location[0] < len(input) and 0 <= location[1] < len(input[0])
        neighborMatches[dir] = validLoc and input[location[0]][location[1]] == cellValue

    # Count corners
    corners = 0
    # Outside corners
    if not neighborMatches['midleft'] and not neighborMatches['upmid']:
        corners += 1
    if not neighborMatches['midright'] and not neighborMatches['upmid']:
        corners += 1
    if not neighborMatches['midleft'] and not neighborMatches['downmid']:
        corners += 1
    if not neighborMatches['midright'] and not neighborMatches['downmid']:
        corners += 1
    # Inside corners
    if neighborMatches['midleft'] and neighborMatches['upmid'] and not neighborMatches['upleft']:
        corners += 1
    if neighborMatches['midright'] and neighborMatches['upmid'] and not neighborMatches['upright']:
        corners += 1
    if neighborMatches['midleft'] and neighborMatches['downmid'] and not neighborMatches['downleft']:
        corners += 1
    if neighborMatches['midright'] and neighborMatches['downmid'] and not neighborMatches['downright']:
        corners += 1

    return corners

print(part2(parseInput('input.txt')))
# A maze is a tuple of: (height, width, obstacleSet (y, x pairs))
type Maze = tuple[int, int, set[tuple[int, int]]]

# A guard is a tuple of: (y, x, direction(index into directions))
type Guard = tuple[int, int, int]

directions = (
    (-1, 0), # up
    (0, 1), # right
    (1, 0), # down
    (0, -1) # left
)

def parseInput(filename) -> tuple[Maze, Guard]:
    file = open(filename, 'r')

    obstacles = set()
    y = 0
    width = 0
    guard = (-1, -1, -1) # invalid
    firstLine = True

    for line in file:
        if firstLine:
            width = len(line) - 1 # subtract the newline
            firstLine = False

        for x, char in enumerate(line):
            match char:
                case '#':
                    obstacles.add((y, x))
                case '^':
                    guard = (y, x, 0)
                case '>':
                    guard = (y, x, 1)
                case 'v':
                    guard = (y, x, 2)
                case '<':
                    guard = (y, x, 3)
                case _:
                    continue
        
        y += 1
    
    if guard[0] == -1:
        print('Never found guard')
    
    return ((y, width, obstacles), guard)

def doTour(maze: Maze, guard: Guard) -> tuple[set[tuple[int, int]], bool]:
    visitedSet = set()
    previousGuards = set()

    # While guard is on the maze, add to visitedSet then execute a move
    while 0 <= guard[0] < maze[0] and 0 <= guard[1] < maze[1]:
        if guard in previousGuards:
            return visitedSet, True

        visitedSet.add(guard[0:2])
        previousGuards.add(guard)

        newLocation = (
            guard[0] + directions[guard[2]][0], 
            guard[1] + directions[guard[2]][1]
        )

        # If we would move into an obstacle, we just rotate the guard
        if newLocation in maze[2]:
            guard = (guard[0], guard[1], (guard[2] + 1) % 4)
        # Otherwise we move there and don't turn
        else:
            guard = (newLocation[0], newLocation[1], guard[2])
    
    return visitedSet, False

def part1(maze: Maze, guard: Guard):
    visitedSet, _ = doTour(maze, guard)
    return len(visitedSet)

def part2(maze: Maze, guard: Guard):
    visitedSet, _ = doTour(maze, guard)
    cycles = 0

    # Adding obstacles elsewhere doesn't matter
    for location in visitedSet:
        maze[2].add(location)

        _, cycle = doTour(maze, guard)
        if cycle:
            cycles += 1

        # Reset our maze for the next iteration
        maze[2].remove(location)

    return cycles

print(part2(*parseInput('input.txt')))
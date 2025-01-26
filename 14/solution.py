import re
import math

# Position + velocity
type Robot = tuple[tuple[int, int], tuple[int, int]]

def parseInput(filename) -> list[Robot]:
    file = open(filename, 'r')

    result: list[Robot] = []
    robotRegex = r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)\n?'
    for line in file:
        match = re.fullmatch(robotRegex, line)
        result.append(((int(match[1]), int(match[2])), (int(match[3]), int(match[4]))))
    return result

def part1(input: list[Robot], width: int, height: int):
    quadrants = [0] * 4
    xBoundary = (width - 1) / 2.0
    yBoundary = (height - 1) / 2.0
    for robot in input:
        finalX = (robot[0][0] + 100*robot[1][0]) % width
        finalY = (robot[0][1] + 100*robot[1][1]) % height

        if finalX < xBoundary and finalY < yBoundary:
            quadrants[0] = quadrants[0] + 1
        elif finalX > xBoundary and finalY < yBoundary:
            quadrants[1] = quadrants[1] + 1
        elif finalX < xBoundary and finalY > yBoundary:
            quadrants[2] = quadrants[2] + 1
        elif finalX > xBoundary and finalY > yBoundary:
            quadrants[3] = quadrants[3] + 1
    
    return math.prod(quadrants)

def part2(input: list[Robot], width, height, minIterations, maxIterations, step):
    iterations = minIterations
    robots = list(map(
        lambda robot: moveRobotXTimes(robot, minIterations, width, height), 
        input))
    while iterations < maxIterations:
        print(f'Seconds {iterations}:')
        printRobots(map(lambda robot: robot[0], robots), width, height)
        print('\n\n')
        iterations += step
        robots = list(map(lambda robot: moveRobotXTimes(robot, step, width, height), robots))

def moveRobot(robot: Robot, width, height) -> Robot:
    return (
        ((robot[0][0] + robot[1][0]) % width, (robot[0][1] + robot[1][1]) % height),
        robot[1]
    )

def moveRobotXTimes(robot: Robot, times, width, height) -> Robot:
    finalX = (robot[0][0] + times*robot[1][0]) % width
    finalY = (robot[0][1] + times*robot[1][1]) % height
    return ((finalX, finalY), robot[1])

def printRobots(coords: list[tuple[int, int]], width, height):
    counts: dict[tuple[int, int], int] = {}

    for coord in coords:
        current = counts.get(coord, 0)
        counts[coord] = current + 1

    for y in range(height):
        row: list[str] = []
        for x in range(width):
            count = counts.get((x, y), 0)
            row.append(str(count) if count != 0 else '.')
        print(''.join(row))

# print(part1(parseInput('input.txt'), 101, 103))
part2(parseInput('input.txt'), 101, 103, 418, 10000, 101)
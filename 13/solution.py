import re
import math

# Machine is stored as 
# [(buttonA.X, ButtonA.y), (buttonB.x, buttonB.y), (prize.x, prize.y)]
type Machine = list[tuple[int, int]]

def parseInput(filename) -> list[Machine]:
    file = open(filename, 'r')

    machines: list[Machine] = []
    lineRegex = r'.+X[+=](\d+), Y[+=](\d+)\n?'
    while line := file.readline():
        # Skip blank line between machines
        if line == '\n':
            continue

        machine: Machine = []
        for _ in range(3):
            match = re.fullmatch(lineRegex, line)
            if match == None:
                print('Parsing error on line: ' + line)
                return []
            machine.append((int(match[1]), int(match[2])))
            line = file.readline()

        machines.append(machine)

    return machines

def checkMachine(machine: Machine):
    workingCombos: set[tuple[int, int]] = set()

    # Problem states that 100 is the max
    for aPushes in range(100):
        if (machine[0][0] * aPushes > machine[2][0] or 
            machine[0][1] * aPushes > machine[2][1]):
            break

        remainingX = machine[2][0] - machine[0][0] * aPushes
        remainingY = machine[2][1] - machine[0][1] * aPushes

        # No valid B number
        if remainingX % machine[1][0] != 0:
            continue

        bPushes = remainingX // machine[1][0]
        
        # B number also valid for Y
        if bPushes * machine[1][1] == remainingY:
            workingCombos.add((aPushes, bPushes))

    bestCombo = min(
        workingCombos, 
        default=(-1, -1), 
        key=lambda combo: combo[0]*3 + combo[1])
    return bestCombo[0]*3 + bestCombo[1] if bestCombo[0] != -1 else 0

def part1(input: list[Machine]):
    return sum(map(checkMachine, input))

def modifyMachine(machine: Machine):
    extraPrizeCoords = 10000000000000
    machineCopy = machine.copy()
    machineCopy[2] = (machine[2][0] + extraPrizeCoords, 
                      machine[2][1] + extraPrizeCoords)
    return machineCopy

def part2(input: list[Machine]):
    modifiedInputs = map(modifyMachine, input)
    return sum(map(efficientCheckMachine, modifiedInputs))

def efficientCheckMachine(machine):
    soln = solve_optimized_diophantine(machine[0][0],
                                       machine[1][0],
                                       machine[2][0],
                                       machine[0][1],
                                       machine[1][1],
                                       machine[2][1])
    
    print('Got result for machine: ' + str(machine) + ' Result: ' + str(soln))

    if soln == None:
        return 0
    
    return soln[0]*3 + soln[1]

# Entirely written by Claude after some back and forth asking
# for this function
def solve_positive_diophantine_system(a, b, c, d, e, f):
    """
    Solve system of Diophantine equations with positive integer constraints:
    ax + by = c
    dx + ey = f
    """
    # Compute GCDs
    gcd_ab = math.gcd(a, b)
    gcd_de = math.gcd(d, e)
    
    # Check solvability
    if c % gcd_ab != 0 or f % gcd_de != 0:
        return []
    
    # Reduce search space more aggressively
    max_x = max(c // a, f // d) + 1
    max_y = max(c // b, f // e) + 1
    
    solutions = []
    for x in range(1, max_x):
        for y in range(1, max_y):
            if a*x + b*y == c and d*x + e*y == f:
                solutions.append((x, y))
    
    return solutions

def solve_optimized_diophantine(a, b, c, d, e, f):
    """
    Solve ax + by = c and dx + ey = f, minimizing 3x + y
    Assumes positive integer constraints
    """
    def extended_gcd(a, b):
        if b == 0:
            return a, 1, 0
        gcd, x1, y1 = extended_gcd(b, a % b)
        return gcd, y1, x1 - (a // b) * y1

    # Check solvability
    gcd1 = math.gcd(a, b)
    gcd2 = math.gcd(d, e)
    if c % gcd1 != 0 or f % gcd2 != 0:
        return None

    # Solve first equation
    gcd1, m, n = extended_gcd(a, b)
    m *= c // gcd1
    n *= c // gcd1

    # Search for solutions that minimize 3x + y
    best_solution = None
    best_cost = float('inf')

    for k in range(-1000, 1000):  # Adjust range as needed
        x = m + k * (b // gcd1)
        y = n - k * (a // gcd1)

        # Check second equation
        if d*x + e*y == f and x > 0 and y > 0:
            cost = 3*x + y
            if cost < best_cost:
                best_solution = (x, y)
                best_cost = cost

    return best_solution

print(part2(parseInput('example.txt')))
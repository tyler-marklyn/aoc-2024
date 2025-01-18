import math

# Map has height, width, antenna dictionary
type Map = tuple[int, int, dict[str, list[tuple[int, int]]]]

def parseInput(filename) -> Map:
    file = open(filename, 'r')
    finalRow = 0
    width = 0
    antennas = {}
    for row, line in enumerate(file):
        finalRow = row
        if row == 0:
            width = len(line) - 1
        
        for col, char in enumerate(line):
            if char not in '.\n':
                currentList = antennas.get(char, [])
                currentList.append((row, col))
                antennas[char] = currentList

    return finalRow + 1, width, antennas

def part1(map: Map):
    antinodes = set()

    # Iterate over all pairs of nodes in each set of antenna chars,
    # find the 2 antinodes and add them to the set
    for nodelist in map[2].values():
        for iloc, loc in enumerate(nodelist):
            for otherloc in nodelist[iloc+1:]:
                rowdiff = otherloc[0] - loc[0]
                coldiff = otherloc[1] - loc[1]
                antinode1 = (loc[0] - rowdiff, loc[1] - coldiff)
                antinode2 = (otherloc[0] + rowdiff, otherloc[1] + coldiff)
                for antinode in [antinode1, antinode2]:
                    if 0 <= antinode[0] < map[0] and 0 <= antinode[1] < map[1]:
                        antinodes.add(antinode)

    # printMapWithAntinodes(map, antinodes)
    return len(antinodes)

def printMapWithAntinodes(map, antinodes):
    for row in range(map[0]):
        currRow = []
        for col in range(map[1]):
            foundNode = False
            for char in map[2]:
                if (row, col) in map[2][char]:
                    currRow.append(char)
                    foundNode = True
            if (row, col) in antinodes:
                if not foundNode:
                    currRow.append('#')
                else:
                    currRow[col] = '*'
            elif not foundNode:
                currRow.append('.')

        stringrow = ''.join(currRow)
        print(stringrow)

def part2(map: Map):
    antinodes = set()

    # Iterate over all pairs of nodes in each set of antenna chars,
    # figure out the slope, and then add all antinodes to the set
    for nodelist in map[2].values():
        for iloc, loc in enumerate(nodelist):
            for otherloc in nodelist[iloc+1:]:
                rowdiff = otherloc[0] - loc[0]
                coldiff = otherloc[1] - loc[1]

                # Get the integer slope
                gcd = math.gcd(rowdiff, coldiff)
                rowchange = rowdiff/gcd
                colchange = coldiff/gcd

                # Go one way
                currRow = loc[0]
                currCol = loc[1]
                while 0 <= currRow < map[0] and 0 <= currCol < map[1]:
                    antinodes.add((currCol, currRow))
                    currRow += rowchange
                    currCol += colchange

                # Then the other
                currRow = loc[0]
                currCol = loc[1]
                while 0 <= currRow < map[0] and 0 <= currCol < map[1]:
                    antinodes.add((currCol, currRow))
                    currRow -= rowchange
                    currCol -= colchange

    # printMapWithAntinodes(map, antinodes)
    return len(antinodes)


print(part2(parseInput('input.txt')))

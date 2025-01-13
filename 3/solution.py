import re

def parseInput():
    inputFile = open('input.txt', 'r')
    return inputFile.read()

def part1(input):
    muls = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', input)
    sum = 0
    for match in muls:
        product = int(match[0]) * int(match[1])
        sum += product
    return sum

def part2(input):
    sum = 0
    do = True
    allfinds = re.findall(r"(mul|don't|do)\(([^)]*)\)", input)
    for found in allfinds:
        match found:
            case ('do', ''):
                do = True
            case ("don't", ''):
                do = False
            case ('mul', args):
                factors = re.fullmatch(r"(\d{1,3}),(\d{1,3})", args)
                if do and factors:
                    sum += int(factors[1]) * int(factors[2])
            case _:
                continue
    return sum

print(part2(parseInput()))
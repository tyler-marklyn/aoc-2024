def parseInput(filename):
    file = open(filename, 'r')
    return file.read()

def part1(input):
    # Ignore trailing empty space if it exists
    if len(input) % 2 == 0:
        input = input[:-1]

    leftInputIndex = 0
    rightInputIndex = len(input) - 1
    leftMemoryIndex = 0
    rightMemoryIndex = sum(map(int, input))
    leftRemaining = int(input[0])
    rightRemaining = int(input[-1])
    leftFileId = 0
    rightFileId = len(input) // 2
    inEmptySpace = False

    checksum = 0

    while leftFileId < rightFileId:
        # Iterate over final memory, go until we reach end of file
        while leftRemaining > 0 and rightRemaining > 0:
            if not inEmptySpace:
                # Update checksum with file from left
                checksum += leftFileId * leftMemoryIndex

            else: # In empty space
                # Update checksum with file from right that
                # we have theoretically moved into empty space
                checksum += rightFileId * leftMemoryIndex
                # Update right indices
                rightRemaining -= 1
                rightMemoryIndex -= 1
            
            # We always update left indices
            leftRemaining -= 1
            leftMemoryIndex += 1
        
        # When we leave the inner while loop, we have reached the 
        # end of a file, update as necessary

        if leftRemaining == 0:
            inEmptySpace = not inEmptySpace # Flip
            leftInputIndex += 1
            leftRemaining = int(input[leftInputIndex])

            # If we just moved out of empty space, update file ID
            if not inEmptySpace:
                leftFileId += 1
        
        if rightRemaining == 0:
            # Assume right is always in a file, so first we skip empty space
            rightInputIndex -= 1
            emptySpace = int(input[rightInputIndex])
            rightMemoryIndex -= emptySpace
            # And now we're in a file again
            rightInputIndex -= 1
            rightFileId -= 1
            rightRemaining = int(input[rightInputIndex])

    # Loop ends when left and right are in the same file. We just have to go
    # until we reach the right memory index now
    while leftMemoryIndex < rightMemoryIndex:
        checksum += leftFileId * leftMemoryIndex
        leftMemoryIndex += 1

    return checksum

# Return index of first item in iterable that meets condition
# (basically the typescript find function)
def find(frees, targetSize):
    for i, free in enumerate(frees):
        if free[1] >= targetSize:
            return i, free
    return -1, None

def part2(input):
    # In this version, files and free spaces are always contiguous,
    # so we build a list of each, and then do the movement algorithm

    # Files map from fileId to (startingIndex, length)
    files: dict[int, tuple[int, int]] = {}
    # Free list will always be sorted by starting index
    # Free item is (startingIndex, length)
    frees: list[tuple[int, int]] = []

    # Build our starting memory layout
    fileId = 0
    memIndex = 0
    inFree = False
    for char in input:
        length = int(char)
        if inFree:
            frees.append((memIndex, length))
        else:
            files[fileId] = (memIndex, length)
            fileId += 1
        memIndex += length
        inFree = not inFree
    
    # Do movement
    fileId -= 1 # We ended up 1 past the end
    while fileId > 0:
        file = files[fileId]
        # Try to move the file
        ifreeBlock, freeBlock = find(frees, file[1])
        if ifreeBlock != -1 and freeBlock[0] < file[0]:
            # Update the free block
            remainingFree = freeBlock[1] - file[1]
            if remainingFree == 0:
                # Remove the block
                frees.pop(ifreeBlock)
            else:
                frees[ifreeBlock] = (freeBlock[0] + file[1], freeBlock[1] - file[1])
            
            # Update the file
            files[fileId] = (freeBlock[0], file[1])
        
        # Move on to the next file
        fileId -= 1

    # printFilesLikeExample(files, memIndex)
    # Calculate checksum by only iterating files, since free is always 0
    checksum = 0
    for fileId, file in files.items():
        for memIndex in range(file[0], file[0] + file[1]):
            checksum += memIndex * fileId

    return checksum

def printFilesLikeExample(files: dict[int, tuple[int, int]], memSize: int):
    outputList = ['.'] * memSize
    for fileId, file in files.items():
        for i in range(file[0], file[0]+file[1]):
            outputList[i] = str(fileId)
    output = ''.join(outputList)
    print(output)

print(part2(parseInput('input.txt')))
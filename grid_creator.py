def makeLRGrid(size):

    grid = []
    for _ in range(size):
        grid.append([])
        for _ in range(size):
            grid[-1].append(0)
    return grid

def main():
    size = 40
    start = (0,0)
    end = (size-1,size-1)
    maze = makeLRGrid(size)
    file = open("grid_test.py", "w")
    file.write("%s = %s\n" %("maze", maze))
    file.write("%s = %s\n" %("start", start))
    file.write("%s = %s\n" %("end", end))
    file.close()

if __name__ == '__main__':
    main()
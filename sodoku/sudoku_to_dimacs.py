# Sudoku as a SAT Problem
"""
Inˆes Lynce
IST/INESC-ID, Technical University of Lisbon, Portugal
ines@sat.inesc-id.pt
Jo¨el Ouaknine
Oxford University Computing Laboratory, UK
joel@comlab.ox.ac.uk
"""

# Quang Lam

import sys

def s(x, y, z):
    return 81 * (x - 1) + 9 * (y - 1) + z

def main():
    i = -1
    grid = []
    for x in open(sys.argv[1], 'r'):
        grid.append(x.strip().split())
    
    clauses = []
    
    # There is at least one number in each entry:
    for x in range(1, 10):
        for y in range(1, 10):
            arr = []
            for z in range(1, 10):
                arr.append(s(x, y, z))
            clauses.append(arr)

    # Each number appears at most once in each row:
    for y in range(1, 10):
        for z in range(1, 10):
            for x in range(1, 9):
                for i in range(x + 1, 10):
                    clauses.append([-s(x, y, z), -s(i, y, z)])

    # Each number appears at most once in each column:
    for x in range(1, 10):
        for z in range(1, 10):
            for y in range(1, 10):
                for i in range(y + 1, 10):
                    clauses.append([-s(x, y, z), -s(x, i, z)])

    # Each number appears at most once in each 3x3 sub-grid:
    for z in range(1, 10):
        for i in range(0, 3):
            for j in range(0, 3):
                for x in range(1, 4):
                    for y in range(1, 4):
                        for k in range(y + 1, 4):
                            clauses.append([-s(3 * i + x, 3 * j + y, z), -s(3 * i + x, 3 * j + k, z)])
                        for k in range(x + 1, 4):
                            for l in range(1, 4):
                                clauses.append([-s(3 * i + x, 3 * j + y, z), -s(3 * i + k, 3 * j + l, z)])

    # Unit Clauses
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 'x':
                print(i, j, grid[i][j])
                x = i + 1
                y = j + 1
                z = int(grid[i][j])
                clauses.append([s(x, y, z)])    

    # Print
    f = open('sudoku.dimacs', 'w')

    f.write(' '.join(['p', 'cnf', str(9 * 9 * 9), str(len(clauses))]) + '\n')
    
    for clause in clauses:
        f.write(' '.join(str(x) for x in clause) + ' 0\n')

    f.close()
    

if __name__ == '__main__':
    main()
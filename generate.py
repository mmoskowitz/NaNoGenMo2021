#!/usr/bin/env python

import grimdrake.Grid
import grimdrake.Filler
import copy

basegrid = grimdrake.Grid.Grid(15, 15)
basefiller = grimdrake.Filler.Filler()
basefiller.full_auto = True

for row in range(7):
    for column in range(7):
        basegrid.fillspace(column * 2 + 1, row * 2 + 1)

#iterating through black squares

blocks = (5,7,9)
vals = (0,2,4,6)

def iterate_across(grid, level):
    if level < 4:
        for block in blocks:
            new_grid = copy.deepcopy(grid)
            new_grid.fillspace(block, vals[level])
            new_grid.fillspace(14-block, 14-vals[level])
            iterate_across(new_grid, level + 1)
    else:
        iterate_down(grid, 0)

def iterate_down(grid, level):
    if level < 4:
        for block in blocks:
            new_grid = copy.deepcopy(grid)
            new_grid.fillspace(vals[level], block)
            new_grid.fillspace(14-vals[level], 14-block)
            iterate_down(new_grid, level + 1)
    else:
        if (is_contiguous(grid)):
            fill_grid(grid)

"""very reliant on our specific grid format"""
def is_contiguous(grid):
    #horizontal breaks
    if (grid.isblack(0,5) and grid.isblack(2,5) and grid.isblack(4,5)):
        #top left corner
        if (grid.isblack(5,0) and grid.isblack(5,2) and grid.isblack(5,4)):
            return False
        #double jog through center
        if (grid.isblack(5,6) and grid.isblack(6,7)):
            return False
        if (grid.isblack(6,5)):
            #jog through center
            if (grid.isblack(7,6)):
                return False
            #top left 7x5
            if (grid.isblack(7,0) and grid.isblack(7,2) and grid.isblack(7,4)):
                return False
    #straight bisect
    if (grid.isblack(0,7) and grid.isblack(2,7) and grid.isblack(4,7) and grid.isblack(6,7)):
        return False
    if (grid.isblack(0,9) and grid.isblack(2,9) and grid.isblack(4,9)):
        #top right corner
        if (grid.isblack(9,0) and grid.isblack(9,2) and grid.isblack(9,4)):
            return False
        #double jog through center
        if (grid.isblack(9,6) and grid.isblack(6,7)):
            return False
        if (grid.isblack(6,9)):
            #jog through center
            if (grid.isblack(7,6)):
                return False
            #top right 7x5
            if (grid.isblack(7,0) and grid.isblack(7,2) and grid.isblack(7,4)):
                return False

    #vertical breaks
    if (grid.isblack(5,0) and grid.isblack(5,2) and grid.isblack(5,4)):
        #double jog through center
        if (grid.isblack(6,5) and grid.isblack(7,6)):
            return False
        if(grid.isblack(5,6)):
            #jog through center
            if (grid.isblack(6,7)):
                return False
            #top left 5x7
            if (grid.isblack(0,7) and grid.isblack(2,7) and grid.isblack(4,7)):
                return False
    #straight bisect
    if (grid.isblack(7,0) and grid.isblack(7,2) and grid.isblack(7,4) and grid.isblack(7,6)):
        return False
    if (grid.isblack(9,0) and grid.isblack(9,2) and grid.isblack(9,4)):
        #double jog through center
        if (grid.isblack(8,5) and grid.isblack(7,6)):
            return False
        if (grid.isblack(9,6)):
            #jog through center
            if (grid.isblack(6,7)):
                return False
            #top right 5x7
            if (grid.isblack(14,7) and grid.isblack(12,7) and grid.isblack(10,7)):
                return False

    #all passed, grid is continuous
    return True

def fill_grid(grid):
    filler = copy.deepcopy(basefiller)
    filler.set_grid(grid)
    success = filler.fill()
    if (success):
        handle_filled(filler)
    else:
        print "FAILED"
        filler.printgrid()
        print "FAILED TO FILL"

def handle_filled(filler):
    print "Success!"
    filler.printgrid()
    entries = {}
    entries[0] = {}
    entries[1] = {}
    for entry in filler.entrylist:
        entries[entry[0]][entry[1]] = entry[2]
    for dir in (1, 0):
        print dir
        for num in range(33):
            if (num in entries[dir]):
                print num, entries[dir][num]
        
iterate_across(basegrid, 0)


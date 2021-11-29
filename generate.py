#!/usr/bin/env python

import grimdrake.Grid
import grimdrake.Filler
import copy
import sys

class Generator:

    basegrid = grimdrake.Grid.Grid(15, 15)
    basefiller = grimdrake.Filler.Filler()
    basefiller.full_auto = True

    for row in range(7):
        for column in range(7):
            basegrid.fillspace(column * 2 + 1, row * 2 + 1)

    #iterating through black squares

    blocks = (5,7,9)
    vals = (0,2,4,6)

    index = 0
    across_blocks = [0,0,0,0]
    down_blocks = [0,0,0,0]

    target = "target"

    def generate(self):
        self.iterate_across(self.basegrid, 0)
    
    def iterate_across(self, grid, level):
        if level < 4:
            for block in self.blocks:
                new_grid = copy.deepcopy(grid)
                new_grid.fillspace(block, self.vals[level])
                new_grid.fillspace(14-block, 14-self.vals[level])
                self.across_blocks[level] = str(block)
                self.iterate_across(new_grid, level + 1)
        else:
            self.iterate_down(grid, 0)

    def iterate_down(self, grid, level):
        if level < 4:
            for block in self.blocks:
                new_grid = copy.deepcopy(grid)
                new_grid.fillspace(self.vals[level], block)
                new_grid.fillspace(14-self.vals[level], 14-block)
                self.down_blocks[level] = str(block)
                self.iterate_down(new_grid, level + 1)
        else:
            if (self.is_contiguous(grid)):
                self.fill_grid(grid)

    """very reliant on our specific grid format"""
    def is_contiguous(self, grid):
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

    def fill_grid(self, grid):
        filler = copy.deepcopy(self.basefiller)
        filler.set_grid(grid)
        success = filler.fill()
        if (success):
            self.handle_filled(filler)
        else:
            print "FAILED"
            filler.printgrid()
            print "FAILED TO FILL"
            sys.exit()

    def handle_filled(self, filler):
        print "Success!"
        self.index += 1
        blocks = self.across_blocks + self.down_blocks
        code = "-".join(blocks)
        print self.index, code
        filename = "{}/{}.txt".format(self.target, code)
        f = open(filename, "w")
        f.write("{} {}".format(self.index, code) + "\n")
        filler.printgrid(f)
        entries = {}
        entries[0] = {}
        entries[1] = {}
        for entry in filler.entrylist:
            entries[entry[0]][entry[1]] = entry[2]
        for dir in (1, 0):
            f.write(str(dir) + "\n")
            for num in range(33):
                if (num in entries[dir]):
                    f.write("{} {}".format(num, entries[dir][num]) + "\n")
        f.close()

def main():
     generator = Generator()
     generator.generate()

if (__name__ == "__main__"):
    main() 


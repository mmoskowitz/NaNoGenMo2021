#!/usr/bin/env python

import sys, re
import fileinput

class LayerOut:

    """A grid is a dict containing:
    number: a number like 6121
    code: a code that looks like "9-9-9-9-5-5-5-5"
    lights: a list of fifteen strings that look like "disbelief comes" or "r i d n i h a u"
    across: a list of across entries that look like "1. disbelief"
    down: a list of down entries that look like "1. droop"
    """
    grids = []
    currentgrid = None
    currententries = None

    title_re = re.compile(r'\d+ \d-\d-\d-\d-\d-\d-\d-\d')
    entry_re = re.compile(r'\d+ \w+')
    entryhead_re = re.compile(r'[10]')
    space_re = re.compile(r'\s')
    
    def layout(self):
        self.parse()
        self.setupvolume()
        self.writepages()
        #print self.grids

    def parse(self):
        for line in fileinput.input():
            self.parseline(line)

    def parseline(self, line):
        if ('+' in line):
            return
        if ('_' in line):
            return
        if ('--' in line):
            return
        if (self.title_re.match(line)):
            self.parsetitle(line)
            return
        if ('|' in line):
            self.parselights(line)
            return
        if (self.entry_re.match(line)):
            self.parseentry(line)
            return
        if (self.entryhead_re.match(line)):
            self.parseentryhead(line)
            return
        else:
            print ("unparsed line:", line)
            return

    def parsetitle(self, line):
        #start new grid
        self.currentgrid = {}
        self.grids.append(self.currentgrid)
        self.currentgrid['lights'] = []
        self.currentgrid['across'] = []
        self.currentgrid['down'] = []
        parts = re.split(self.space_re, line)
        self.currentgrid['number'] = parts[0]
        self.currentgrid['code'] = parts[1]
        return

    def parselights(self, line):
        light = "".join([line[i] for i in range(1, len(line) - 1, 2)])
        self.currentgrid['lights'].append(light)
        return

    def parseentryhead(self, line):
        if ('1' in line):
            self.currententries = self.currentgrid['across']
        else:
            self.currententries = self.currentgrid['down']
        return

    def parseentry(self, line):
        parts = re.split(self.space_re, line)
        self.currententries.append(parts[0] + ". " + parts[1])
        return

    #layout section
    include = []
    title = ""
    volume = ""
    
    def setupvolume(self):
        f = open("include.ps","r")
        self.include = f.readlines()
        f.close()
        
        across1len = self.grids[0]['code'][0]
        if (across1len == "5"):
            self.volume = "I"
        if (across1len == "7"):
            self.volume = "II"
        if (across1len == "9"):
            self.volume = "III"
        self.title = "Volume {}: 1-Across Length = {}".format(self.volume, across1len)

    def writepages(self):
        filename = "target/vol{}.ps".format(self.volume)
        f = open(filename, "w")

        pages = int(len(self.grids) / 2)

        #prolog
        f.write("%!PS-Adobe-3.0\n")
        f.write("%%Pages: {}\n".format(pages + 2))
        for line in self.include:
            f.write(line)
            
        #setup
        f.write("%%BeginSetup\n")
        f.write("/volumetitle ({}) def\n".format(self.title))
        f.write("%%EndSetup\n")
            
        #pages
        #title page
        f.write("\n");
        f.write("%%Page: {} {}\n".format(1, 1))
        f.write("/pagenum ({}) def\n".format(1, 1))
        f.write("drawtitlepage\n")

        #blank page
        f.write("\n");
        f.write("%%Page: {} {}\n".format(2, 2))
        f.write("/pagenum ({}) def\n".format(2))
        f.write("/recto false def\n")
        f.write("drawblankpage\n")

        #grids
        for page in range(pages):
            f.write("\n");
            f.write("%%Page: {} {}\n".format(page + 3, page + 3))
            f.write("/pagenum ({}) def\n".format(page+3))
            if (page  % 2 == 0):
                f.write("/recto true def\n")
            else:
                f.write("/recto false def\n")
            even = len(self.grids) > page*2 + 1
            pagegrids = [self.grids[page*2]]
            if (even):
                pagegrids.append(self.grids[page*2 + 1])
            for i in range(len(pagegrids)):
                grid = pagegrids[i]
                #squares
                f.write("/squares{} [\n".format(i));
                for line in grid["lights"]:
                    f.write("[ ")
                    for letter in line:
                        if letter == " ":
                            f.write ("0 ")
                        else:
                            f.write("1 ")
                    f.write("]\n")
                f.write("] def\n")
                
                #title
                f.write("/title{} (Grid #{}: {}) def\n".format(i, grid["number"], grid["code"]))
                
                #entries
                f.write("/entries{} [\n".format(i))
                f.write("[\n")
                for entry in grid["across"]:
                    f.write("({})\n".format(entry.upper()))
                f.write("][\n")
                for entry in grid["down"]:
                    f.write("({})\n".format(entry.upper()))
                f.write("]\n")
                f.write("] def\n")
            if (even):
                f.write("drawpage\n")
            else:
                f.write("drawhalfpage\n")
                    
        f.write("%%EOF\n")
        f.close()
        
                 
    

def main():
     layerout = LayerOut()
     layerout.layout()

if (__name__ == "__main__"):
    main() 


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

try:
    import scribus
except ImportError as err:
    print ("This Python script is written for the Scribus scripting interface.")
    print ("It can only be run from within Scribus.")
    sys.exit(1)

import math

def dbg(s):
    scribus.messageBox("Debug", s)

def main(argv):
    """This is a documentation string. Write a description of what your code
    does here. You should generally put documentation strings ("docstrings")
    on all your Python functions."""

    margins = scribus.getPageMargins() # (T, L, R, B)
    marginTop = margins[0]
    marginBottom = margins[3]

    lineSpacing = scribus.valueDialog("Line Spacing", "Input desired line spacing", '0')
    if not lineSpacing:
        sys.exit(0)
    lineSpacing = float(lineSpacing)

    offset = scribus.valueDialog(
            "Offset",
            "Input desired vertical offset from top margin", "0")
    if not offset:
        sys.exit(0)
    offset = float(offset) + marginTop

    pageHeight = scribus.getPageSize()[1] - marginTop - offset
    nLines = math.ceil(pageHeight / lineSpacing)

    scribus.progressTotal(nLines)
    scribus.statusMessage("Generating guides...")
    
    guides = []

    for i in range(nLines):
        scribus.progressSet(i)
        y = offset + (lineSpacing * i)
        if y != marginTop and y < scribus.getPageSize()[1] - marginBottom:
            guides.append(y)

    scribus.setHGuides(guides)

def main_wrapper(argv):
    try:
        scribus.statusMessage("Running script...")
        scribus.progressReset()
        main(argv)
    finally:
        if scribus.haveDoc():
            scribus.setRedraw(True)
        scribus.statusMessage("")
        scribus.progressReset()

if __name__ == '__main__':
    main_wrapper(sys.argv)
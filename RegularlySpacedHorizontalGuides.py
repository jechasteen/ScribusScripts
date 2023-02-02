#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

try:
    # Please do not use 'from scribus import *' . If you must use a 'from import',
    # Do so _after_ the 'import scribus' and only import the names you need, such
    # as commonly used constants.
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
    
    # Get line spacing, and offset from user
    # (pageHeight - offset) / lineSpacing - 1 = n lines
    # compute y values offset, offset + lineSpacing(n)

    margins = scribus.getPageMargins() # (T, L, R, B)
    marginTop = margins[0]
    marginBottom = margins[3]

    lineSpacing = float(
        scribus.valueDialog("Line Spacing", "Input desired line spacing", '0'))
    offset = float(
        scribus.valueDialog(
            "Offset",
            "Input desired vertical offset from top margin", "0")) + marginTop
    pageHeight = scribus.getPageSize()[1] - marginTop - offset
    nLines = math.ceil(pageHeight / lineSpacing)

    dbg("nLines: " + str(nLines))

    guides = []

    for i in range(nLines):
        y = offset + (lineSpacing * i)
        if y != marginTop and y < scribus.getPageSize()[1] - marginBottom:
            guides.append(y)

    scribus.setHGuides(guides)

def main_wrapper(argv):
    """The main_wrapper() function disables redrawing, sets a sensible generic
    status bar message, and optionally sets up the progress bar. It then runs
    the main() function. Once everything finishes it cleans up after the main()
    function, making sure everything is sane before the script terminates."""
    try:
        scribus.statusMessage("Running script...")
        scribus.progressReset()
        main(argv)
    finally:
        # Exit neatly even if the script terminated with an exception,
        # so we leave the progress bar and status bar blank and make sure
        # drawing is enabled.
        if scribus.haveDoc():
            scribus.setRedraw(True)
        scribus.statusMessage("")
        scribus.progressReset()

# This code detects if the script is being run as a script, or imported as a module.
# It only runs main() if being run as a script. This permits you to import your script
# and control it manually for debugging.
if __name__ == '__main__':
    main_wrapper(sys.argv)
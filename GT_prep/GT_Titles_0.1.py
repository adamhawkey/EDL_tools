#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
usage: GT_Titles_0.1.py <inputEDL> <outputEDL>
"""

# This script is very specific to the show Good Trouble.
# Incredibly specific to the titles EDL's that come from their editorial dept.

import sys
import shutil
import os
import re

print(sys.argv[0])
if len(sys.argv) < 2:
    print('Not enough arguments.', __doc__)
    sys.exit()

inputEDL, outputEDL = sys.argv[1:]

shutil.copy(inputEDL, outputEDL)

regex = (r"^([0-9]{3})([ ]+)(BL)(    V     C        )(00:00:00:00 00:00:00:00)[ ]+([0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2})(.[0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2})(.*)\n"
	r"([0-9]{3})(.*)\n"
	r"(\*)(.*)\n"
	r"(\*)(.*)\n"
	r"([0-9]{3})([ ]+BL    V     C)(.*)$\n"
	r"(\*)(.*)\n"
	r"([0-9]{3})(.*)\n"
	r"([0-9]{3})([ ]+BL    V     D    012 )(00:00:00:00 00:00:00:12)[ ]+([0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2})( [0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2})(.*)$\n"
	r"(.*)\n"
	r"(.*)")

subst = "\\1\\2GT_OT\\4\\5 \\6\\26"

edlIn = open(inputEDL, "r")
edl = edlIn.read()
edlOut = open(outputEDL, "w")
# You can manually specify the number of replacements by changing the 4th argument
result = re.sub(regex, subst, edl, 0, re.MULTILINE)

if result:
    edlOut.write(result)
    edlOut.close()

# Somehow, we need to convert in the BBEdit Grep of:
'''
grep
^([0-9]{3})([ ]+BL    V     C)([ ]+00:00:00:00 00:00:00:00)[ ]+([0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2})( [0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2})(.*)$
([0-9]{3})(.*)
(\*)(.*)
(\*)(.*)
([0-9]{3})([ ]+BL    V     C)(.*)$
(\*)(.*)
([0-9]{3})(.*)
([0-9]{3})([ ]+BL    V     D    012 )(00:00:00:00 00:00:00:12)[ ]+([0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2})( [0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2})(.*)$
(.*)
(.*)\n
replace
\1\2\3 \4\24
'''

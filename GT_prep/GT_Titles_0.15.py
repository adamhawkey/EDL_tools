#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
usage: GT_Titles_0.2.py <inputEDL> <outputEDL>
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

#shutil.copy(inputEDL, outputEDL)

BLevents = (r"^([0-9]{3})([ ]+)(BL)(.*)\n"
	r"(\*)( SOURCE FILE: \(NULL\))")
subst = ""

regex1 = (r"^([0-9]{3})([ ]+)(BL)(    V     C        )(00:00:00:00 00:00:00:00)[ ]+([0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2})(.[0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2})(.*)\n"
	r"([0-9]{3})(.*)\n"
	r"(\*)(.*)\n"
	r"(\*)(.*)\n"
	r"(\*)(.*)\n"
	r"([0-9]{3})([ ]+)([A-Za-z0-9_\-]+)( V     C        )(.*)$\n"
	r"(\*)(.*)\n"
	r"(\*)(.*)\n"
	r"([0-9]{3})(.*)\n"
	r"([0-9]{3})([ ]+BL    V     D    012 )(00:00:00:00 00:00:00:12)[ ]+([0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2})( [0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2})(.*)$\n"
	r"(.*)\n"
	r"(.*)\n"
	r"(.*)")

test_str = ("002     BL    V     C        00:00:00:00 00:00:00:00 00:03:13:16 00:03:13:16 \n"
	"002  1_-_NAME V     D    012 01:00:00:00 01:00:00:12 00:03:13:16 00:03:14:04 \n"
	"* BLEND, DISSOLVE \n"
	"* TO CLIP NAME:  1 - NAME ONLY - RIGHT.PNG \n"
	"* SOURCE FILE: (NULL)\n"
	"003  1__NAME V     C        01:00:00:12 01:00:02:12 00:03:14:04 00:03:16:04 \n"
	"* FROM CLIP NAME:  1 - NAME ONLY - RIGHT.PNG \n"
	"* SOURCE FILE: 1 - NAME ONLY - RIGHT.PNG\n"
	"004  1_-_NAME V     C        01:00:02:12 01:00:02:12 00:03:16:04 00:03:16:04 \n"
	"004     BL    V     D    012 00:00:00:00 00:00:00:12 00:03:16:04 00:03:16:16 \n"
	"* BLEND, DISSOLVE \n"
	"* FROM CLIP NAME:  1 - NAME ONLY - RIGHT.PNG \n"
	"* SOURCE FILE: 1 - NAME ONLY - RIGHT.PNG")

subst1 = "\\17\\18\\19\\20\\5 \\6\\32"

# You can manually specify the number of replacements by changing the 4th argument
#result = re.sub(regex, subst, test_str, 0, re.MULTILINE)

edlIn = open(inputEDL, "r")
edl = edlIn.read()
edlOut = open(outputEDL, "w")
# You can manually specify the number of replacements by changing the 4th argument

# delete standalone BL events:  https://regex101.com/r/kuafhd/1
result = re.sub(BLevents, subst, edl, 0, re.MULTILINE)

# replace dissolves with 1 clip:  https://regex101.com/r/VnSTI3/1
result1 = re.sub(regex1, subst1, result, 0, re.MULTILINE)

'''
regex2 = (r"^([0-9]{3})([ ]+)(BL)(.*)")
subst2 = "M2      GoodTrouble_4004_OT_R 0.0       00:00:00:01"

regex3 = (r"00:00:00:00 00:00:00:00")
subst3 = "00:00:00:01 00:00:00:01"

regex4 = (r"* SOURCE FILE: (NULL)")
subst4 = "\* FROM FILE: U:\\avid_jobs\\good-myr\\4004con\\05_titles\\open_titles\\GoodTrouble_4004_OT_R_000001.tif\n"
'''

if result1:
    print(result1)
    edlOut.write(result1)
    edlOut.close()

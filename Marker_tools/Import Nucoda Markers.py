def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)
from pprint import pprint
import sys
import os
lib_path = os.getenv("RESOLVE_SCRIPT_LIB")
import DaVinciResolveScript as dvr_script
from Tkinter import *
from tkFileDialog import *
root = Tk()
root.wm_title("Frame.io To Resolve")
w = Label(root, text="Select Frame.io CSV")

from sys import platform as _platform
if _platform == "darwin":
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "fuscript" to true' ''')

fileName = askopenfilename(parent=root)
resolve = dvr_script.scriptapp("Resolve")
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()
timeline = project.GetCurrentTimeline()

import csv
from StringIO import StringIO
with open(fileName, 'rb') as f:
    data = f.read().decode('utf8')
    # remove unicode byte-order marker if it exists
    if data.startswith(u'\uFEFF'):
        data = data[1:]
        

trim = data.split("\n",1)[1];
newdata = removeNonAscii(trim)
reader = csv.reader(StringIO(newdata))


colors = ["Blue", "Green", "Cyan", "Red"]
rows = iter(reader)
header = next(rows)

for row in rows:
    fields = dict(zip(header, row))
    print (timeline.AddMarker(int(fields[' Position'].strip())-86400, colors[int(fields[' Colour'])], fields['Date'].strip(), fields[' Description'].strip(), 1))
  




#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version: TOA_paths_0.1.py
"""
# adding paths and filenames to Resolve generated EDL.
# Will eventually match exr's to "* FROM/TO CLIP NAME:" comment in EDL.

# we are going to force the names into the EDL since we know most of the info.
# The path to the EXR's should be relative to the cwd you run the script from.
# Eventually, I will add the glob.glob() search recursive for the EXR's

import opentimelineio as otio
import glob
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help="Name of EDL to read")
parser.add_argument('-o', '--output', help="Name of EDL to write")
args = parser.parse_args()
print('Attempting to conform sources to {0}, and writing {1}'.format(args.input, args.output))

cwd = os.getcwd()
extension = 'exr'
sep = '.'

inputEDL, outputEDL = (args.input, args.output)

timeline = otio.adapters.read_from_file(inputEDL, ignore_timecode_mismatch=True)

for clip in timeline.each_clip():
    clipname_full = clip.name
    #print('* FROM CLIP NAME: {0}'.format(clipname_full))
    clipname = clipname_full.split(sep)[0]
    framerange = clipname_full.split(sep)[1]
    firstframe = framerange[1:5]  # I could also search for the number up to the '-'
    filepath = ('/{0}/{0}.{1}.{2}'.format(clipname, firstframe, extension))
    print(cwd, filepath)
    clip.media_reference = otio.schema.ExternalReference(
            target_url = cwd + filepath,  # I need to replace the target_url with pwd.
            available_range = None  # we don't know the available range
        )

otio.adapters.write_to_file(timeline, outputEDL, adapter_name='cmx_3600', style='nucoda')
print('wrote file: {}'.format(outputEDL))
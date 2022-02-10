#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
version: ripple_0.2.py
"""

#versioning up to 0.2 to add ability to input time offset for ripple

import opentimelineio as otio
import sys
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "-i",
    "--inEDL",
    help="input EDL",
    type=str
    )
parser.add_argument(
    "-o",
    "--outEDL",
    help="output EDL",
    type=str
    )
parser.add_argument(
    "-r",
    "--ripple",
    type=int,
    default=-86376,
    help="amount to ripple source range (in frames)",
    )
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="print each line",
    )
parser.add_argument(
    "-q",
    "--quiet",
    action="store_true",
    help="suppress terminal output",
    )

args = parser.parse_args()

inputEDL = args.inEDL
outputEDL = args.outEDL

if args.ripple:
    ripple = args.ripple
else:
    ripple = 0

print("reading: ", inputEDL, "and writing: ", outputEDL, "with source values rippled by", ripple)

timeline = otio.adapters.read_from_file(inputEDL, ignore_timecode_mismatch=True)

EDIT_RATE = 24
HOUR = 3600 * EDIT_RATE

for clip in timeline.each_clip():

    start_frame = clip.source_range.start_time.value

    # SRC TC is less than an hour - don't ripple
    #if start_frame < HOUR:
    #    ripple = 100

    end_frame = start_frame + clip.source_range.duration.value + ripple
        
    clip.source_range = otio.opentime.range_from_start_end_time(
        otio.opentime.from_frames(start_frame + ripple, EDIT_RATE),
        otio.opentime.from_frames(end_frame, EDIT_RATE)
    )

    if args.verbose:
        print(start_frame, start_frame + ripple)

    # print(clip.name, clip.source_range, clip.metadata)
    # I need to map the clip or tape name to the clip.name
    # print(start_frame + ripple, end_frame)
#print(otio.adapters.write_to_string(timeline))
otio.adapters.write_to_file(timeline, outputEDL, adapter_name='cmx_3600', style='nucoda')


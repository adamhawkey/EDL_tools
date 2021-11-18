#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
version: GT_prep_0.4.py
"""

# This script is very specific to the show Good Trouble.
# Versioning up to 0.4 as we begin season 4.
# Camera has changed to the Sony Venice X-OCN format in Venice_SLog3_SGamut3.cine space.
#
# In a future version, I may add variable amount of cc_layers, different colorspaces, and verbose/quiet switch

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
print("reading: ", inputEDL, "and writing: ", outputEDL)

timeline = otio.adapters.read_from_file(inputEDL, ignore_timecode_mismatch=True)

lut_path = ('T:\\luts\\GoodTrouble\\Season_4\\Season_04_SL3SG3C\\') # this is the local root path to the luts.
lut_space = ('sl3_sg3c')
lut_version = ('v3')
lut_ext = ('cube')

timeline = otio.adapters.read_from_file(inputEDL, ignore_timecode_mismatch=True)
# ignore_timecode_mismatch=True deals with the source timecode and duration 
# not matching the timebase.

for clip in timeline.each_clip():
    
    edl_meta = clip.metadata.get('cmx_3600',{})
    
    nucoda_stack = [
        'NUCODA_LAYER Log',
        'NUCODA_LAYER Log2',
        'NUCODA_LAYER Log3',
        'NUCODA_LAYER Log4',
        'NUCODA_LAYER Log5',
        'NUCODA_LAYER Log6',
    ]
    
    comments = edl_meta.get('comments', [])

    for comment in comments:
        if 'REEL: GT_' in comment:
            _, lut_string = comment.split(": ")
            #print("lut_string=", lut_string)
            lut_string_split = re.split(r'_SDR', lut_string)
            #print("lut_string_split=", lut_string_split)
            lut_string_chars = re.split(r'[^A-Za-z0-9_]+', lut_string_split[0])
            #print(lut_string_chars[0])
            lut_root = lut_string_chars[0]
            #print("lut_root=",lut_root)
            if args.verbose:
                print('{0} becomes {0}_{1}_{2}.{4}'.format(lut_string, lut_root, lut_space, lut_version, lut_ext))
            lut_layer = 'NUCODA_LAYER GT_LUT -effect NucodaCMSPath -lut {0}{1}_{2}.{4}'.format(lut_path, lut_root, lut_space, lut_version, lut_ext)
            #print("lut_layer=", lut_layer)
            nucoda_stack.append(lut_layer)

    comments.extend(nucoda_stack)

otio.adapters.write_to_file(timeline, outputEDL, adapter_name='cmx_3600', style='nucoda')
#print(otio.adapters.write_to_string(timeline, adapter_name='cmx_3600'))

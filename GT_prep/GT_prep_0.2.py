#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
version: GT_prep_0.2.py
"""
import opentimelineio as otio
import sys

inputEDL, outputEDL = sys.argv[1:]

lut_space = ('VLog') # other option is SDR
lut_version = ('V2')
lut_ext = ('cube')

EDIT_RATE = 24
HOUR = 3600 * EDIT_RATE
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
            lut_root, _ = lut_string.split('_SDR')
            lut_layer = 'NUCODA_LAYER GT_LUT -effect NucodaCMSPath -lut T:\\luts\\GoodTrouble\\{0}_{1}_{2}.{3}'.format(lut_root, lut_space, lut_version, lut_ext)
            nucoda_stack.append(lut_layer)

    comments.extend(nucoda_stack)
    
otio.adapters.write_to_file(timeline, outputEDL, adapter_name='cmx_3600', style='nucoda')
#print(otio.adapters.write_to_string(timeline, adapter_name='cmx_3600'))

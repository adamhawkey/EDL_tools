#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
version: GT_prep_0.1.py
"""
import opentimelineio as otio
import sys

inputEDL, outputEDL = sys.argv[1:]

EDIT_RATE = 24
HOUR = 3600 * EDIT_RATE
timeline = otio.adapters.read_from_file(inputEDL)
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
        if 'REEL:' in comment:
            _, reel_name = comment.split(": ")
            lut_layer = 'NUCODA_LAYER GT_LUT -effect NucodaCMSPath -lut T:\\luts\\GoodTrouble\\{}.cube'.format(reel_name)
            nucoda_stack.append(lut_layer)

    comments.extend(nucoda_stack)
    
otio.adapters.write_to_file(timeline, outputEDL, adapter_name='cmx_3600', style='nucoda')
#print(otio.adapters.write_to_string(timeline, adapter_name='cmx_3600'))

#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
version: CDL_extract_0.1.py
"""
### hopefully will write CDL files from a CDL-EDL

import opentimelineio as otio
import sys
import re

_, inputEDL = sys.argv[:]

timeline = otio.adapters.read_from_file(inputEDL, ignore_timecode_mismatch=True)
# ignore_timecode_mismatch=True deals with the source timecode and duration 

for clip in timeline.each_clip():
    #edl_meta = clip.metadata.get('cmx_3600',{})
    cdl = clip.metadata.get('cdl', {})
    asc_sat = cdl['asc_sat']
    asc_sop = cdl['asc_sop']
    asc_slope = asc_sop['slope']
    asc_offset = asc_sop['offset']
    asc_power = asc_sop['power']
    
    print('<ColorDecisionList xmnls="urn:ASC:CDL:v1.01">')
    print('    <ColorDecision>')
    print('        <ColorCorrection>')
    print('            <SOPNode>')
    print('                <Slope>{0} {1} {2}</Slope>'.format(asc_slope[0], asc_slope[1], asc_slope[2]))
    print('                <Offset>{0} {1} {2}</Offset>'.format(asc_offset[0], asc_offset[1], asc_offset[2]))
    print('                <Power>{0} {1} {2}</Power>'.format(asc_power[0], asc_power[1], asc_power[2]))
    print('            </SOPNode>')
    print('            <SatNode>')
    print('                <Saturation>{0}</Saturation>'.format(asc_sat))
    print('            </SatNode>')
    print('        </ColorCorrection>')
    print('    </ColorDecision>')
    print('</ColorDecisionList>')

'''
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
            #print(lut_string)
            lut_string_split = re.split(r'_SDR', lut_string)
            #print(lut_string_split)
            lut_string_chars = re.split(r'[^A-Za-z0-9_]+', lut_string_split[0])
            #print(lut_string_chars[0])
            lut_root = lut_string_chars[0]
            #print(lut_root)
            print('{0} becomes {1}_{2}_{3}.{4}'.format(lut_string, lut_root, lut_space, lut_version, lut_ext))
            lut_layer = 'NUCODA_LAYER GT_LUT -effect NucodaCMSPath -lut {0}{1}_{2}_{3}.{4}'.format(lut_path, lut_root, lut_space, lut_version, lut_ext)
            nucoda_stack.append(lut_layer)

    comments.extend(nucoda_stack)
    
otio.adapters.write_to_file(timeline, outputFolder, adapter_name='cmx_3600', style='nucoda')
#print(otio.adapters.write_to_string(timeline, adapter_name='cmx_3600'))
'''
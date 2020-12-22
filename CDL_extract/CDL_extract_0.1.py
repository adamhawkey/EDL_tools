#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
version: CDL_extract_0.1.py
"""
### will write individual CDL files from a CDL-EDL (a least the kind that gets sent to Culley)

import opentimelineio as otio
import sys
import re

_, inputEDL = sys.argv[:]

timeline = otio.adapters.read_from_file(inputEDL, ignore_timecode_mismatch=True)
# ignore_timecode_mismatch=True deals with the source timecode and duration 

for clip in timeline.each_clip():
    clipname = clip.name
    cdl = clip.metadata.get('cdl', {})
    asc_sat = cdl['asc_sat']
    asc_sop = cdl['asc_sop']
    asc_slope = asc_sop['slope']
    asc_offset = asc_sop['offset']
    asc_power = asc_sop['power']
    outputCDL = ('{}.cdl'.format(clipname))
    # write the output cdl file
    writeCDL = open(outputCDL, 'w')
    writeCDL.write('<ColorDecisionList xmnls="urn:ASC:CDL:v1.01">\n')
    writeCDL.write('    <ColorDecision>\n')
    writeCDL.write('        <ColorCorrection>\n')
    writeCDL.write('            <SOPNode>\n')
    writeCDL.write('                <Slope>{0} {1} {2}</Slope>\n'.format(asc_slope[0], asc_slope[1], asc_slope[2]))
    writeCDL.write('                <Offset>{0} {1} {2}</Offset>\n'.format(asc_offset[0], asc_offset[1], asc_offset[2]))
    writeCDL.write('                <Power>{0} {1} {2}</Power>\n'.format(asc_power[0], asc_power[1], asc_power[2]))
    writeCDL.write('            </SOPNode>\n')
    writeCDL.write('            <SatNode>\n')
    writeCDL.write('                <Saturation>{0}</Saturation>\n'.format(asc_sat))
    writeCDL.write('            </SatNode>\n')
    writeCDL.write('        </ColorCorrection>\n')
    writeCDL.write('    </ColorDecision>\n')
    writeCDL.write('</ColorDecisionList>\n')
    writeCDL.close()

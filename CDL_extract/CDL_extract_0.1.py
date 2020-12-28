#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
version: CDL_extract_0.1.py
"""
### Will write individual CDL files from a CDL-EDL (a least the kind that gets sent to Culley).
### If the edl uses different CDL values for different events with the same source file, source clip, or reel,
### the only way to name the .cdl's without the possibility of overwriting earlier events is to
### use the locator name if it's provided, like: *LOC: 01:00:02:16 CYAN    PNK_K1214_REH_080

import opentimelineio as otio
import sys
import re
import os

inputEDL = sys.argv[1]

timeline = otio.adapters.read_from_file(inputEDL, ignore_timecode_mismatch=True)
# ignore_timecode_mismatch=True deals with the source timecode and duration 

outFolder, ext = inputEDL.split('.', 1)
os.mkdir(outFolder)  # Need to add exception so that if folder exists, it warns you.

def writeCDL():
	#writes individual .cdl files in current folder
    outputCDL = ('{}.cdl'.format(markers))
    # write the output cdl file
    writeCDL = open("{0}/{1}".format(outFolder, outputCDL), 'w')
    writeCDL.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    writeCDL.write('<ViewingDescription>written with CDL_extract by Adam Hawkey</ViewingDescription>\n')
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

for clip in timeline.each_clip():
    #edl_meta = clip.metadata.get('cmx_3600',{})    # Not necessary for this particular script
    clipname = clip.name
    markers = clip.markers[0].name
    cdl = clip.metadata['cdl']
    asc_sat = cdl['asc_sat']
    asc_sop = cdl['asc_sop']
    asc_slope = asc_sop['slope']
    asc_offset = asc_sop['offset']
    asc_power = asc_sop['power']
    #write the output cdl file.
    writeCDL()

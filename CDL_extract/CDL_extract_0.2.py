#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
Usage:  CDL_extract_0.2.py {EDL or ALE name}
"""
### First major revision to be able to input a Resolve ALE with CDL values and make .cc files.

import opentimelineio as otio
import sys
import re
import os

if len(sys.argv) < 2:
    print('Not enough arguments.', __doc__)
    sys.exit()
inputFile = sys.argv[1]

timeline = otio.adapters.read_from_file(inputFile, ignore_timecode_mismatch=True)
# ignore_timecode_mismatch=True (allows source tc and dur to not match record tc)

num = 0 #counter for multiple duplicate clip_names.
outFolder, ext = inputFile.split('.', 1)

try:
    os.mkdir(outFolder)  # if folder exists, it warns you and exits.
except: 
    print('folder exists, shall we continue?')
    answer = input('[Y or N]')
    if answer == 'Y':
        print('writing to pre-existing directory: {}'.format(outFolder))
        pass
    elif answer == 'N':
        print('exiting program')
        exit()

def writeCDL():     #writes individual .cdl files in current folder
    outputCDL = ('{}.cdl'.format(clip_name))
    print('writing: {}'.format(outputCDL))
    writeCDL = open("{0}/{1}".format(outFolder, outputCDL), 'w')    # write the output cdl file
    writeCDL.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    writeCDL.write('<ViewingDescription>written with CDL_extract_0.2 by Adam Hawkey</ViewingDescription>\n')
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
    clip_name = clip.name
#    try:
#        clip_name = clip.name[0].name
#    except:
#        clip_name = '{0}_{1}'.format(clip_name, num)  #this is only if there is no locator present.  will not help if there are multiple clips with same clip_name.
#        num = num + 1   #this increments the value after the name incase there is a duplicate.  Would be better if I checked if an identical filename exists, and only increment then.

    try:
        cdl = clip.metadata['cdl']
        asc_sat = cdl['asc_sat']
        asc_sop = cdl['asc_sop']
        asc_slope = asc_sop['slope']
        asc_offset = asc_sop['offset']
        asc_power = asc_sop['power']

        ale_meta = clip.metadata.get('ALE')
        print(clip_name)
        print(ale_meta)
        #ale = clip.metadata['ALE']
        #tapename = ale['Tape']
        
        print(cdl)
        #writeCDL()  #write the output cdl file.
    except:
        print('No CDL values present for {}'.format(clip_name))


#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
Usage:  ALE_to_CDL_0.4.py {-i inputfilename -o outputFolder}
"""
### total rewrite to input a Resolve ALE with CDL values and make .cc files in a specified folder.
### changed default to write Nuke compatible .cc files.

import opentimelineio as otio
import sys
import re
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inFile", help="input File", type=str)
parser.add_argument("-o", "--outFolder", help="output Folder", type=str)
parser.add_argument("-v", "--verbose", action="store_true", help="print each line")
parser.add_argument("-q", "--quiet", action="store_true", help="suppress terminal output")

args = parser.parse_args()

inFile = args.inFile
outFolder = args.outFolder

if args.verbose:
    print('Verbose mode')
    print("reading:", inFile, "and writingCDL .cc files to:", outFolder)
elif args.quiet:
    print('shhhhh, I\'m being quiet')

timeline = otio.adapters.read_from_file(inFile)

num = 0 #counter for multiple duplicate clip_names. (not implemented yet)

def main():
    writeDIR()
    for clip in timeline.each_clip():
        clip_name_ext = clip.name
        clip_name, ext = clip_name_ext.split('.', 1)
        #print(clip_name)
        try:
            cdl = clip.metadata['cdl']
            asc_sat = cdl['asc_sat']
            asc_sop = cdl['asc_sop']
            asc_slope = asc_sop['slope']
            asc_offset = asc_sop['offset']
            asc_power = asc_sop['power']
            print(clip_name, cdl)
            writeNukeCDL(clip_name, asc_sat, asc_slope, asc_offset, asc_power)  #write the output cdl file.
        except:
            print('No CDL values present for {}'.format(clip_name))

def writeDIR():
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

def writeCDL(clip_name, asc_sat, asc_slope, asc_offset, asc_power):     #writes individual .cdl files in current folder
    outputCDL = ('{}.cc'.format(clip_name))
    print('writing: {}'.format(outputCDL))
    writeCDL = open("{0}/{1}".format(outFolder, outputCDL), 'w')    # write the output cdl file
    writeCDL.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    writeCDL.write('<ViewingDescription>written with ALE_to_CDL_0.3 by Adam Hawkey</ViewingDescription>\n')
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

def writeNukeCDL(clip_name, asc_sat, asc_slope, asc_offset, asc_power):     #writes individual Nuke compatible .cc files in output folder.
    outputCDL = ('{}.cc'.format(clip_name))
    print('writing: {}'.format(outputCDL))
    writeCDL = open("{0}/{1}".format(outFolder, outputCDL), 'w')    # write the output cdl file
    writeCDL.write('<ColorCorrection>\n')
    writeCDL.write('    <SOPNode>\n')
    writeCDL.write('        <Slope>{0} {1} {2}</Slope>\n'.format(asc_slope[0], asc_slope[1], asc_slope[2]))
    writeCDL.write('        <Offset>{0} {1} {2}</Offset>\n'.format(asc_offset[0], asc_offset[1], asc_offset[2]))
    writeCDL.write('        <Power>{0} {1} {2}</Power>\n'.format(asc_power[0], asc_power[1], asc_power[2]))
    writeCDL.write('    </SOPNode>\n')
    writeCDL.write('    <SatNode>\n')
    writeCDL.write('        <Saturation>{0}</Saturation>\n'.format(asc_sat))
    writeCDL.write('    </SatNode>\n')
    writeCDL.write('</ColorCorrection>\n')
    writeCDL.close()

main()

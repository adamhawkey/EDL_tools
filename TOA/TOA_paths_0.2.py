#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version: TOA_paths_0.1.py

Usage: conform.py -i inputEDL -f media -o outputEDL
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

cwd = os.getcwd()
extension = 'exr'
sep = '.'

def parse_args():
    """ parse arguments out of sys.argv """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
    	'-i',
        '--input',
        type=str,
        #required=True,
        help='Timeline file(s) to read. Supported formats: {adapters}'
             ''.format(adapters=otio.adapters.available_adapter_names())
    )
    parser.add_argument(
        '-f',
        '--folder',
        type=str,
        #required=True,
        help='Folder to look for media in.'
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        #required=True,
        help="Timeline file to write out."
    )
    return parser.parse_args()

def _find_matching_media(name, folder):
    """Look for media with this name in this folder."""
    
    print('looking for {0} in {1}'.format(name, folder))

    matches = glob.glob("{0}/{1}/{1}.*".format(folder, name), recursive=True)
    #print(matches)
    #matches = map(os.path.abspath, matches)

    if len(matches) == 0:
        print("DEBUG: No match for clip '{0}'".format(name))
        return None
    if len(matches) == 1:
        return matches[0]
    else:
        print(
            "WARNING: {0} matches found for clip '{1}', using '{2}'".format(
                len(matches),
                name,
                matches[0]
            )
        )
        return matches[0]

def _conform_timeline(timeline, folder):
    """ Look for replacement media for each clip in the given timeline.

    The clips are relinked in place if media with a matching name is found.
    """

    count = 0

    for clip in timeline.each_clip():
        # look for a media file that matches the clip's name
        new_path = _find_matching_media(clip.name, folder)

        # if no media is found, keep going
        if not new_path:
            continue

        # if we found one, then relink to the new path
        clip.media_reference = otio.schema.ExternalReference(
            target_url="file://" + new_path,
            available_range=None  # we don't know the available range
        )
        count += 1

    return count

def main():
    args = parse_args()
    timeline = otio.adapters.read_from_file(args.input, ignore_timecode_mismatch=True)
    count = _conform_timeline(timeline, args.folder)
    print("Relinked {0} clips to new media.".format(count))
    otio.adapters.write_to_file(timeline, args.output, adapter_name='cmx_3600', style='nucoda')
    print(
        "Saved {} with {} clips.".format(
            args.output,
            len(list(timeline.each_clip()))
        )
    )

if __name__ == '__main__':
    main()

'''  # this was before I used the function method.
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
'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version: TOA_paths_0.1.py
"""
# adding paths and filenames to Resolve generated EDL.

import opentimelineio as otio
import sys
import re

inputEDL, outputEDL = sys.argv[1:]

print('reading {}'.format(inputEDL))
timeline = otio.adapters.read_from_file(inputEDL, ignore_timecode_mismatch=True)

for clip in timeline.each_clip():
    print(clip, '\n')
    #_, clip_name_full = comment.split(": ")
    #print(clip_name_full)
    #edl_meta = clip.metadata.get('cmx_3600',{})
    #print(edl_meta)

comment_type = ['* FROM FILE: ']
print(comment_type)
    #comments = edl_meta
    #comments = edl_meta.get('comments', [])
    #clip_name_root = re.split(r'.[', comments)
    #print(comments)
    

    #for comment in comments:
        #if '* FROM CLIP NAME: ' in comment:   # may need to look for TO FILE NAME: also
            #_, clip_name_full = comment.split(": ")
            #print(clip_name_full)
            #clip_name_root = re.split(r'.[', clip_name)
            #clip_name_chars = re.split(r'[^A-Za-z0-9_]+', clip_name_root[0])
            #print(clip_name_chars[0])
            #lut_root = clip_name_chars[0]
            #print('{0} becomes {1}_{2}_{3}.{4}'.format(clip_name, lut_root, lut_space, lut_version, lut_ext))
            #lut_layer = 'NUCODA_LAYER GT_LUT -effect NucodaCMSPath -lut {0}{1}_{2}_{3}.{4}'.format(lut_path, lut_root, lut_space, lut_version, lut_ext)
            #comment_type.append(lut_layer)

comments.extend(comment_type)

#otio.adapters.write_to_file(timeline, outputEDL, adapter_name='cmx_3600', style='nucoda')

'''
for clip in timeline.each_clip():
    # edl_meta = clip.metadata.get('cmx_3600', {})
    # comments = edl_meta.get('comments', [])
    
    #ripple = -HOUR + 100

    start_frame = clip.source_range.start_time.value

    # SRC TC is less than an hour - don't ripple
    if start_frame < HOUR:
        ripple = 100

    end_frame = start_frame + clip.source_range.duration.value + ripple
    
    clip.source_range = otio.opentime.range_from_start_end_time(
        otio.opentime.from_frames(start_frame + ripple, EDIT_RATE),
        otio.opentime.from_frames(end_frame, EDIT_RATE)
    )
    # print(clip.name, clip.source_range, clip.metadata)
    # I need to map the clip or tape name to the clip.name
    # print(start_frame + ripple, end_frame)
#print(otio.adapters.write_to_string(timeline))
otio.adapters.write_to_file(timeline, outputEDL, adapter_name='cmx_3600', style='nucoda')
'''

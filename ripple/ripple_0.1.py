#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
version: ripple_0.1.py
"""
import opentimelineio as otio
import sys
import copy

inputfile, outputfile = sys.argv[1:]

EDIT_RATE = 24
HOUR = 3600 * EDIT_RATE
timeline = otio.adapters.read_from_file(inputfile)
for clip in timeline.each_clip():
    ripple = -HOUR + 100

    start_frame = clip.source_range.start_time.value

    # SRC TC is less than an hour - don't ripple
    if start_frame < HOUR:
        ripple = 100

    end_frame = start_frame + clip.source_range.duration.value + ripple

    clip.source_range = otio.opentime.range_from_start_end_time(
        otio.opentime.from_frames(start_frame + ripple, EDIT_RATE),
        otio.opentime.from_frames(end_frame, EDIT_RATE)
    )

otio.adapters.write_to_file(timeline, outputfile, adapter_name='cmx_3600', style='nucoda')


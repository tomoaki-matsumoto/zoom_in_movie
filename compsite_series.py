#! /bin/env python3
# last updated : 2020/12/05 21:06:33
# -*- coding: utf-8 -*-
# Composite images with different resolution data in image sequence.
#
# Calling sequence:
# ./zoom_composite.py
#
# This code requires module opencv-python.
#
def composite(fnl, fnh, fnn, weight):
    import cv2
    import numpy as np
    imagel = cv2.imread(fnl) # low resolution
    imageh = cv2.imread(fnh) # high resolution
    imagen = imageh*weight + imagel*(1-weight)
    cv2.imwrite(fnn, imagen)

def get_stage_level_by_fn(fn):
    fnbase = os.path.basename(fn)
    stage, level, ext = fnbase.split('.')
    return int(stage), int(level)

import numpy as np
import glob
import os
import shutil

# Edit here
pngdir = 'png_zoom_1080p'       # input directory
pngdircomposite = 'png_zoom_composite_1080p' # output directory

if not os.path.isdir(pngdircomposite):
    os.mkdir(pngdircomposite)

fnlist = glob.glob(pngdir+'/'+'[0-9]*.png')
fnlist.sort()

# Zoom in or zoom out
stage, level_st = get_stage_level_by_fn(fnlist[0])
stage, level_ed = get_stage_level_by_fn(fnlist[-1])
if level_st < level_ed:
    bool_zoomin = True          # zoom-in
else:
    bool_zoomin = False         # zoom-out

# stage 52 level 2-3
# make list of list stages_by_level
# stages_by_level[levels[n]][:] = stages
stlist = []
lvlist = []
for fn in fnlist:
    stage, level = get_stage_level_by_fn(fn)
    stlist.append(stage)
    lvlist.append(level)
stagemax = max(stlist)
stagemin = min(stlist)
levelmax = max(lvlist)
levelmin = min(lvlist)


stages_by_level = []
levels = []
for level in range(levelmin, levelmax+1):
    levels.append(level)
    stages = []
    for fn in fnlist:
        stage, lev = get_stage_level_by_fn(fn)
        if lev == level:
            stages.append(stage)
    stages_by_level.append(stages)

levels_by_stage  =[]
stages = []
for stage in range(stagemin, stagemax+1):
    stages.append(stage)
    levels = []
    for fn in fnlist:
        st, level = get_stage_level_by_fn(fn)
        if st == stage:
            levels.append(level)
    levels_by_stage.append(levels)


# for each frame
for stage in range(stagemin, stagemax+1):
    ist = stage-stagemin
    if len(levels_by_stage[ist]) == 1:
        # copy image
        # print('just copy')
        fnL = pngdir + '/{:0>5}.{:0>5}.png'.format(stage, levels_by_stage[ist][0])
        fnout = pngdircomposite + '/{:0>5}.png'.format(stage)
        shutil.copyfile(fnL, fnout)
        print(fnout)
    else:
        # composite
        lL, lR = levels_by_stage[ist]
        if lL+1 != lR:
            print('*** Error in lmin, lmax')
        # dumplicate rage [stL, stR] for levels [lL, lR]
        if bool_zoomin:
            stL = stages_by_level[lR][0]
            stR = stages_by_level[lL][-1]
            # stR = (stL + stR)//2
            stR = stL + (stR-stL)*2./3.
            weight = max(0.0, min(1.0, (stage-stL)/(stR-stL)))
            print(weight)
            fnL = pngdir + '/{:0>5}.{:0>5}.png'.format(stage, lL)
            fnR = pngdir + '/{:0>5}.{:0>5}.png'.format(stage, lR)
            fnout = pngdircomposite + '/{:0>5}.png'.format(stage)
            print(fnL, fnR)
            composite(fnL, fnR, fnout, weight)
        else:
            stR = stages_by_level[lR][-1]
            stL = stages_by_level[lL][0]
            # stR = (stL + stR)//2
            stR = stL + (stR-stL)*2./3.
            weight = max(0.0, min(1.0, 1-(stage-stL)/(stR-stL)))
            print(weight)
            fnL = pngdir + '/{:0>5}.{:0>5}.png'.format(stage, lL)
            fnR = pngdir + '/{:0>5}.{:0>5}.png'.format(stage, lR)
            fnout = pngdircomposite + '/{:0>5}.png'.format(stage)
            print(fnL, fnR)
            composite(fnL, fnR, fnout, weight)

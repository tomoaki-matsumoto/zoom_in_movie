#! /bin/env python3
# last updated : 2020/12/07 09:25:58
# -*- coding: utf-8 -*-
# (C) Tomoaki Matsumoto <matsu@hosei.ac.jp>
#
# A sample code for visualization of a zoom-in movie for AMR simulations.
# Uniform grid files are used for the visualization.
#
# Calling sequence:
#
# ./zoomseries.py
#
# If you execute this command on a remote server, you may have to use X virtual framebuffer.
# Paraview does not support remote X11.
# Xvfb :1 -ac -screen 0 1024x1024x24 &> /dev/null &
# export DISPLAY=:1
#
import numpy as np
import amr.path as ap
import os
import textwrap
import subprocess

dir = "/rzi9/amnh/M1B01a/"      # a directory of data to be read
pngdir = 'png_zoom_1080p'      # a directory for PNG files (output files)
file_inputParam = 'inputParam.py'
nframe = 150                    # number of frames

if not os.path.isdir(pngdir):
    os.mkdir(pngdir)

distance_st = 72.69963836669922
# distance_ed = 0.1436619758605957/4  # too close to sink particle
distance_ed = 0.1436619758605957/2
logd_st = np.log10(distance_st)
logd_ed = np.log10(distance_ed)
d_logd = (logd_ed - logd_st)/(nframe-1)
distance_list = 10**np.arange(logd_st, logd_ed + d_logd, d_logd)
distance_0 = distance_st/2

# density propto 1/distance**2
target_logn_st = 6
target_logn_ed = 30
target_logn_list = np.minimum(np.log10(10**target_logn_st*(distance_st/distance_list)**2), target_logn_ed)

stage = 1765000

prefix_list = [
    'ug',
    '16000au.1.',
    '8000au.1.',
    '4000au.1.',
    '2000au.1.',
    '1000au.1.',
    '400au.1.',
    '200au.1.',
    '100au.1.',
    '50au.1.']

level_list = [0,1,2,3,4,5,6,7,8,9]

l0_au = 1387.9597746403967      # conversion factor btw simulation unit-length and physical unit (au).

boxsize = np.array([25226, 16000, 8000, 4000, 2000, 1000, 400, 200, 100, 50])/l0_au

for n in range(nframe):
    # if n != nframe-1:
    #     continue
    distance = distance_list[n]
    target_logn = target_logn_list[n]
    mm = 0
    fnlist = []
    for m in range(len(prefix_list)):
        if not (boxsize[m] * 0.8 <= distance and distance <= boxsize[m] * 4.1) :
            continue
        prefix = prefix_list[m]
        level = level_list[m]
        fn_base = (ap.encode_filename( ['', prefix, stage, level, ''] ))[0:-1]
        pngfile = pngdir + '/{:0>5}.{:0>5}.png'.format(n, m)
        fnlist.append(pngfile)
        print(pngfile)

        string = textwrap.dedent('''
dir = '{dir}'
fn = '{fn_base}'
target_logn = {target_logn}
pngfile = '{pngfile}'
distance = {distance}
''').format(dir=dir, fn_base=fn_base, target_logn=target_logn, pngfile=pngfile, distance=distance).strip()

        with open(file_inputParam, mode='w') as f:
            f.write(string)
        f.close()
        subprocess.run(['pvbatch', '--use-offscreen-rendering', 'pvscript.py'])
       
        mm = mm + 1
        if mm >= 2:
            break

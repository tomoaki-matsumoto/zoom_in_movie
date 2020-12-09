# last updated : 2020/12/07 09:38:01
# -*- coding: utf-8 -*-
# (C) Tomoaki Matsumoto <matsu@hosei.ac.jp>
#
# A python script used for Paraview.
#
# Calling sequence:
#
# pvbatch --use-offscreen-rendering core_zoom2.py
#
import inputParam as ip
import amr.uniformgrid as ug

target_logn = ip.target_logn
distance = ip.distance
rhomax = 13.0 # maximum and minimum log rho for color scale
rhomin = 4.0

# read data
dir = ip.dir
fn = ip.fn
time = ug.read_header(dir+fn+'.d')[1] # get time of data

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'XDMF Reader'
ugdata = XDMFReader(FileNames=[dir+fn+'.xdmf'])

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
renderView1.ViewSize = [1920, 1080] #1080p

# reset view to fit data
renderView1.ResetCamera()

# create a new 'Calculator'
calculator1 = Calculator(Input=ugdata)
calculator1.Function = ''

# Properties modified on calculator1
calculator1.ResultArrayName = 'log_n'
calculator1.Function = 'log10(Density*261832.02833370265)'

# show data in view
calculator1Display = Show(calculator1, renderView1)
# trace defaults for the display properties.
calculator1Display.Representation = 'Outline'
calculator1Display.ColorArrayName = ['POINTS', '']
calculator1Display.Slice = 129
calculator1Display.ScalarOpacityUnitDistance = distance/2/calculator1Display.Slice

# hide data in view
Hide(ugdata, renderView1)

# rescale color and/or opacity maps used to include current data range
calculator1Display.RescaleTransferFunctionToDataRange(True)

# change representation type
calculator1Display.SetRepresentationType('Volume')

# get opacity transfer function/opacity map for 'Density'
densityPWF = GetOpacityTransferFunction('Density')
densityPWF.Points = [0.027056114748120308, 0.0, 0.5, 0.0, 3176.96630859375, 1.0, 0.5, 0.0]
densityPWF.ScalarRangeInitialized = 1

# set scalar coloring
ColorBy(calculator1Display, ('POINTS', 'log_n'))

# rescale color and/or opacity maps used to include current data range
calculator1Display.RescaleTransferFunctionToDataRange(True)

# show color bar/color legend
calculator1Display.SetScalarBarVisibility(renderView1, True)


# get color transfer function/color map for 'logn'
lognLUT = GetColorTransferFunction('logn')
lognLUT.RGBPoints = [rhomin, 0.231373, 0.298039, 0.752941,
                     4.4, 0.231373, 0.298039, 0.752941,
                     (4.4+6.5)/2, 0.865003, 0.865003, 0.865003,
                     6.5, 0.705882, 0.0156863, 0.14902,
                     8.5, 0.992218,0.555217,0.236278, #O
                     9.5, 1.0, 1.0, 0.0,   # Y
                     10.0, 0.0, 1.0, 0.0, # G
                     11.0, 0.0, 0.8, 0.7, # C
                     11.5, 0.0, 0.3, 0.8, # CB
                     11.75, 0.05, 0.2, 0.8, # CB
                     12.0, 0.1, 0.1, 0.8, # B
                     rhomax, 0.7, 0.2, 0.7] # M
lognLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'logn'
lognPWF = GetOpacityTransferFunction('logn')
lognPWF.Points = [-1.5677345678491652, 0.0, 0.5, 0.0, 3.5020126092025303, 1.0, 0.5, 0.0]
lognPWF.ScalarRangeInitialized = 1


# Properties modified on lognLUT
# lognLUT.NumberOfTableValues = 512

# Rescale transfer function
lognLUT.RescaleTransferFunction(rhomin, rhomax)

# Properties modified on lognPWF
rhoOptMin = 6-1.7
lognPWF.Points = [rhomin, 0.0, 0.5, 0.0,
                  max(target_logn-3.0,rhoOptMin), 0.0, 0.5, 0.0,
                  max(target_logn-1.6,rhoOptMin), 0.01, 0.5, 0.0,
                  target_logn, 0.1, 0.5, 0.0,
                  rhomax, 1.0, 0.5, 0.0]

lognLUTColorBar = GetScalarBar(lognLUT, renderView1)
lognLUTColorBar.Title = 'log n'
lognLUTColorBar.ComponentTitle = '(cm-3)'

# current camera placement for renderView1
sinkloc = [-0.14385176, -1.28737869,  2.32440692]
sinkradius = 0.00027842075*4
# create a new 'Sphere'
sphere1 = Sphere()
sphere1.Center = sinkloc
sphere1.Radius = sinkradius
sphere1.ThetaResolution = 16
sphere1.PhiResolution = 16
# show data in view
sphere1Display = Show(sphere1, renderView1)
# trace defaults for the display properties.
sphere1Display.ColorArrayName = [None, '']

renderView1.CameraFocalPoint = sinkloc
renderView1.CameraPosition = [renderView1.CameraFocalPoint[0], renderView1.CameraFocalPoint[1] - distance, renderView1.CameraFocalPoint[2]]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = distance/3.
renderView1.Background = [0.0, 0.0, 0.0]

# create a new 'Text'
text1 = Text()

# # Properties modified on text1
t0_yr = 34606.168196095314      # conversion factor btw simulation unit-time and physical unit (yr).
text1.Text = 'Model M1B01\nt = {:12.5e}'.format(time*t0_yr) + ' yr'

# # show data in view
text1Display = Show(text1, renderView1)

# # Properties modified on text1Display
text1Display.WindowLocation = 'UpperLeftCorner'

# Properties modified on text1Display
text1Display.FontSize = 10

# save screenshot
SaveScreenshot(ip.pngfile, magnification=1, quality=100, view=renderView1)


#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).

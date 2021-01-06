''' GD 20200102
    
    Mainline for wxPython syswheel util
'''

import os
import sys
import math
import time

import wx

import mainframe


app = wx.App( False )
frame = mainframe.WheelFrame( None, "Sys Wheel" )
app.MainLoop()
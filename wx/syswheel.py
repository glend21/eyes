''' GD 20200102
    
    Mainline for wxPython syswheel util
'''

import os
import sys
import math
import time

import wx

import mainframe


'''
app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
frame = wx.Frame(None, wx.ID_ANY, "Hello World") # A Frame is a top-level window.
frame.Show(True)     # Show the frame.
app.MainLoop()
'''

class DrawPanel(wx.Frame):

    """Draw a line to a panel."""

    def __init__(self):
        wx.Frame.__init__(self, None, title="Draw on Panel")
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.work = 0.0
        self.tot = 0.0

    def OnPaint(self, event=None):
        dc = wx.PaintDC(self)
        dc.Clear()

        w = 4
        r = 50
        c = wx.Point( 160, 120 )

        for theta in range( 0, 360, 4 ):
            rtheta = math.radians( theta )

            l = r * self.usage()
            if l <= 0.0:
                continue

            if l < (r * 0.33):
                dc.SetPen( wx.Pen( wx.GREEN, 4 ) )
            elif l < (r * 0.67):
                dc.SetPen( wx.Pen( wx.YELLOW, 4 ) )
            else:
                dc.SetPen( wx.Pen( wx.RED, 4 ) )

            start = wx.Point( c.x + int( r * math.cos( rtheta ) ), 
                              c.y - int( r * math.sin( rtheta ) )
                            )
                            
            end = wx.Point( c.x + int( (r + l) * math.cos( rtheta ) ),
                            c.y - int( (r + l) * math.sin( rtheta ) )
                          ) 
            dc.DrawLine( start, end )
            #wx.Sleep( 1 )


    def usage( self ):
        ''' Get the CPU usage and calc the percentage '''


        # Make the IO as efficient as possible
        # The aggregated CPU data is on the first line
        with open( "/proc/stat", "rt" ) as ifh:
            ln = ifh.readline()

        vals = [ int( v ) for v in ln.split()[ 1 : ] ]
        work = sum( vals[ : 3 ] )
        tot = sum( vals )
        print( ln )
        print( vals )
        print( tot )
        cpu_perc = 0.0
        if self.tot > 0:
            cpu_perc = (work - self.work) / (tot - self.tot) * 100.0

        self.work = work
        self.tot = tot

        print( "%s [%.1f]" % ('#' * int( cpu_perc ), cpu_perc) )
        return cpu_perc



app = wx.App( False )
frame = mainframe.WheelFrame( None, "Sys Wheel" )
app.MainLoop()
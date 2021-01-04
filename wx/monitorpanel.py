''' GD 20210102
    A wx.Panel that displays an instrument wheel
'''

import math

import wx

import globals as gl
import instrument


class AMonitorPanel( wx.Panel ):
    ''' ABC for all monitor panels '''

    def __init__( self, parent, title="" ):
        ''' ctor '''

        wx.Panel.__init__( self, parent, size=wx.Size( gl.panel_width, gl.panel_height ) )
        self.myParent = parent
        self.title = title
        self.SetBackgroundColour( wx.TheColourDatabase.Find( "GREY" ) )

        psize = self.GetClientSize()
        self.centre = wx.Point( int( psize.width / 2 ), int( psize.height / 2 ) )
        self.radius = int( psize.height / 3)

        # Pre-calc as much as we can to save time later
        self.lines = []        # [theta, start pt, end pt, colour]
        # Theta starts at 90-deg and go clockwise (decreasing)
        for theta in range( 90, -270, int( -360 / gl.num_spokes ) ):
            rad_theta = math.radians( theta )
            self.lines.append( [ rad_theta,
                                  self._calc_point( self.centre, self.radius, rad_theta ),
                                  wx.Point(),
                                  None
                                ] )

        # Now subscribe us to the paint event
        self.Bind( wx.EVT_PAINT, self.OnPaint )


    def _calc_point( self, centre, radius, rtheta ):
        ''' Calculates a point on the radius of a circle with given centre radius and angle '''
        pt = wx.Point( centre.x + int( radius * math.cos( rtheta ) ),
                       centre.y - int( radius * math.sin( rtheta ) ) )
        return pt


'''
'''
class CpuMonitorPanel( AMonitorPanel ):
    ''' Monitor panel for CPU usage '''

    def __init__( self, parent, title="" ):
        ''' ctor '''

        AMonitorPanel.__init__( self, parent, title )
        self.work = 0.0
        self.tot = 0.0
        self.spoke = 0


    def OnPaint( self, event ):
        ''' Handle the timer interrupt '''
        print( "Ping!" )

        dc = wx.PaintDC( self )

        length = self.radius * instrument.It.cpu_all[ 2 ]
        if length <= 0.0:
            return
        elif length < self.radius * 0.25:
            colour = wx.Pen( wx.GREEN, 3 ) 
        elif length < self.radius * 0.50:
            colour = wx.Pen( wx.YELLOW, 3 )
        elif length < self.radius * 0.75:
            colour = wx.Pen( wx.TheColourDatabase.Find( "ORANGE" ) )
        else:
            colour = wx.Pen( wx.RED, 3 )

        # Calc the endpoint of the next line
        # spoke [0] == theta in radians, [1] == start point, [2] = end point
        pt = self.lines[ self.spoke ]
        end = self._calc_point( self.centre, self.radius + length, pt[ 0 ] )
        pt[ 2 ] = end
        pt[ 3 ] = colour
        self.spoke += 1

        # Draw *all* lines
        for ln in self.lines:
            if ln[ 3 ] is not None:
                dc.SetPen( ln[ 3 ] );
                dc.DrawLine( ln[ 1 ], ln[ 2 ] )

        dc.SetPen( wx.Pen( wx.BLUE, 5 ) )
        marker = self._calc_point( self.centre, self.radius - 10, pt[ 0 ] )
        print( "S: (%d, %d)" % (pt[1].x, pt[1].y) )
        print( "M: (%d, %d)" % (marker.x, marker.y) )
        dc.DrawLine( marker, marker )
        
        if self.spoke == len( self.lines ):
            self.spoke = 0


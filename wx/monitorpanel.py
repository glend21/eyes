''' GD 20210102
    A wx.Panel that displays an instrument wheel
'''

import math
import time

import wx

import globals as gl
import instrument


class MonitorMenu( wx.Menu ):
    ''' Right-click context menu for a panel '''

    def __init__( self, parent ):
        ''' ctor '''

        wx.Menu.__init__( self )
        self.parent = parent
        self.idmap = {}

        id = wx.NewId()
        min1 = self.AppendRadioItem( id, "2 minutes" )
        self.Bind( wx.EVT_MENU, self.OnAction, min1 )
        self.idmap[ id ] = 2

        id = wx.NewId()
        min5 = self.AppendRadioItem( id, "10 minutes" )
        self.Bind( wx.EVT_MENU, self.OnAction, min5 )
        self.idmap[ id ] = 10
        
        id = wx.NewId()
        min10 = self.AppendRadioItem( id, "30 minutes" )
        self.Bind( wx.EVT_MENU, self.OnAction, min10 )
        self.idmap[ id ] = 30
        
        id = wx.NewId()
        hr1 = self.AppendRadioItem( id, "1 hour" )
        self.Bind( wx.EVT_MENU, self.OnAction, hr1 )
        self.idmap[ id ] = 60
        
        id = wx.NewId()
        hr6 = self.AppendRadioItem( id, "6 hours" )
        self.Bind( wx.EVT_MENU, self.OnAction, hr6 )
        self.idmap[ id ] = 360
        
        id = wx.NewId()
        hr12 = self.AppendRadioItem( id, "12 hours")
        self.Bind( wx.EVT_MENU, self.OnAction, hr12 )
        self.idmap[ id ] = 720
        
        id = wx.NewId()
        hr24 = self.AppendRadioItem( id, "24 hours")
        self.Bind( wx.EVT_MENU, self.OnAction, hr24 )
        self.idmap[ id ] = 1440
        

    def OnAction( self, ev ):
        ''' Handle the menu click '''
        print( ev.GetId() )
        if not self.parent is None:
            self.parent.set_minutes( self.idmap[ ev.GetId() ] )



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
        self.radius = int( psize.height / 4)
        self.spoke = 0
        self.minutes = 2        # Default periord for all panels
        self.ping_count = 0     # Counts up to self.minutes

        # Pre-calc as much as we can to save time later
        self.lines = []        # [theta, start pt, end pt, colour]
        start_time = time.localtime()
        step = int( -360 / gl.num_spokes )
        print( "Starting at ")
        # Theta starts at 90-deg and goes clockwise (decreasing)
        for theta in range( 90, -270, step ):
            rad_theta = math.radians( theta + (start_time.tm_sec * step) )   # step is -ve
            self.lines.append( [ rad_theta,
                                  self._calc_point( self.centre, self.radius, rad_theta ),
                                  wx.Point(),
                                  None
                                ] )

        # Now subscribe us to the events
        self.Bind( wx.EVT_PAINT, self.OnPaint )
        self.Bind( wx.EVT_RIGHT_DOWN, self.OnRightDown )


    @classmethod
    def create( cls, tag, parent, title ):
        ''' Factory method to create the correct sub-class '''
        if tag[ : 3 ] == "cpu":
            return CpuMonitorPanel( parent, title )
        elif tag[ : 3 ] == "mem":
            return MemMonitorPanel( parent, title )
        else:
            return None


    def ping( self ):
        ''' Called by the timer handler, determines if we need to repaint this monitor '''

        if self.ping_count < self.minutes * 60 / gl.num_spokes:
            self.ping_count += 1
        else:
            self.ping_count = 0
            self.Refresh()


    def set_minutes( self, val ):
        ''' Sets the number of minutes per period, clears the display '''
        self.minutes = val
        self.ping_count = 0
        self.spoke = 0
        # self.lines = []

        # Start redrawing from the beginning
        self.Refresh()


    def OnRightDown( self, ev ):
        ''' Right-click handler '''
        self.PopupMenu( MonitorMenu( self ), ev.GetPosition() )


    def _calc_point( self, centre, radius, rtheta ):
        ''' Calculates a point on the radius of a circle with given centre radius and angle '''
        pt = wx.Point( centre.x + int( radius * math.cos( rtheta ) ),
                       centre.y - int( radius * math.sin( rtheta ) ) )
        return pt


    def _draw_label( self, dc, text ):
        ''' Draws the text label on the panel's DC '''
        size = dc.GetTextExtent( text )
        pen = dc.GetPen()
        dc.SetPen( wxPen( wx.BLACK, 3) )
        dc.DrawText( text, 
                     self.radius - int( size.width / 2 ), 
                     self.radius + int( size.height / 2 ) )
        dc.SetPen( pen )


    def _colourise( self, value, bins ):
        ''' Returns a wx.Pen of the correct colour depending on the range of value '''
        floor = 0.0
        for b in bins:
            if value > self.radius * floor and value <= self.radius * b[0]:
                return wx.Pen( b[1], 3 )
            else:
                floor = b[0]

        return None

    def _draw_spoke( self, dc, length, colour ):
        ''' Draws all spokes up to the current one '''
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
        dc.DrawLine( marker, marker )
        
        if self.spoke == len( self.lines ):
            self.spoke = 0

'''
'''
class CpuMonitorPanel( AMonitorPanel ):
    ''' Monitor panel for CPU usage '''

    def __init__( self, parent, title="" ):
        ''' ctor '''
 
        AMonitorPanel.__init__( self, parent, title )
        self.work = 0.0
        self.tot = 0.0
        self.cpu_colours = ( ( 0.25, wx.GREEN ),
                             ( 0.50, wx.YELLOW ),
                             ( 0.75, wx.TheColourDatabase.Find( "ORANGE" ) ),
                             ( 1.0, wx.RED ) )


    def OnPaint( self, event ):
        ''' Handle the timer interrupt '''
        print( "Ping!" )

        dc = wx.PaintDC( self )

        length = self.radius * instrument.It.cpus[ self.title ][ 2 ]
        print( self.title, length )
        colour = self._colourise( length, self.cpu_colours )
        if colour is None:
            print( "no colour" )
            return

        self._draw_spoke( dc, length, colour )


class MemMonitorPanel( AMonitorPanel ):
    ''' Monitor panel for memory usage '''

    def __init__( self, parent, title="" ):
        ''' Ctor '''
        AMonitorPanel.__init__( self, parent, title )
        self.percent = 0.0
        self.mem_colours = ( ( 0.80, wx.GREEN ),
                             ( 0.90, wx.YELLOW),
                             ( 1.00, wx.RED ) )


    def OnPaint( self, event ):
        ''' Handle the paint event from the timer '''
        print( "Mem ping" )

        dc = wx.PaintDC( self )
        length = self.radius * instrument.It.memory / 100.0
        colour = self._colourise( length, self.mem_colours )
        if colour is None:
            return

        self._draw_spoke( dc, length, colour )

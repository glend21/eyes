''' GD 20210102

    The main application frame
'''

import wx

import globals as gl
import monitorpanel as panels
import instrument


class WheelFrame( wx.Frame ):
    def __init__( self, parent, title ):
        ''' ctor '''
        wx.Frame.__init__( self,
                           parent, 
                           title=title, 
                           size=( int(gl.panel_width * 3.3), int(gl.panel_height * 1.5) ) )
        self.CreateStatusBar()

        # The menus
        filemenu = wx.Menu()
        mnuExit = filemenu.Append( wx.ID_EXIT, "E&xit", "Exit the program" )

        toolmenu = wx.Menu()
        toolmenu.Append( 101, "&CPU", "Add CPU monitor" )

        menubar = wx.MenuBar()
        menubar.Append( filemenu, "&File" )
        menubar.Append( toolmenu, "&Tools" )
        self.SetMenuBar( menubar )

        self.SetBackgroundColour( wx.TheColourDatabase.Find( "LIGHT GREY" ) )

        # Event bindings
        self.Bind( wx.EVT_MENU, self.OnExit )

        # Create some static geometry to save time later
        geom = { 
                  "panels" : []
               }
        p = 0
        for r in range( int( gl.max_panels / gl.panels_per_row ) ):
            for c in range( gl.panels_per_row ):
                pos = wx.Point( 10 + c * (gl.panel_width + 10),
                                10 + r * (gl.panel_height + 10) )
                geom[ "panels" ].append( { "origin" : pos } )
                p += 1

        # The sizer to hold the panels
        sizer = wx.GridSizer( cols=3, gap=wx.Size( 10, 10 ) )

        # Create some monitor panels
        self.monitors = []
        for p in range( 2 ):        # For the moment
            monitor = panels.CpuMonitorPanel( self, pos=geom[ "panels" ][ p ][ "origin" ] )
            self.monitors.append( monitor )
            sizer.Add( monitor )
        self.SetSizer( sizer )

        # Create and bind the timer
        self.instrument = instrument.Instrument()

        self.timer = wx.Timer( self )
        self.timer.Start( 1000 )
        self.Bind( wx.EVT_TIMER, self.Ping, self.timer )

        self.Show( True )


    def OnExit( self, ev ):
        self.timer.Stop()
        self.Close( True )


    def Ping( self, ev ):
        ''' Receives the timer notification '''

        # Poll the data collection doolally
        self.instrument.fetch()

        # Now get each monitor to Paint itself
        for monitor in self.monitors:
            monitor.Refresh( eraseBackground=False )

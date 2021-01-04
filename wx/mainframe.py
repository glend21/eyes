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

        self.tool_menu_items = {}
        toolmenu = wx.Menu()
        self.__create_tool_menu( toolmenu )

        menubar = wx.MenuBar()
        menubar.Append( filemenu, "&File" )
        menubar.Append( toolmenu, "&Tools" )
        self.SetMenuBar( menubar )

        self.SetBackgroundColour( wx.TheColourDatabase.Find( "LIGHT GREY" ) )

        # Event bindings
        self.Bind( wx.EVT_MENU, self.OnExit, mnuExit )

        # Create some static geometry to save time later
        self.geom = { 
                      "panels" : []
                    }
        p = 0
        for r in range( int( gl.max_panels / gl.panels_per_row ) ):
            for c in range( gl.panels_per_row ):
                pos = wx.Point( 10 + c * (gl.panel_width + 10),
                                10 + r * (gl.panel_height + 10) )
                self.geom[ "panels" ].append( { "origin" : pos } )
                p += 1

        # The sizer to hold the panels
        self.sizer = wx.GridSizer( cols=3, gap=wx.Size( 10, 10 ) )

        # Create some monitor panels
        self.monitors = []
        '''
        for p in range( 1 ):        # For the moment
            monitor = panels.CpuMonitorPanel( self, pos=geom[ "panels" ][ p ][ "origin" ] )
            self.monitors.append( monitor )
            sizer.Add( monitor )
        '''
        self.SetSizer( self.sizer )

        # Create and bind the timer
        self.timer = wx.Timer( self )
        self.timer.Start( 1000 )
        self.Bind( wx.EVT_TIMER, self.OnTimer, self.timer )

        self.Show( True )


    def __create_tool_menu( self, menu ):
        ''' Adds entries to the Tools menu '''
        for cpu in instrument.It.cpu_names:
            id = wx.NewId()
            print( "Generated ID: %d" % id )
            tool = menu.Append( id, cpu, "Add CPU monitor" )
            self.Bind( wx.EVT_MENU, self.OnAddTool, tool ) #id=id )
            self.tool_menu_items[ id ] = cpu


    #
    # Event handlers
    # 
    def OnExit( self, ev ):
        print( "I shouldn't be here" )
        self.timer.Stop()
        self.Close( True )


    def OnTimer( self, ev ):
        ''' Receives the timer notification '''

        # Poll the data collection doolally
        instrument.It.update()

        # Now get each monitor to Paint itself
        for monitor in self.monitors:
            monitor.Refresh( eraseBackground=False )


    def OnAddTool( self, ev ):
        ''' Adds the specified panel to the main frame '''
        print(" Menu! %d" % ev.GetId() )

        monitor = panels.CpuMonitorPanel( self, title=self.tool_menu_items[ ev.GetId() ] )
        self.monitors.append( monitor )
        self.sizer.Add( monitor )
        self.sizer.Layout()       

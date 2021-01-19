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
        toolmenu = self.__create_tool_menu()
        prefsmenu = self.__create_prefs_menu()
        helpmenu = wx.Menu()
        mnuAbout = helpmenu.Append( wx.ID_ABOUT, "&About", "About" )

        menubar = wx.MenuBar()
        menubar.Append( filemenu, "&File" )
        menubar.Append( toolmenu, "&Tools" )
        menubar.Append( prefsmenu, "&Preferences" )
        menubar.Append( helpmenu, "&Help" )
        self.SetMenuBar( menubar )

        # Event bindings
        self.Bind( wx.EVT_MENU, self.OnExit, mnuExit )
        self.Bind( wx.EVT_MENU, self.OnAbout, mnuAbout )

        self.SetBackgroundColour( wx.TheColourDatabase.Find( "LIGHT GREY" ) )

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


    def __create_tool_menu( self ):
        ''' Creates and adds entries to the Tools menu '''

        menu = wx.Menu()
        # FIXME pre-creating all the monitor panels here, rather than when they are added to the main frame
        for cpu in instrument.It.cpus:
            id = wx.NewId()
            tool = menu.Append( id, cpu, "Add CPU monitor" )
            self.Bind( wx.EVT_MENU, self.OnAddTool, tool )
            self.tool_menu_items[ id ] = cpu

        id = wx.NewId()
        tool = menu.Append( id, "mem", "Add Memory monitor" )
        self.Bind( wx.EVT_MENU, self.OnAddTool, tool )
        self.tool_menu_items[ id ] = "mem"

        id = wx.NewId()
        tool = menu.Append( id, "net", "Add network menu" )
        self.Bind( wx.EVT_MENU, self.OnAddTool, tool )
        self.tool_menu_items[ id ] = "net"

        return menu


    def __create_prefs_menu( self ):
        ''' Creates and adds entries to the Preferences menu '''
        menu = wx.Menu()
        id = wx.NewId()
        pref = menu.AppendCheckItem( id, "Log output to file ...", "Log output to file" )
        self.Bind( wx.EVT_MENU, self.OnLogToggle, pref )

        return menu


    #
    # Event handlers
    # 
    def OnExit( self, ev ):
        self.timer.Stop()
        self.Close( True )

    def OnAbout( self, ev ):
        title = "System Eyes"
        dlg = wx.MessageDialog( self, title, title, wx.ICON_INFORMATION | wx.OK )
        dlg.ShowModal()
        dlg.Destroy()

    def OnTimer( self, ev ):
        ''' Receives the timer notification '''

        # Poll the data collection doolally
        instrument.It.update()

        # Now get each monitor to Paint itself
        for monitor in self.monitors:
            monitor.ping()


    def OnAddTool( self, ev ):
        ''' Adds the specified panel to the main frame '''

        tag = self.tool_menu_items[ ev.GetId() ]
        monitor = panels.AMonitorPanel.create( tag, self, tag )
        self.monitors.append( monitor )
        self.sizer.Add( monitor )
        self.sizer.Layout()       


    def OnLogToggle( self, ev ):
        ''' When the user selects or deselects to output to a file '''
        print( "Hi Sparky" )

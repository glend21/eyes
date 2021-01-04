The main app is a Frame
It can contain up to 9 MonitorPanels, each of which is a wxPanel containing a wxDC
The panel sizes are fixed, the size of the main frame adjusts per the number of panels it contains
The panel bulk calculates all the coordinates it can on __init__, to speed up drawing time
There is one InstrumentCache which is responsible for fetching all system data per interval
MonitorPanel sub-classes do the actual work of fetching the data from the cache
The MonitorPanel runs in a separate thread, and maintains a history of previous observations
A timer pings once per second, signals the thread to grab the latest data, and updates each panel in turn

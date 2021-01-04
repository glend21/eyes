''' GD 20210102

    Little attempt to poll CPU usage and display it as a test histogram to the terminal
'''

import os
import sys
import time
import threading


class Repeater( threading.Timer ):
    def run( self):
        print("Hi there")
        while not self.finished.wait( self.interval ):
            self.function( *self.args, **self.kwargs )


cpu_work = 0
cpu_tot = 0


def usage():
    ''' Get the CPU usage and calc the percentage '''

    global cpu_work, cpu_tot

    # Make the IO as efficient as possible
    # The aggregated CPU data is on the first line
    with open( "/proc/stat", "rt" ) as ifh:
        ln = ifh.readline()

    vals = [ int( v ) for v in ln.split()[ 1 : ] ]
    work = sum( vals[ : 3 ] )
    tot = sum( vals )

    cpu_perc = 0.0
    if cpu_tot > 0:
        cpu_perc = (work - cpu_work) / (tot - cpu_tot) * 100.0

    cpu_work = work
    cpu_tot = tot

    print( "%s [%.1f]" % ('#' * int( cpu_perc ), cpu_perc) )
    return cpu_perc



def main( argc, argv ):
    ''' It '''

    '''
    for i in range( 10 ):
        u = usage()
        print( "%s [%.1f]" % ('#' * int( u ), u) )
        time.sleep( 2 )
    '''

    timer = Repeater( 2, usage )
    timer.start()
    threading.Event().wait( )
    timer.cancel()



if __name__ =="__main__":
    main( len( sys.argv ), sys.argv )

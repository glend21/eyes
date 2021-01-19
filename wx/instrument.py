''' GD 20210104

    Gets and caches all the system information
'''

import psutil


class Instrument():
    def __init__( self ):
        # CPU data is stores as a tuple (work, tot, perc)
        #self.num_cpus = 0
        self.cpus = {}
        self.memory = 0.0
        # self.cpu_all = (0, 0, 0.0)
        #self.cpu_names = [ "CPU all" ]

        # Create an empty list of CPU data
        with open( "/proc/stat", "rt") as ifh:
            while True:
                tag = ifh.readline().split()[ 0 ]
                # The first lines in the file all refer to cpu data
                if tag[ 0 : 3 ] == "cpu":
                    self.cpus[ tag ] = (0, 0, 0.0)
                else:
                    break
        print( self.cpus )

    def update( self ):
        ''' Reads all system data '''

        #
        # CPU

        # Make the IO as efficient as possible
        # The aggregated CPU data is on the first line
        with open( "/proc/stat", "rt" ) as ifh:
            while True:
                fields = ifh.readline().split()
                if fields[ 0 ][ 0 : 3 ] == "cpu":
                    self.cpus[ fields[ 0 ] ] = self.__calc_perc( fields )
                else:
                    break

        #
        # Memory
        mem = psutil.virtual_memory()
        self.memory = mem.percent


    def __calc_perc( self, fields ):
        ''' Parses the line and calculates the CPU 
            Returns a tuple of (work jiffies, total jiffies, usage 0.0 u < 1.0)
        '''

        vals = [ int( v ) for v in fields[ 1 : ] ] 
        prev = self.cpus[ fields[ 0 ] ]
        work = sum( vals[ : 3 ] )
        tot = sum( vals )
        
        if prev[ 1 ] > 0:
            perc = (work - prev[ 0 ]) / (tot - prev[ 1 ])
        else:
            perc = 0.0

        #print( "%s [%.1f]" % ('#' * int( cpu_perc ), cpu_perc) )
        return (work, tot, perc)


# Semi-singleton instance
It = Instrument()

''' GD 20210104

    Gets and caches all the system information
'''

class Instrument:
    def __init__( self ):
        # CPU data is stores as a tuple (work, tot, perc)
        self.num_cpus = 0
        self.cpus = []
        self.cpu_all = (0, 0, 0.0)

        with open( "/proc/stat", "rt") as ifh:
            while True:
                tag = ifh.readline().split()[ 0 ]
                # The first lines in the file all refer to cpu data
                # The very first line is total data across all cpus, so skip it
                if tag[ 0 : 3 ] == "cpu":
                    if len( tag ) > 3:
                        self.cpus.append( (0, 0, 0.0) )
                else:
                    break


    def fetch( self ):
        ''' Reads all system data '''

        # Make the IO as efficient as possible
        # The aggregated CPU data is on the first line
        with open( "/proc/stat", "rt" ) as ifh:
            ln = ifh.readline()
            self.cpu_all = self.__calc_perc( -1, ln )

            # There must be at least one numbered CPU
            for n in range( 10000 ):
                ln = ifh.readline()
                if ln[ : 3 ] == "cpu":
                    self.cpus[ n ] = self.__calc_perc( n, ln )
                else:
                    break

            self.num_cpus = n


    def __calc_perc( self, n, ln ):
        ''' Parses the line and calculates the CPU 
            Returns a tuple of (work jiffies, total jiffies, usage 0.0 u < 1.0)
        '''

        vals = [ int( v ) for v in ln.split()[ 1 : ] ]
        work = sum( vals[ : 3 ] )
        tot = sum( vals )

        if n == -1:
            cpu = self.cpu_all
        else:
            cpu = self.cpus[ n ]

        if cpu[ 1 ] > 0:
            perc = (work - cpu[ 0 ]) / (tot - cpu[ 1 ])
        else:
            perc = 0.0
        print( "%.1f" % perc )

        #print( "%s [%.1f]" % ('#' * int( cpu_perc ), cpu_perc) )
        return (work, tot, perc)

#!/usr/bin/env python

"""
MODULE:     r.in.narr

AUTHOR(S):  Julien Seguinot <julien.seguino@natgeo.su.se>.

PURPOSE:    Import North American Regional Reanalysis fields from the ESRL
            Physical Science Division [1] netCDF data files.

COPYRIGHT:  (c) 2011-2014 Julien Seguinot

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

#%Module
#% description: Import North American Regional Reanalysis netCDF data files
#% keywords: raster import NARR PSD
#%End

#%option
#% key: input
#% type: string
#% gisprompt: old,file,input
#% description: NetCDF file to be imported
#% required: yes
#%end
#%option
#% key: var
#% type: string
#% description: NetCDF variable to be imported
#% required: yes
#%end
#%option
#% key: prefix
#% type: string
#% description: Prefix for output raster maps (default: narr_)
#% required: no
#% answer: narr_
#%end

from numpy import flipud        # scientific module Numpy [2]
from netCDF4 import Dataset     # interface to netCDF4 library [3]
from grass.script import core as grass
from grass.script import array as garray


def main():
    """Main function, called at execution time"""

    # parse arguments
    input = options['input']
    var = options['var']
    prefix = options['prefix']

    # read NetCDF data
    nc = Dataset(input, 'r')
    data = nc.variables[var][:]
    nc.close()

    # set temporary region
    res = 32463.0
    rows = 277
    cols = 349
    grass.run_command('g.region',
                      n=res*(rows-0.5), s=res*-0.5,
                      e=res*(cols-0.5), w=res*-0.5,
                      rows=rows, cols=cols)

    # for each month
    a = garray.array()
    for (i, timeslice) in enumerate(data):
        mapname = prefix + '%02i' % (i+1)
        grass.message('Importing ' + mapname + ' ...')

        # import data with grass array
        a[:] = flipud(timeslice)
        a.write(mapname=mapname, overwrite=True, null=-32767)

if __name__ == "__main__":
    options, flags = grass.parser()
    main()

# Links
# [1] http://www.esrl.noaa.gov/psd/data/gridded/data.narr.html
# [2] http://numpy.scipy.org
# [3] http://netcdf4-python.googlecode.com


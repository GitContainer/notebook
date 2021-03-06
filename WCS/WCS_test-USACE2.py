# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Extract data from USACE WCS Service

# <codecell>

from owslib.wcs import WebCoverageService
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from owslib.wcs import WebCoverageService
%matplotlib inline

# <codecell>

endpoint='http://gis.sam.usace.army.mil/server/services/JALBTCX/NCMP_BareEarth_1m/ImageServer/WCSServer?request=GetCapabilities&service=WCS'
#endpoint='http://gis.sam.usace.army.mil/server/services/JALBTCX/NCMP_2005_MA_BareEarth_1m/ImageServer/WCSServer?request=GetCapabilities&service=WCS'

# <codecell>

wcs = WebCoverageService(endpoint,version='1.0.0',timeout=60)

# <codecell>

for k,v in wcs.contents.iteritems():
    print v.title

# <codecell>

wcs.contents

# <codecell>

lidar = wcs['1']
print lidar.title
print lidar.boundingBoxWGS84
print lidar.timelimits
print lidar.supportedFormats

# <codecell>

# try Plum Island Sound Region
bbox = (-70.825,42.671,-70.7526,42.762)
output = wcs.getCoverage(identifier="1",bbox=bbox,crs='EPSG:4326',format='GeoTIFF',
                         resx=0.0001, resy=0.0001)

# <codecell>

f=open('test.tif','wb')
f.write(output.read())
f.close()

# <codecell>

from osgeo import gdal
gdal.UseExceptions()

# <codecell>

ds = gdal.Open('test.tif')

# <codecell>

band = ds.GetRasterBand(1)
elevation = band.ReadAsArray()
nrows, ncols = elevation.shape

# I'm making the assumption that the image isn't rotated/skewed/etc. 
# This is not the correct method in general, but let's ignore that for now
# If dxdy or dydx aren't 0, then this will be incorrect
x0, dx, dxdy, y0, dydx, dy = ds.GetGeoTransform()

if dxdy == 0.0:
    x1 = x0 + dx * ncols
    y1 = y0 + dy * nrows

# <codecell>

import cartopy.crs as ccrs
from cartopy.io.img_tiles import MapQuestOpenAerial, MapQuestOSM, OSM

# <codecell>

print x0,x1,y1,y0

# <codecell>

elevation=ma.masked_equal(elevation,0)

# <codecell>

plt.figure(figsize=(8,10))
ax = plt.axes(projection=ccrs.PlateCarree())
tiler = MapQuestOpenAerial()
ax.add_image(tiler, 14)
plt.imshow(elevation, cmap='jet', extent=[x0, x1, y1, y0],
           transform=ccrs.PlateCarree(),alpha=0.6,zorder=2);
ax.gridlines(draw_labels=True,zorder=3);


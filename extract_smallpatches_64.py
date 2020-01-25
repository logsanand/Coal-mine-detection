
from osgeo import gdal_array as gdarr
from osgeo import gdal, osr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geopandas
from geopandas import GeoDataFrame
from shapely.geometry import Point
import math
import os
import glob

image_list = []
for filename in glob.glob(r'\*.tif'): #assuming gif  
	image_list.append(filename)
	print(image_list)

#I access the satellite images (I just show one here to make it short)
for j in range(len(image_list)):
	sentin_band = image_list[j]
	head, tail = os.path.split(sentin_band)
	filename1=tail.split('.')[0]
	print(filename1)
	path=r''
	path2=r''
	file2=filename1+'_lon'
	file3=filename1+'_lat'
	format='.txt'
	file4=os.path.join(path,file2+format)
	file5=os.path.join(path,file3+format)
	ds = gdal.Open(sentin_band, gdal.GA_ReadOnly)
	gt = ds.GetGeoTransform()  # Geotransforms allow conversion of pixel to map coordinates
	crs = ds.GetProjection()  
	
	
	with open(file4, "r") as f:
		lon = [float(line.rstrip()) for line in f]
		
	#print('lon',lon)
	with open(file5, "r") as f1:
		lat = [float(line.rstrip().replace('\U00002013', '-')) for line in f1]
		
	#print(lat)
	#lon= [ 78.678000, 78.681624] # Assume EPSG:4326 (WGS84) https://epsg.io/4326
	#lat=[ 22.183175, 22.183170]

	for i in range(len(lon)):
		# Reproject lon/lat to CRS of raster (UTM in this case)
		source = osr.SpatialReference()
		source.ImportFromEPSG(4326)  # WGS84 4326
		target = osr.SpatialReference()
		target.ImportFromWkt(crs)
		#print(lon[i])
		transform = osr.CoordinateTransformation(source, target)
		print(lon[i], lat[i])
		mx, my, z = transform.TransformPoint(lon[i], lat[i])
		# Inverse GT to convert from map to pixel
		inv_gt = gdal.InvGeoTransform(gt)  
		px,py=gdal.ApplyGeoTransform(inv_gt,mx,my)
		# Apply the inverse GT and truncate the decimal places.
		px, py = (math.floor(f) for f in gdal.ApplyGeoTransform(inv_gt, mx, my))
		#print(px,py)

		xoff=px
		yoff=py
		win_x=64
		win_y=64

		px1=gdarr.DatasetReadAsArray(ds,xoff,yoff,win_x,win_y)
		print(px1.shape[2])
		#plt.imshow(px1[1,:,:])
		#plt.show()
		#print(px1[1,1,1])
		print(px1[1,63,63])
		driver = gdal.GetDriverByName('GTiff')      # we can choose a diferent format e.g. XYZ
		newRaster = driver.Create(path2+filename1+'_'+str(i)+'.tif',px1.shape[2],px1.shape[1], 13,  gdal.GDT_UInt16)
		prj = ds.GetProjection()                         # definenew raster dataset proj. & geotransform
		newRaster.SetProjection(prj)
		newtfcoord=gdal.ApplyGeoTransform(gt,px,py)
		newRaster.SetGeoTransform([newtfcoord[0],10,0,newtfcoord[1],0,-10])# We can use the same GT because TL is same
		#newBand = newRaster.GetRasterBand(1) # get band 1 so we can fill it with data
		print(newRaster.RasterXSize)
		print(newRaster.RasterCount)
		print(newRaster.RasterYSize)
		#newRaster.WriteRaster(0,0,px1.shape[2],px1.shape[1],px1.tostring())                          # write the array to the band
		for i, image in enumerate(px1, 1):
			newRaster.GetRasterBand(i).WriteArray(image)
		newRaster = None 


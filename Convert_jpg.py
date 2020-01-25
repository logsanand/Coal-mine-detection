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
for filename in glob.glob(r'/*.tif'): #assuming gif  
	image_list.append(filename)
	#print(image_list)

for j in range(len(image_list)):
	sentin_band = image_list[j]
	head, tail = os.path.split(sentin_band)
	filename1=tail.split('.')[0]
	print(filename1)
	path=r''
	scale = '-scale min_val max_val'
	options_list = [
		'-ot Byte',
		'-of JPEG',
		scale
	] 
	options_string = " ".join(options_list)

	gdal.Translate(path+filename1+'.jpg',
				   image_list[j],options=options_string)
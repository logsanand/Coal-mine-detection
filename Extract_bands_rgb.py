import gdal
import subprocess
import glob
import os
image_list = []
for filename in glob.glob(r'/*.tif'): #assuming gif  
	image_list.append(filename)
	#print(image_list)
for j in range(len(image_list)):
    head, tail = os.path.split(image_list[j])
    filename1=tail.split('.')[0]
    print(filename1)
    path=r'/'
    subprocess.call(["gdal_translate","-of","Gtiff","-b","4","-b","3", "-b","2",image_list[j],path+filename1+".tif"])
	
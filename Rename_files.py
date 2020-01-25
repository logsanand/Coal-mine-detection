
import os
import glob

Left = glob.glob("/*.tif")
print(Left[0])
path1="/"
count=0
for file in Left:
	filename=os.path.split(file)
	#print(filename)
	new_name=path1+"NoMines"+"_"+str(count)+".tif"
	os.rename(path1+filename[1],new_name)
	#print(new_name)
	count=count+1

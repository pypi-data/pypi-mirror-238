import os
from osgeo import gdal
import numpy

gdal.AllRegister()

file = "./demo/00002.tif"
(fileRoot, fileExt) = os.path.splitext(file)
outFileName = fileRoot + "_mod" + fileExt

ds = gdal.Open(file)
band = ds.GetRasterBand(1)

arr = band.ReadAsArray()

[cols, rows] = arr.shape
arr_min = arr.min()
arr_max = arr.max()
arr_mean = int(arr.mean())

arr_out = numpy.where((arr < arr_mean), 10000, arr)

driver = gdal.GetDriverByName("GTiff")
outdata = driver.Create(outFileName, rows, cols, 1, gdal.GDT_UInt16)
outband = outdata.GetRasterBand(1)
outband.SetUnitType("myFavouriteGame")
outband.WriteArray(arr_out)
outdata = None

###

ds = gdal.Open("./demo/00002_mod.tif")
band = ds.GetRasterBand(1)
print('unit',band.GetUnitType())
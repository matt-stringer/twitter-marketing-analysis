from osgeo import ogr
import struct


shapefile = ogr.Open("tl_2013_06_sldl/tl_2013_06_sldl.shp")
layer = shapefile.GetLayer(0)

for i in range(layer.GetFeatureCount()):
	feature = layer.GetFeature(i)
	geometry = feature.GetGeometryRef()

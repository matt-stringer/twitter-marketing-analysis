from osgeo import ogr
import shapely.wkt

import pyprojb
# Load the thai and myanmar polygons from the world borders
# dataset.
shapefile = ogr.Open("TM_WORLD_BORDERS-0.3/TM_WORLD_BORDERS-0.3.shp")
layer = shapefile.GetLayer(0)
thailand = None
myanmar = None
for i in range(layer.GetFeatureCount()):
	feature = layer.GetFeature(i)
	if feature.GetField("ISO2") == "TH":
		geometry = feature.GetGeometryRef()
		thailand = shapely.wkt.loads(geometry.ExportToWkt())
	elif feature.GetField("ISO2") == "MM":
		geometry = feature.GetGeometryRef()
		myanmar = shapely.wkt.loads(geometry.ExportToWkt())
# Calculate the common border.
commonBorder = thailand.intersection(myanmar)
# Save the common border into a new shapefile.



spatialReference = osr.SpatialReference()
spatialReference.SetWellKnownGeogCS('WGS84')
driver = ogr.GetDriverByName("ESRI Shapefile")
dstPath = os.path.join("common-border", "border.shp")
dstFile = driver.CreateDataSource(dstPath)
dstLayer = dstFile.CreateLayer("layer", spatialReference)
wkt = shapely.wkt.dumps(commonBorder)

feature = ogr.Feature(dstLayer.GetLayerDefn())
feature.SetGeometry(ogr.CreateGeometryFromWkt(wkt))
dstLayer.CreateFeature(feature)
feature.Destroy()
dstFile.Destroy()
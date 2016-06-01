#!/usr/bin/python
# -*- coding: latin-1 -*-

import os, sys


from osgeo import gdal,gdalconst
import struct



def findPoints(geometry, results):
    for i in range(geometry.GetPointCount()):
       x,y,z = geometry.GetPoint(i)
       if results['north'] == None or results['north'][1] < y:
       		results['north'] = (x,y)
       if results['south'] == None or results['south'][1] > y:
         	results['south'] = (x,y)


for i in range(geometry.GetGeometryCount()):
	findPoints(geometry.GetGeometryRef(i), results)

		

shapefile = osgeo.ogr.Open("california.shp")
layer = shapefile.GetLayer(0)
numLayers = shapefile.GetLayerCount()
feature = layer.GetFeature(55)

results = {'north' : None,
           'south' : None}

findPoints(geometry, results)

print "Northernmost point is (%0.4f, %0.4f)" % results['north']
print "Southernmost point is (%0.4f, %0.4f)" % results['south']



for layerNum in range(numLayers):
	layer = shapefile.GetLayer(layerNum)
	
	numFeatures = layer.GetFeatureCount()
	print "Layer %d has %d features:" % (layerNum, numFeatures)
	print

	for featureNum in range(numFeatures):



	 	feature = layer.GetFeature(featureNum)
		
		geometry = feature.GetGeometryRef()

		

    
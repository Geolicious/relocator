# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qgis2leaf
								 A QGIS plugin
 QGIS to Leaflet creation program
							 -------------------
		begin				: 2014-04-29
		copyright			: (C) 2013 by Riccardo Klinger
		email				: riccardo.klinger@geolicious.com
 ***************************************************************************/

/***************************************************************************
 *																		 *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or	 *
 *   (at your option) any later version.								   *
 *																		 *
 ***************************************************************************/
"""

from PyQt4.QtCore import QFileInfo
import osgeo.ogr, osgeo.osr #we will need some packages
from osgeo import ogr
from osgeo import gdal
import processing
import shutil
from qgis.core import *
import qgis.utils
import os #for file writing/folder actions
import shutil #for reverse removing directories
import urllib # to get files from the web
from urlparse import parse_qs
import time
import tempfile
import re
import fileinput
import webbrowser #to open the made map directly in your browser
import sys #to use another print command without annoying newline characters 
from xml.etree import ElementTree as et
import zipfile

def relocator_exec(path_r, zipit):
	print "project relocated to " + str(path_r)
	path_r = os.path.join(path_r, 'export_' + str(time.strftime("%Y_%m_%d")) + '_' + str(time.strftime("%I_%M_%S")))
	os.makedirs(path_r)

	canvas = qgis.utils.iface.mapCanvas()
	allLayers = canvas.layers()
	proj=QgsProject.instance()
	path= proj.homePath()
	for i in allLayers:
		#first for vector files:
		if i.dataProvider().name() != "wms":
			if i.type()==0:
				(Directory,nameFile) = os.path.split(i.dataProvider().dataSourceUri())
				QgsVectorFileWriter.writeAsVectorFormat(i,path_r + os.sep + nameFile.split("|",1)[0],"utf-8",i.crs(),"ESRI Shapefile")
				print i.name() + " is vector"
				#print i.dataProvider().name()
			#now for raster
			if i.type() == 1:
				(Directory,nameFile) = os.path.split(i.dataProvider().dataSourceUri())
				print nameFile
				for root, dirs, files in os.walk(Directory):
					if root == Directory:
						first_part = nameFile.partition(".")[0]
						print first_part + " is raster"
						for file1 in files:
							m = re.search(first_part, file1)
							if m and m.group(0)!= '' :
								print file1 + " is a match!"
								shutil.copyfile(Directory + os.sep + file1, path_r + os.sep + file1)
	filename = proj.fileName()
	filename=filename.replace(path, path_r)
	shutil.copyfile(proj.fileName(), filename)
	tree = et.parse(filename)
	root = tree.getroot()
	for layer in allLayers:
		(Directory,nameFile) = os.path.split(layer.dataProvider().dataSourceUri())
		if (layer.type() == 0 or layer.type() == 1) and layer.dataProvider().name() != "wms":
			print nameFile
			for maplayer in root.iter('projectlayers'):
				for datasource in maplayer.iter('datasource'):
					m = re.search(nameFile, datasource.text)
					if m:
						(Directory2,nameFile2) = os.path.split(datasource.text)
						datasource.text = "./" + str(nameFile2)
						tree.write(filename)			
	if zipit == 1:
		zf = zipfile.ZipFile(os.path.abspath(os.path.join(path_r, os.pardir)) +  os.sep + "myzipfile.zip", "w")
		for dirname, subdirs, files in os.walk(path_r):
			zf.write(dirname)
			for filename in files:
				zf.write(os.path.join(dirname, filename))
		zf.close()


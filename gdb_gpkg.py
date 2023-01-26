# libraries
import os, subprocess, zipfile, fnmatch, shutil, pygeopkg, osgeo
from pygeopkg.core.geopkg import GeoPackage
from osgeo import ogr
# set variables
wd = “/Users/morgan.rohansmith/Documents/recreation_points”
zdir = wd + “/source/zip”
edir = wd + “/source/extract”
qdir = wd + “/process”
zzdir = wd + “/zip”
pattern = ‘*.zip’

# create working directories
if not os.path.exists(wd):
    os.makedirs(zdir)
    os.makedirs(edir)
    os.makedirs(qdir)
    os.makedirs(zzdir)
print(“Download and move all gdbs to ” + zdir + ” and press Enter to continue”)
input(“...“)

# unzip all gdbs to working directory and keep the gdb name
for root, dirs, files in os.walk(zdir):
    for filename in fnmatch.filter(files, pattern):
        print(os.path.join(root, filename))
        zipfile.ZipFile(os.path.join(root, filename)).extractall(os.path.join(root, os.path.splitext(filename)[0]))
        print(“|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|“)
        print(“”)
# make a list of all extracted gdbs
for root, dir, files in os.walk(zdir):
    for dirname in dir:
        if dirname.endswith(‘.gdb’):
            thefile = os.path.join(root, dirname)
            try:
                shutil.move(thefile, edir)
            except:
                print(“WTF is going on???“)
# create a gpkg for each gdb, using the same name
for root, dir, files in os.walk(edir):
    for dirname in dir:
        if dirname.endswith(‘.gdb’):
            thefile = os.path.join(root, dirname)
            print(thefile)
            gpkg = GeoPackage.create(qdir + “/” + dirname + “.gpkg”, flavor=‘EPSG’)
            driver = ogr.GetDriverByName(“OpenFileGDB”)
            data = driver.Open(dirname, 0)
            fcl = []
            for i in data:
                fc = i.GetName()
                fcl.append(fc)
            for fc in fcl:
                gdbLyr = QgsVectorLayer(“{0}|layername={1}“.format(fgdb, fc), fc, “ogr”)
                print(‘Writing: ’, fc)
                options = QgsVectorFileWriter.SaveVectorOptions()
                options.driverName = “GPKG”
                options.layerName = fc
                options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
                options.EditionCapability = 0 #CanAddNewLayer
                QgsVectorFileWriter.writeAsVectorFormat(gdbLyr, gpkg, options)

#       for i in list_of_gdbs:
#           create gpkg:
#               list feature classes in gdb, and convert to feature class within the gpkg

# zip all gpkgs

# remove working directories

"""
   Copyright 2023 Ian Housman

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


#Example of how to run the LANDTRENDR temporal segmentation algorithm and view outputs using the Python visualization tools
#LANDTRENDR original paper: https://www.sciencedirect.com/science/article/pii/S0034425710002245
#LANDTRENDR in GEE paper: https://www.mdpi.com/2072-4292/10/5/691
#Acquires Landsat data, runs LANDTRENDR, and then adds some outputs to the viewer
####################################################################################################
import os,sys
sys.path.append(os.getcwd())

#Module imports
import geeViz.getImagesLib as getImagesLib
import geeViz.changeDetectionLib as changeDetectionLib
import geeViz.taskManagerLib as taskManagerLib
ee = getImagesLib.ee
Map = getImagesLib.Map
Map.clearMap()
####################################################################################################
# Define user parameters:

# Specify study area: Study area
# Can be a featureCollection, feature, or geometry
studyArea = getImagesLib.testAreas['CA']

# Update the startJulian and endJulian variables to indicate your seasonal 
# constraints. This supports wrapping for tropics and southern hemisphere.
# If using wrapping and the majority of the days occur in the second year, the system:time_start will default 
# to June 1 of that year.Otherwise, all system:time_starts will default to June 1 of the given year
# startJulian: Starting Julian date 
# endJulian: Ending Julian date
startJulian = 152
endJulian = 273

# Specify start and end years for all analyses
# More than a 3 year span should be provided for time series methods to work 
# well. If using Fmask as the cloud/cloud shadow masking method, or providing
# pre-computed stats for cloudScore and TDOM, this does not 
# matter
startYear = 1990  
endYear = 2022



#Choose band or index
#NBR, NDMI, and NDVI tend to work best
#Other good options are wetness and tcAngleBG
indexName = 'NBR'

#How many significant loss and/or gain segments to include
#Do not make less than 1
#If you only want the first loss and/or gain, choose 1
#Generally any past 2 are noise
howManyToPull = 1

#Parameters to identify suitable LANDTRENDR segments

#Thresholds to identify loss in vegetation
#Any segment that has a change magnitude or slope less than both of these thresholds is omitted
lossMagThresh = -0.15
lossSlopeThresh = -0.05


#Thresholds to identify gain in vegetation
#Any segment that has a change magnitude or slope greater than both of these thresholds is omitted
gainMagThresh = 0.1
gainSlopeThresh = 0.05

slowLossDurationThresh = 3

#Choose from: 'newest','oldest','largest','smallest','steepest','mostGradual','shortest','longest'
chooseWhichLoss = 'largest'
chooseWhichGain = 'largest'

#LandTrendr Params
# run_params ={
#   'timeSeries': (ImageCollection) Yearly time-series from which to extract breakpoints. The first band is used to find breakpoints, and all subsequent bands are fitted using those breakpoints.
#   'maxSegments':            6,\ (Integer) Maximum number of segments to be fitted on the time series.
#   'spikeThreshold':         0.9,\ (Float, default: 0.9) Threshold for damping the spikes (1.0 means no damping).
#   'vertexCountOvershoot':   3,\(Integer, default: 3) The initial model can overshoot the maxSegments + 1 vertices by this amount. Later, it will be pruned down to maxSegments + 1.
#   'preventOneYearRecovery': False,\(Boolean, default: False): Prevent segments that represent one year recoveries.
#   'recoveryThreshold':      0.25,\(Float, default: 0.25) If a segment has a recovery rate faster than 1/recoveryThreshold (in years), then the segment is disallowed.
#   'pvalThreshold':          0.05,\(Float, default: 0.1) If the p-value of the fitted model exceeds this threshold, then the current model is discarded and another one is fitted using the Levenberg-Marquardt optimizer.
#   'bestModelProportion':    0.75,\(Float, default: 0.75) Allows models with more vertices to be chosen if their p-value is no more than (2 - bestModelProportion) times the p-value of the best model.
#   'minObservationsNeeded':  6\(Integer, default: 6) Min observations needed to perform output fitting.
# };
#Define landtrendr params
run_params = { \
  'maxSegments':            6,\
  'spikeThreshold':         0.9,\
  'vertexCountOvershoot':   3,\
  'preventOneYearRecovery': True,\
  'recoveryThreshold':      0.25,\
  'pvalThreshold':          0.05,\
  'bestModelProportion':    0.75,\
  'minObservationsNeeded':  6\
}

#Whether to add outputs to map
addToMap = True

#Export params
#Whether to export LANDTRENDR outputs
exportLTStack = False

# Whether to export LandTrendr vertex array raw output
exportLTRawArray = True

#Set up Names for the export
outputName = 'LT_Test'

#Provide location composites will be exported to
#This should be an asset imageCollection
exportPathRoot = 'users/username/someCollection'



#CRS- must be provided.  
#Common crs codes: Web mercator is EPSG:4326, USGS Albers is EPSG:5070, 
#WGS84 UTM N hemisphere is EPSG:326+ zone number (zone 12 N would be EPSG:32612) and S hemisphere is EPSG:327+ zone number
crs = 'EPSG:5070'

#Specify transform if scale is None and snapping to known grid is needed
transform = [30,0,-2361915.0,0,-30,3177735.0]

#Specify scale if transform is None
scale = None
####################################################################################################
#End user parameters
####################################################################################################
####################################################################################################
####################################################################################################
#Start function calls
####################################################################################################
hansen = ee.Image("UMD/hansen/global_forest_change_2020_v1_8").select(['lossyear']).add(2000).int16()
hansen = hansen.updateMask(hansen.neq(2000).And(hansen.gte(startYear)).And(hansen.lte(endYear)))
Map.addLayer(hansen,{'min':startYear,'max':endYear,'palette':changeDetectionLib.lossYearPalette},'Hansen Loss Year',False)

####################################################################################################
#Call on master wrapper function to get Landat scenes and composites
# Important that the range of data values of the composites match the run_params spikeThreshold and recoveryThreshold
# e.g. Reflectance bands that have a scale of 0-1 should have a spikeThreshold around 0.9
# and a recoveryThreshold around 0.25
# If the reflectance values were scaled by 10000, the spikeThreshold would be around 9000 
# and a recoveryThreshold around 2500
allImages = getImagesLib.getProcessedLandsatScenes(studyArea,startYear,endYear,startJulian,endJulian).select([indexName])
dummyImage = allImages.first()
composites = ee.ImageCollection(ee.List.sequence(startYear,endYear).map(lambda yr: getImagesLib.fillEmptyCollections(allImages.filter(ee.Filter.calendarRange(yr,yr,'year')),dummyImage).median().set('system:time_start',ee.Date.fromYMD(yr,6,1).millis())))

#Run LANDTRENDR
ltOut = changeDetectionLib.simpleLANDTRENDR(composites,startYear,endYear,indexName, run_params,lossMagThresh,lossSlopeThresh,\
                                                gainMagThresh,gainSlopeThresh,slowLossDurationThresh,chooseWhichLoss,\
                                                chooseWhichGain,addToMap,howManyToPull)
if exportLTStack:
  ltOutStack = ltOut[1]

  #Export  stack
  exportName = outputName + '_Stack_'+indexName + '_'+str(startYear) + '_' + str(endYear) + '_' + str(startJulian) + '_' + str(endJulian)
  exportPath = exportPathRoot + '/'+ exportName

  #Set up proper resampling for each band
  #Be sure to change if the band names for the exported image change
  pyrObj = {'_yr_':'mode','_dur_':'mode','_mag_':'mean','_slope_':'mean'}
  possible = ['loss','gain']
  how_many_list = ee.List.sequence(1,howManyToPull).getInfo()
  outObj = {}
  for p in possible:
    for key in pyrObj.keys():
      for i in how_many_list:
        i = int(i)
        kt = indexName + '_LT_'+p + key+str(i)
        outObj[kt]= pyrObj[key]

  
  #Export output
  getImagesLib.exportToAssetWrapper(ltOutStack,exportName,exportPath,outObj,studyArea,scale,crs,transform)


#Export raw LandTrendr array image
if exportLTRawArray:
  rawLT = ltOut[0]
  rawLTForExport = changeDetectionLib.rawLTToVertices(rawLT,indexName,10000).int16()
  Map.addLayer(rawLT,{},'Raw LT {}'.format(indexName),False)
  Map.addLayer(rawLTForExport,{},'Raw LT For Export {}'.format(indexName),False)
  
  rawLTForExport = rawLTForExport.set({'startYear':startYear,
                                        'endYear':endYear,
                                        'startJulian':startJulian,
                                        'endJulian':endJulian,
                                        'band':indexName})
  rawLTForExport =rawLTForExport.set(run_params)
  exportName = '{}_LT_Raw_{}_{}_{}_{}_{}'.format(outputName,indexName,startYear,endYear,startJulian,endJulian)
  exportPath = exportPathRoot + '/'+ exportName
  # getImagesLib.exportToAssetWrapper(rawLTForExport,exportName,exportPath,{'.default':'sample'},studyArea,scale,crs,transform)
  # //Reverse for modeling
  decompressedC = changeDetectionLib.simpleLTFit(rawLTForExport,startYear,endYear,indexName,True,run_params['maxSegments'])
  Map.addLayer(decompressedC,{},'Decompressed LT Output {}'.format(indexName),False)

####################################################################################################
#Load the study region
Map.addLayer(studyArea, {'strokeColor': '0000FF'}, "Study Area", False)
Map.centerObject(studyArea)
####################################################################################################
####################################################################################################
# View map
Map.turnOnInspector()
Map.view()
####################################################################################################
####################################################################################################
# If exporting LT stack, track the exports
if exportLTStack:taskManagerLib.trackTasks2()
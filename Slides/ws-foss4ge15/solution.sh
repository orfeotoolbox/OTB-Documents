#!/bin/bash

export WSROOTDIR=/tmp/FOSS4G
export RAWDATADIR=${WSROOTDIR}/raw_data/
export INPUTIMAGEDIR=${RAWDATADIR}/spot4t5/SPOT4_HRVIR1_XS_20130607_N2A_CArdecheD0000B0000
export INPUTIMAGE=SPOT4_HRVIR1_XS_20130607_N2A_ORTHO_SURF_CORR_PENTE_CArdecheD0000B0000.TIF
export WORKINGDIR=${WSROOTDIR}/results

# Create directories
mkdir -p ${RAWDATADIR}
mkdir -p ${WORKINGDIR}
# Get the data
wget -O ${WSROOTDIR}/raw_data.tar.gz https://www.orfeo-toolbox.org/packages/ws-foss4ge2015/raw_data.tar.gz
tar -x -z -C ${WSROOTDIR} -f ${WSROOTDIR}/raw_data.tar.gz

# Extract red band
otbcli_BandMath -il ${INPUTIMAGEDIR}/${INPUTIMAGE} -out ${WORKINGDIR}/red.tif int16 -exp "im1b2"

# Extract green band
otbcli_BandMath -il ${INPUTIMAGEDIR}/${INPUTIMAGE} -out ${WORKINGDIR}/green.tif int16 -exp "im1b1"

# Compute synthetic blue band
otbcli_BandMath -il ${INPUTIMAGEDIR}/${INPUTIMAGE} -out ${WORKINGDIR}/blue.tif int16 -exp "im1b1==-10000?-10000:0.7*im1b1+0.24*im1b2-0.14*im1b3"

# Concatenate all bands for visualization
export RGBIMAGE=SPOT4_HRVIR1_XS_20130607_rgb.tif
otbcli_ConcatenateImages -il ${WORKINGDIR}/red.tif ${WORKINGDIR}/green.tif ${WORKINGDIR}/blue.tif -out ${WORKINGDIR}/${RGBIMAGE} int16

# Compute radiometric indices
otbcli_BandMath -il ${INPUTIMAGEDIR}/${INPUTIMAGE} -out ${WORKINGDIR}/ndvi.tif int16 -exp "im1b1==-10000?-10000:(im1b3-im1b2)/(im1b3+im1b2)*1000"
otbcli_BandMath -il ${INPUTIMAGEDIR}/${INPUTIMAGE} -out ${WORKINGDIR}/ndwi.tif int16 -exp "im1b1==-10000?-10000:(im1b3-im1b4)/(im1b3+im1b4)*1000"

# Concatenate image and indices
otbcli_ConcatenateImages -il ${INPUTIMAGEDIR}/${INPUTIMAGE} ${WORKINGDIR}/ndvi.tif ${WORKINGDIR}/ndwi.tif -out ${WORKINGDIR}/im4classif.tif



# Extract geometries
## Extract image enveloppe
otbcli_ImageEnvelope -in ${WORKINGDIR}/${RGBIMAGE} -proj "EPSG:32631" -out ${WORKINGDIR}/env.shp

## Clipping, reprojecting and merging land use layers:
ogr2ogr -append -t_srs ${RAWDATADIR}/l93.wkt -clipsrc ${WORKINGDIR}/env.shp ${WORKINGDIR}/landuse_l93.shp ${RAWDATADIR}/osm/auvergne/landuse.shp
ogr2ogr -append -t_srs ${RAWDATADIR}/l93.wkt -clipsrc ${WORKINGDIR}/env.shp ${WORKINGDIR}/landuse_l93.shp ${RAWDATADIR}/osm/rhone-alpes/landuse.shp

## Clipping, reprojecting and merging natural layers:
ogr2ogr -append -t_srs ${RAWDATADIR}/l93.wkt -clipsrc ${WORKINGDIR}/env.shp ${WORKINGDIR}/natural_l93.shp ${RAWDATADIR}/osm/auvergne/natural.shp
ogr2ogr -append -t_srs ${RAWDATADIR}/l93.wkt -clipsrc ${WORKINGDIR}/env.shp ${WORKINGDIR}/natural_l93.shp ${RAWDATADIR}/osm/rhone-alpes/natural.shp

## Clipping, reprojecting and merging waterways layers:
ogr2ogr -append -t_srs ${RAWDATADIR}/l93.wkt -clipsrc ${WORKINGDIR}/env.shp ${WORKINGDIR}/waterways_l93.shp ${RAWDATADIR}/osm/auvergne/waterways.shp
ogr2ogr -append -t_srs ${RAWDATADIR}/l93.wkt -clipsrc ${WORKINGDIR}/env.shp ${WORKINGDIR}/waterways_l93.shp ${RAWDATADIR}/osm/rhone-alpes/waterways.shp

# Build the reference data set with consistent classes
## Extract the two large rivers covering the image:
ogr2ogr -append -sql "select * from waterways_l93 where name in (\"La Loire\", \"Le Rhone\")" ${WORKINGDIR}/large_rivers.shp ${WORKINGDIR}/waterways_l93.shp

## In Qgis, use the \textit{vector/geoprocessing/buffer} tool to build a 25m buffer around, and save it to \texttt{water.shp}.
echo "In Qgis, use the vector/geoprocessing/buffer tool to build a 25m buffer around, and save it to water.shp"
echo "Press a key when done"
read -n 1 -s

## Append selected features from land use layer:
ogr2ogr -append -sql "select * from landuse_l93 where type in (\"basin\",\"pond\",\"reservoir\",\"salt_pond\",\"water\") and OGR_GEOM_AREA > 10000" ${WORKINGDIR}/water.shp ${WORKINGDIR}/landuse_l93.shp

## Append selected features from natural layer:
ogr2ogr -append -sql "select * from natural_l93 where type in (\"water\") and OGR_GEOM_AREA > 1000" ${WORKINGDIR}/water.shp ${WORKINGDIR}/natural_l93.shp

## Extract selected features from natural layer:
ogr2ogr -append -sql "select * from natural_l93 where type in (\"forest\")" ${WORKINGDIR}/forest.shp ${WORKINGDIR}/natural_l93.shp

## Extract selected features from land use layer:
ogr2ogr -append -sql "select * from landuse_l93 where type in (\"residential\",\"commercial\",\"cemetery\",\"construction\", \"industrial\", \"recreational\",\"harbour\", \"allotments\",\"brownfield\")" ${WORKINGDIR}/builtup.shp ${WORKINGDIR}/landuse_l93.shp

# Add class label, exclude overlaps in QGis (see slides)
echo "Add class label, exclude overlaps in QGis (see slides)"
read -n 1 -s

# Build separate sets for training (250 polygons of each class) and validation (the remaining)
ogr2ogr -append -dialect SQLITE -sql "select * from forest order by osm_id limit 250" ${WORKINGDIR}/training.shp ${WORKINGDIR}/forest.shp
ogr2ogr -append -dialect SQLITE -sql "select * from water order by osm_id limit 250" ${WORKINGDIR}/training.shp ${WORKINGDIR}/water.shp
ogr2ogr -append -dialect SQLITE -sql "select * from builtup order by osm_id limit 250" ${WORKINGDIR}/training.shp ${WORKINGDIR}/builtup.shp
ogr2ogr -append -dialect SQLITE -sql "select * from forest order by osm_id limit 250,1000000" ${WORKINGDIR}/validation.shp ${WORKINGDIR}/forest.shp
ogr2ogr -append -dialect SQLITE -sql "select * from water order by osm_id limit 250,1000000" ${WORKINGDIR}/validation.shp ${WORKINGDIR}/water.shp
ogr2ogr -append -dialect SQLITE -sql "select * from builtup order by osm_id limit 250,100000" ${WORKINGDIR}/validation.shp ${WORKINGDIR}/builtup.shp

# Merge everything in a single layer
ogr2ogr -append ${WORKINGDIR}/all.shp ${WORKINGDIR}/water.shp
ogr2ogr -append ${WORKINGDIR}/all.shp ${WORKINGDIR}/forest.shp
ogr2ogr -append ${WORKINGDIR}/all.shp ${WORKINGDIR}/builtup.shp

# Image Classification

## Estimation of image statistics
otbcli_ComputeImagesStatistics -il ${WORKINGDIR}/im4classif.tif -out ${WORKINGDIR}/stats.xml -bv -10000

## Training the classification algorithm
otbcli_TrainImagesClassifier -io.il ${WORKINGDIR}/im4classif.tif -io.vd ${WORKINGDIR}/training.shp -io.out ${WORKINGDIR}/model.svm -classifier libsvm -classifier.libsvm.k rbf -sample.mt 1000  -sample.mv 2000 -sample.vfn "class" -io.imstat ${WORKINGDIR}/stats.xml

## Classifying the image
otbcli_BandMath -il ${WORKINGDIR}/im4classif.tif -out ${WORKINGDIR}/mask.tif uint8 -exp "im1b1>-10000?255:0"
otbcli_ImageClassifier -in ${WORKINGDIR}/im4classif.tif -mask ${WORKINGDIR}/mask.tif -model ${WORKINGDIR}/model.svm -imstat ${WORKINGDIR}/stats.xml -out ${WORKINGDIR}/classif.tif uint8

## Classification noise cleaning
otbcli_ClassificationMapRegularization -io.in ${WORKINGDIR}/classif.tif -io.out ${WORKINGDIR}/classif_reg.tif -ip.radius 2

## Accuracy assesment
otbcli_ComputeConfusionMatrix -in ${WORKINGDIR}/classif_reg.tif -ref vector -ref.vector.in ${WORKINGDIR}/validation.shp -ref.vector.field "class" -nodatalabel 0 -out ${WORKINGDIR}/conf.txt

# Where do OSM and Land Cover differ?

## Rasterize our layer
otbcli_Rasterization -in ${WORKINGDIR}/all.shp -out ${WORKINGDIR}/all.tif -im ${WORKINGDIR}/im4classif.tif -mode attribute -mode.attribute.field "class" -background 0

## Compute the difference map
otbcli_BandMath -il ${WORKINGDIR}/classif_reg.tif ${WORKINGDIR}/all.tif -out ${WORKINGDIR}/errors.tif -exp "im2b1>0?(im1b1!=im2b1?im1b1:0):0"

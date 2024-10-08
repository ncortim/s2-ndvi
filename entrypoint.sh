#!/bin/bash

#exit on error
set -e

WORKER_DIR="/home/worker"

# get env variables
echo "### get env variables wps-properties ###"
WPS_PROPS="${WORKER_DIR}/processor/wps-properties"
source ${WPS_PROPS}

#create a sub directory in outdir to store processed data
echo "### create output directory ###"
mkdir -p /home/worker/workDir/outDir/ndvi_output

#get sentinel 2 scene basename
BASENAME=$(ls ${S2_INPUT}/GRANULE)
DATE=${BASENAME:19:16}
TILE=${BASENAME:5:5}
NEW_BASENAME=NDVI_S2_L2A_"${TILE}"_"${DATE}"

#execute s2 ndvi calculator.py
echo "### Launching s2-2a-10m-ndvi.py ###"
time python3 /home/worker/processor/s2-2a-10m-ndvi.py ${S2_INPUT} ${NDVI_OUTPUT} ${NEW_BASENAME}


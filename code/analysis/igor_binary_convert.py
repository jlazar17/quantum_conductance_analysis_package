#! /usr/bin/python

import os
import argparse



parser=argparse.ArgumentParser()
parser.add_argument('-f', nargs='+',required=True,\
	help='[required] input files')
parser.add_argument('-d', required=True,\
    help='[required] Specify the date the data was taken on in the form \
     mm-dd-yyyy. This is used to generate the directory in which plots will be \
    saved')
args = vars(parser.parse_args())

def checkPathExists(path):
	if not os.path.exists(path):
		os.makedirs(path)

def makePath(date,fileType):
    if fileType=='txt':
        path='./data/qc_data_'+date+'/text_files/'
    if fileType=='ibw':
        path='./data/qc_data_'+date+'/binary_files/'
    checkPathExists(path)
    return path

def findFileName(binaryFile):
    _=binaryFile[:-3]
    fileName=_+'txt'
    return fileName

def makeTextFile(binaryFile,txtPath,ibwPath):
    fileName=findFileName(binaryFile)
    filePath=txtPath+fileName
    os.system('igorbinarywave.py -f '+binaryFile+' -o '+filePath)
    os.system('mv '+binaryFile+' '+ibwPath)

def main(binaryFileArray,date):
    ibwPath=makePath(date,'ibw')
    txtPath=makePath(date,'txt')
    for i in binaryFileArray:
        makeTextFile(i,txtPath,ibwPath)
	print('Done!')

main(args['f'],args['d'])

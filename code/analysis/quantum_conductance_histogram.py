#! /usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import lorentzian as lz

# the number of lines in the output file containing data to be used in the 
# histogram is 10000
NUM_LINES = 10000
ENTRIES_PER_LINE = 100

parser = argparse.ArgumentParser()
parser.add_argument('-f', help='specify infile paths. more than one infile can\
	be specified', nargs='+')
parser.add_argument('-l', help='Specify a lower bound for the histogram. By \
	default it is 0.5', type=float, default=0.5)
parser.add_argument('-u', help='specify a lower bound for the histogram. By \
	default it is 3', type=float, default = 3)
parser.add_argument('-d', required=True,\
    help='[required] Specify the date the data was taken on in the form \
     mm-dd-yyyy. This is used to generate the directory in which plots will be \
    saved')
# returns a dictionary whose keys are the letters corresponding to command\
# line flags 
args = vars(parser.parse_args())

def makePath(date):
	path='./data/qc_data_'+date+'/plots/'
	if not os.path.exists(path):
		os.makedirs(path)
	return path

################################################################################
############################### IMPORTING DATA #################################

def makeDataArray(infile_array):
	dataArray = np.zeros(len(infile_array)*NUM_LINES*ENTRIES_PER_LINE)
	for file in infile_array:
		n=infile_array.index(file)
		with open(file) as f:
			lines = [line.rstrip('\n').split('\t') for line in f]
			for i in range(NUM_LINES):
				for j in range(ENTRIES_PER_LINE):
					dataArray[1000000*n+i*ENTRIES_PER_LINE+j] = lines[i][j]
	return dataArray

def makeHist(y,path):
	n, bins, patches=plt.hist(y, 1000, edgecolor = "none", color='black')
	bigCount,modeBinMiddle=findModeBinsMiddles(n,bins, .7)
	lb=modeBinMiddle-.25
	ub=modeBinMiddle+.25
	lorentzian,p,FWHM=lz.main((1,modeBinMiddle,bigCount),bins[:-1],n,lb,ub)
	T=p[1]
	plt.axvline(x=T, color='red')
	plt.plot(bins[:-1],lorentzian, 'r')
	plt.ylabel('Counts')
	plt.xlabel('Conductance (G0)')
	plt.title('Histogram of measured conductance, truncated from '
			 +str(args['l'])+' to '+str(args['u']))
	modestr='T='+str(T)[:6]+', FWHM='+str(FWHM)[:6]
	plt.text(.6*np.amax(bins), .95*bigCount,modestr,fontsize=14)
	plt.savefig(path+'conductance_histogram.png')

# Takes two arrays of m and m+1 element corresponding to the counts, and bin
# bin edges respectively, and an integer specifying how many bins middles to
# return. I.e. for the biggest bin middle n=1. It also ignores bins whose
# conductance value is greater than the lower bound since values close to 0
# tend to have many counts
def findModeBinsMiddles(counts, binEdges,lowerBound):
	largestCount=int(np.amax(counts))
	binEdgeIndex=np.where(counts==largestCount)[0][0]
	binMiddle=(binEdges[binEdgeIndex]+binEdges[binEdgeIndex+1])/2.0
	return largestCount,binMiddle

def boundData(min, max, dataArray):
	goodDataArray = [i for i in dataArray if (i<max and i>min)]
	return goodDataArray

def main(infileArray,date):
	path=makePath(date)
	min,max = args['l'],args['u']
	dataArray = makeDataArray(infileArray)
	dataArray = boundData(min, max, dataArray)
	makeHist(dataArray,path)
	print('Done!')

if __name__ == '__main__':
    main(args['f'],args['d'])

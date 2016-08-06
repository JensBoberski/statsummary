#!/usr/bin/env python
# coding: utf-8

import sys
import argparse
import numpy
from scipy import stats

def main(fileList):
	for file in fileList:
		calcAndPrintStats(file)
	pass

def calcAndPrintStats(file):
	printInputName(file)
	inputData = loadFileToNumpy(file)
	printShape(inputData)
	labels, statistics = calculateStats(inputData)
	printNumpyArrayTransposed(labels, statistics)


# round a number x to multiples of digit with precission maxPrec
def myRound(x,digit,maxPrec = 16):
	return round(digit * round(x/digit),maxPrec)

# make the round function available for numpy arrays
myNpRound = numpy.vectorize(myRound)

#round every column of a numpy array by different value in roundArray
def roundNumpy(ndArray,roundArray):
	transposedArray = ndArray.transpose()
	if len(transposedArray.shape) !=1:
		return numpy.array([myNpRound(row,digit) for row,digit in zip(transposedArray,roundArray)]).transpose()
	else:
		return myNpRound(ndArray,roundArray)


# takes numpy array with columns of data and returns stats summaries of each line
# as [labels,numpy.array([summaries])]
def calculateStats(data):
	mean = numpy.mean(data,axis=0)
	std = numpy.std(data,axis=0)
	q75, median, q25 = numpy.percentile(data, [75,50,25],axis=0)
	iqr = q75 - q25
	min = numpy.min(data,axis=0)
	max = numpy.max(data,axis=0)

	skew = stats.skew(data,axis=0)
	kur = stats.kurtosis(data,axis=0)
	# approximate the mode by using bins (rounding) of the size IQR/10
	mode = stats.mode(roundNumpy(data,iqr/10))[0][0]
	
	return [["mean","std","skew","ex.kur","~mode","min","25%","50%","75%","max"],numpy.array([mean,std,skew,kur,mode,min,q25,median,q75,max])]
	

# returns input string if not sts.stdin
def printInputName(fileName):
	if fileName is sys.stdin:
		print "<STDIN>",
	else:
		print fileName,


def printShape(ndArray):
	print ndArray.shape[0],"rows",
	try:
		print ndArray.shape[1],"columns"
	except:
		print ""


# wrapper for numpy text import to throw error
def loadFileToNumpy(fileName):
	try:
		inputData = numpy.genfromtxt(fileName)
	except:
		print "Error while laoding "+fileName
		exit(1)
	return inputData


# takes labels and stat values (numpy array) and prints it nicely 
def printNumpyArrayTransposed(labels, numpyArray):
	transposedNumpyArray = numpy.transpose(numpyArray)
	
	if len(transposedNumpyArray.shape) == 1:
		transposedNumpyArray = [transposedNumpyArray]
		
	print "column".ljust(8),
	for label in labels:
		print label.rjust(12),
	print ""
	
	for i in range(len(transposedNumpyArray)):
		print str(i+1).ljust(8),
		for value in transposedNumpyArray[i]:
			print str("%0.5f" % value).rjust(12),
		print ""


if __name__=="__main__":
	parser = argparse.ArgumentParser(description='Creates statistice of ech column of the input data. The input can eiter be a list of files or will be read from stdin.')
	parser.add_argument('files', nargs='*', default=[sys.stdin], help="Files that should be analyzed. [Default: stdin]")

	args = parser.parse_args()
	
	main(args.files)

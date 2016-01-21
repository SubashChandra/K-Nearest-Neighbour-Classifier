#!/usr/bin/python

import sys
import operator
import math
import random 

if len(sys.argv)!=3:
	print "invalid no of args"
	sys.exit()

myData=[]
fh=open(sys.argv[1],'r')
kVal=int(sys.argv[2]) #k value for kth nearest neighbour

for i in fh:
	if len(i)!=1:
		i=i.strip()
		row=i.split(',')
		myData.append(row)

accuList=[] #accuracy list
	
for count in range(10):
	random.shuffle(myData)

	#assuming class will always be at the end	
	#get the no of features ie dimension
	dim=len(myData[0])-1
	#print dim

	#find the no of distinct classes in the dataset
	classList=[]
	for i in myData:
		if i[dim] not in classList:
			classList.append(i[dim])

	classCount=len(classList)

					
	#for the confusion matrix
	#class list to integers from 0 to classCount-1
	classMap={}
	count=0
	for i in classList:
		classMap[i]=count
		count=count+1

	#now create a matrix of dimension classCount * classCount filled with zeros
	temprow=[]
	for i in range(classCount):
		temprow.append(0)
	
	confusionMatrix=[]
	for i in range(classCount):
		confusionMatrix.append(temprow)


	trainSet=[]
	testSet=[]

	size=len(myData)
	#print size

	i=0
	while i<size/2:
		trainSet.append(myData[i])
		i=i+1

	while i<size:
		testSet.append(myData[i])
		i=i+1

	#print len(trainSet)
	#print len(testSet)

	#iterate over the testData nd use k to test get accuracy

	matchCount=0
	for row1 in testSet:
		dList=[]
		for row2 in trainSet:
			temp=[]
			dist=0
			for k in range(dim):
				dist=dist+math.pow((float(row1[k])-float(row2[k])),2)
			dist=math.sqrt(dist)
			temp.append(dist)
			temp.append(row2[dim]) #append class to list
			dList.append(temp)
		dList=sorted(dList)
#		for i in dList:
#			print i

		myDict={}
		for i in range(kVal):
			key=dList[i][1]
			if key not in myDict:
				myDict[key]=1
			else:
				myDict[key]=myDict[key]+1
		
		#now sort the dictionary based on the value (descending)
		myDict=sorted(myDict.items(),key=operator.itemgetter(1),reverse=True)
	#	print "\n***************"
	#	for i in myDict:
	#		print i[0],i[1]

		#randomly assign a class,  assign class at zeroth key
		
		actual=row1[dim]
		prediction=myDict[0][0]

#		print classMap		
#		print actual,prediction
		if len(myDict)==dim: #if all r discrete, assign the one at the top of the dict as the predicted class
			if actual==prediction:
				matchCount=matchCount+1
		else:
			if actual==prediction:
				matchCount=matchCount+1

		actIndex=classMap[actual]
		predIndex=classMap[prediction]
		#update confusion matrix
		confusionMatrix[actIndex][predIndex]=confusionMatrix[actIndex][predIndex]+1
		
	accuracy=(float(matchCount)/(float(size)/2.0))*100
	print accuracy
	for i in confusionMatrix:
		print i
	accuList.append(accuracy)

	#reset the confusion matrix
	for i in range(classCount):
		for j in range(classCount):
			confusionMatrix[i][j]=0

#calculate mean
sum=0.0
for i in  accuList:
	sum=sum+i
mean=sum/10.0
print "Mean: ",
print mean

#calculate standard deviation
temp=0.0
for i in accuList:
	temp=temp+math.pow(mean-i,2)
sd=math.sqrt(temp)
print "Standard Deviation: ",
print sd

print "\n******* Confusin Matrix *******"
print classCount


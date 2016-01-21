#!/usr/bin/python

import sys
import operator
import math
import random 

if len(sys.argv)!=4:
	print "invalid no of args"
	sys.exit()

myData=[]
fh=open(sys.argv[1],'r')
kVal=int(sys.argv[2]) #k value for kth nearest neighbour
classIndex=int(sys.argv[3])


for i in fh:
	if len(i)!=1:
		i=i.strip()
		row=i.split(',')
		myData.append(row)


classList=[]
for i in myData:
	if i[classIndex] not in classList:
		classList.append(i[classIndex])


print "ClassList: "
print classList


meanList=[] #mean list
print "\n###  5-Fold Cross Validation  ###"

for count in range(10):
	random.shuffle(myData)
	
	accuracyList=[]
	for fold in range(5):
		trainSet=[]
		testSet=[]

		size=len(myData)
		dim=len(myData[0])
		#print size

		i=0
		while i<size:
			if i%5==fold:
				testSet.append(myData[i])
			else:
				trainSet.append(myData[i])
			i=i+1

		#print len(trainSet)
		#print len(testSet)

		#iterate over the testData nd use k to test get accuracy
		#print len(trainSet)
		#print len(testSet)
		matchCount=0
		for row1 in testSet:
			dList=[]
			for row2 in trainSet:
				temp=[]
				dist=0
				for k in range(dim):
					if ((sys.argv[1]!='breast-cancer-wisconsin.data' and k!=classIndex) or (sys.argv[1]=='breast-cancer-wisconsin.data' and k!=classIndex and  k!=0)):
						if k==0:
							print row1[k],row2[k]
						val1=row1[k]
						val2=row2[k]

						#handle unavailability in cancer.data, give average
						if val1=='?':
							val1=5
						if val2=='?':
							val2=5

						dist=dist+math.pow((float(val1)-float(val2)),2)
				dist=math.sqrt(dist)
				temp.append(dist)
				temp.append(row2[classIndex]) #append class to list
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
			
			actual=row1[classIndex]
			prediction=myDict[0][0]

	#		print classMap		
	#		print actual,prediction
			if len(myDict)==dim: #if all r discrete, assign the one at the top of the dict as the predicted class
				if actual==prediction:
					matchCount=matchCount+1
			else:
				if actual==prediction:
					matchCount=matchCount+1
			

		accuracy=(float(matchCount)/(float(size)/5.0))*100
		accuracyList.append(accuracy)

	sum=0.0
	for i in accuracyList:
		sum=sum+i
	foldMean=(sum/5.0)
	meanList.append(foldMean)


	#standard deviation of the current fold
	row="Test Run #"+str(count+1)
	temp=0.0
	for i in accuracyList:
		temp=temp+math.pow(foldMean-i,2)
	foldDev=math.sqrt(temp/5.0)
	row=row+"	" + "Mean: "+str(foldMean)+ "	"
	row=row+ "Standard Deviation: "+str(foldDev)+"\n"
	print row

tempSum=0.0
for i in meanList:
	tempSum=tempSum+i
print "Grand Mean: "+str(tempSum/10.0)





print "\n###   Random Subsampling Approach  ###"
accuList=[]
for count in range(10):
	random.shuffle(myData)

	trainSet=[]
	testSet=[]

	size=len(myData)
	dim=len(myData[0])
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
	#confusion Matrix
	cMatrix={}


	matchCount=0
	for row1 in testSet:
		dList=[]
		for row2 in trainSet:
			temp=[]
			dist=0
			for k in range(dim):
				if ((sys.argv[1]!='breast-cancer-wisconsin.data' and k!=classIndex) or (sys.argv[1]=='breast-cancer-wisconsin.data' and k!=classIndex and  k!=0)):
					val1=row1[k]
					val2=row2[k]

					#handle unavailability in cancer.data, give average
					if val1=='?':
						val1=5
					if val2=='?':
						val2=5

					dist=dist+math.pow((float(val1)-float(val2)),2)
			dist=math.sqrt(dist)
			temp.append(dist)
			temp.append(row2[classIndex]) #append class to list
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
		
		actual=row1[classIndex]
		prediction=myDict[0][0]

#		print classMap		
#		print actual,prediction
		if len(myDict)==dim: #if all r discrete, assign the one at the top of the dict as the predicted class
			if actual==prediction:
				matchCount=matchCount+1
		else:
			if actual==prediction:
				matchCount=matchCount+1
		
		#update confusion matrix
		if actual in cMatrix:
			if prediction in cMatrix[actual]:
				cMatrix[actual][prediction]=cMatrix[actual][prediction]+1
			else:
				cMatrix[actual][prediction]=1
		else:
			cMatrix[actual]={}
			cMatrix[actual][prediction]=1



	accuracy=(float(matchCount)/(float(size)/2.0))*100
	print '*****************'
	print "Test Run: "+str(count+1)

	print 'Accuracy: ',accuracy
	accuList.append(accuracy)

#	print cMatrix
	#print dictionary
	print "\nConfusion Matrix"
	
	header=""
	for i in classList:
		header+="\t\t"+i

	print header
	for i in classList:
		col=cMatrix[i]
		row=i
		for j in classList:
			if col.has_key(j):
				row+="\t\t"+str(col[j])
			else:
				row+="\t\t"+"0"
		
		print row
	print '*****************\n'

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
sd=math.sqrt(temp/10)
print "Standard Deviation: ",
print sd



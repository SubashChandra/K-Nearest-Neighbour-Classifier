#!/usr/bin/python

import math
import sys
import matplotlib.pyplot as plt
import numpy as np

fh=open('iris.data','r')

myData=[]
for i in fh:
	if len(i)!=1:
		i=i.strip()
		row=i.split(',')
		myData.append(row)

trainData={}
for row in myData:
	key=(float(row[1]),float(row[3]))
	trainData[key]=row[4]


setx=[]
sety=[]
virx=[]
viry=[]
verx=[]
very=[]

for row in myData:
	if row[4]=='Iris-setosa':
		setx.append(row[1])
		sety.append(row[3])
	elif row[4]=='Iris-versicolor':
		verx.append(row[1])
		very.append(row[3])
	elif row[4]=='Iris-virginica':
		virx.append(row[1])
		viry.append(row[3])
		
prec = 0.02
xCord=np.arange(0,5.1,prec)
yCord=np.arange(0,3.1,prec)

testData={}
for i in xCord:
	for j in yCord:
		newi=float('%.2f' %(i))
		newj=float('%.2f' %(j))
		testData[(newi,newj)]='?'


for row1 in testData.keys():
	minDist=10000
	tClass=''
	for row2 in trainData.keys():
		dist=math.pow((row2[0]-row1[0]),2)+math.pow((row2[1]-row1[1]),2)
		dist=math.sqrt(dist)
		if dist<minDist:
			minDist=dist
			tClass=trainData[row2]
	testData[row1]=tClass


setosax=[]
setosay=[]
virginicax=[]
virginicay=[]
versix=[]
versiy=[]

for row in testData.keys():
	if testData[row]=='Iris-setosa':
		setosax.append(row[0])
		setosay.append(row[1])
	elif testData[row]=='Iris-versicolor':
		versix.append(row[0])
		versiy.append(row[1])
	elif testData[row]=='Iris-virginica':
		virginicax.append(row[0])
		virginicay.append(row[1])
		
line1=[]
for x in np.arange(0,5,prec):
	for y in np.arange(3,0,-prec):
		newx=float('%.2f' %(x))
		newy=float('%.2f' %(y))
		if testData[(newx,newy)]!=testData[(newx,float('%.2f' %(newy-prec)))]:
			line1.append((newx,newy))
			break

line1x=[]
line1y=[]
for i in line1:
	line1x.append(i[0])
	line1y.append(i[1])

line2=[]
for x in np.arange(0.8,5,prec):
	for y in np.arange(0,2.9,prec):
		newx=float('%.2f' %(x))
		newy=float('%.2f' %(y))
		if testData[(newx,newy)]!=testData[(newx,float('%.2f' %(newy+prec)))]:
			line2.append((newx,float('%.2f' %(newy+prec))))
			break

line2x=[]
line2y=[]
for i in line2:
	line2x.append(i[0])
	line2y.append(i[1])


plt.plot(setx,sety,'go',label='Iris-setosa')
plt.plot(verx,very,'bo',label='Iris-versicolor')
plt.plot(virx,viry,'ro',label='Iris-virginica')
plt.axis([0,5,0,3])
plt.plot(line1x,line1y,'black')
plt.plot(line2x,line2y,'black')
plt.legend(loc=2)
plt.show()


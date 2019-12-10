# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 23:04:32 2019

@author: Blaž
"""

""" 
Traveling salesman problem
"""
# imports
import random
import math
import datetime
import sys
import matplotlib.pyplot as plt
import copy
#import numpy as np

# class for a point
class Point:
    def __init__ (self, _xPos, _yPos):
        self.xPos = _xPos
        self.yPos = _yPos
        self.posNumeric = [_xPos, _yPos]
    # Generates distances from point to every anchor
    def generateAnchorDistances (self, _anchorPositions):
        self.anchorDistances = [None] * 9
        for i in range (9):
            tempDistance = calculateDistanceBetwenTwoPoints(self, _anchorPositions[i])
            self.anchorDistances[i] = tempDistance
        
        # check and saves in witch quadrant this point is
        self.quadrant = self.anchorDistances.index(min(self.anchorDistances))
    
        
# Generates anchor positions
    # returns array of points
def generateAnchorPositions (_xMinMax, _yMinMax):
    anchorPositions = [None] * 9
    
    xStart = _xMinMax[0]
    xEnd = _xMinMax[1]
    xMiddle = (xStart + xEnd) /2
    
    yStart = _yMinMax[0]
    yEnd = _yMinMax[1]
    yMiddle = (yStart + yEnd) /2
    
    anchorPositions[0] = Point(xMiddle, yMiddle)
    anchorPositions[1] = Point(xStart, yStart)
    anchorPositions[2] = Point(xMiddle, yStart)
    anchorPositions[3] = Point(xEnd, yStart)
    anchorPositions[4] = Point(xEnd, yMiddle)
    anchorPositions[5] = Point(xEnd, yEnd)
    anchorPositions[6] = Point(xMiddle, yEnd)
    anchorPositions[7] = Point(xStart, yEnd)
    anchorPositions[8] = Point(xStart, yMiddle)
    
    return anchorPositions
    
# generating random points
def generateRandomPoints(_number_of_points, _grid_size):
    
    allowed_fails = 20
    counter_failedLoopInARow = 0
    
    pointsArray = []
    takenPositions = []
    
    while (len(pointsArray) < _number_of_points):
        xCoor = random.uniform(0, _grid_size)
        yCoor = random.uniform(0, _grid_size)
        coorArray = [xCoor, yCoor]
        
        # if position already exists increse counter
            # if counter is to big, break and print a message
            # in case we choose a lot of points and small grid ... 
            # a bit useless now that point positions are not intiger numbers anymore
        if (coorArray in takenPositions):
            counter_failedLoopInARow += 1
            if (counter_failedLoopInARow > allowed_fails):
                print ("\nGenerating points warrning!" + 
                       "\n Couldn generate enough points." +
                       "\n Maybe grid size is not big enough.\n")
                break
            continue
        
        counter_failedLoopInARow = 0
        
        takenPositions.append(coorArray)
        newPoint = Point(xCoor, yCoor)
        pointsArray.append(newPoint)
    
    # Adding the first number to create a circle
    pointsArray.append(copy.deepcopy(pointsArray[0]))
    
    return pointsArray

# if we want to use custom point array (mainly for testing)
def generateCustomePoints():
    
    
    
    inputArray = [[6734, 1453],[7265, 1268],[6898, 1885],[7392, 2244],
                  [7545, 2801],[7509, 3239],[7462, 3590],[7573, 3716],
                  [7541, 3981],[7248, 3779],[6807, 2993],[6347, 2683],
                  [6271, 2135],[6101, 1110],[6107, 669],[5530, 1424],
                  [5199, 2182],[5468, 2606],[5989, 2873],[6426, 3173],
                  [5900, 3561],[5185, 3258],[4706, 2674],[3082, 1644],
                  [1916, 1569],[675, 1006],[401, 841],[23, 2216],[10, 2676],
                  [1112, 2049],[1633, 2809],[2233, 10],[3177, 756],
                  [3023, 1942],[3484, 2829],[3245, 3305],[4307, 2322],
                  [4612, 2035],[4608, 1198],[4985, 140],[4483, 3369],
                  [7352, 4506],[7608, 4458],[7762, 4595],[7732, 4723],
                  [7555, 4819],[7280, 4899],[7611, 5184],[6734, 1453]]
    
    
    
#    txtFile  = open("pointsData.txt", "r")
#    inputArray = []
#    for line in txtFile:
#        a = line.strip().split(", ")
#        a[0] = float(a[0][1:])
#        a[1] = float(a[1][:-1])
#        inputArray.append(a)
#    txtFile.close()
        

    pointArray = []
    
    for inputPoint in inputArray:
        newPoint = Point(inputPoint[0], inputPoint[1])
        pointArray.append(newPoint)
    
    return pointArray


# returns a graph of conected points
def graphPlot(_pointsArray, _colorString, _lineWidth):
    xData = []
    yData = []
    
    for singPoint in _pointsArray:
        xData.append(singPoint.xPos)
        yData.append(singPoint.yPos)
    
    plt.plot(xData[0], yData[0], 'ro', markersize = 5)
    plt.plot(xData[1], yData[1], 'co', markersize = 5)
    
    
    
    plt.plot(xData, yData, _colorString + '--', linewidth = _lineWidth)
    plt.plot(xData, yData, 'go', markersize = 2)
    
#    plt.figure()
    plt.show()

# calculate distance between two given points
def calculateDistanceBetwenTwoPoints(_point1, _point2):
    x1 = _point1.xPos
    y1 = _point1.yPos
    x2 = _point2.xPos
    y2 = _point2.yPos
    
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    return distance

# calculate total travel distance
def calculateTotalTravelDistance(_pointsArray):
    totalDistance = 0
    
    for i in range (len(_pointsArray) -1):
        point1 = _pointsArray[i]
        point2 = _pointsArray[i + 1]

        totalDistance += calculateDistanceBetwenTwoPoints(point1, point2)

    return totalDistance

# look for and return anchor index with the minimal distance to the point
def getPointAnchorIndex(_point):
    anchorIndex = _point.anchorDistances.index(min(_point.anchorDistances))

    return anchorIndex

# calculate distance between anchor, point1 and point2
    # if no anchor parameter is given, it takes the anchor of the first point
def getTriangleDistance(_point1, _point2, _intAnchorPoint = 1, 
                        _anchorIndexSpecific = None):
    anchorIndex = -1
    if (_anchorIndexSpecific != None):
        anchorIndex = _anchorIndexSpecific
    elif (_intAnchorPoint == 1):
        anchorIndex = _point1.anchorDistances.index(min(_point1.anchorDistances))
    elif (_intAnchorPoint == 2):
        anchorIndex = _point2.anchorDistances.index(min(_point2.anchorDistances))
    else:
        print ("Function getTriangleDistance; Parameter Error!")
        return None

    distanceBeteenPoints = calculateDistanceBetwenTwoPoints(_point1, _point2)
    triangleDistance = ((distanceBeteenPoints**2 + 
                        _point1.anchorDistances[anchorIndex] +
                        _point2.anchorDistances[anchorIndex]))
    
    return triangleDistance

# moving an array element for one index to another
def moveElementInArray (_elementIndexOriginal, _elementIndexTarget, _array):
    element = _array[_elementIndexOriginal]
    _array.remove (element)
    _array.insert (_elementIndexTarget, element)
    
    return _array
    
# First (starting) sorting algoritm - the main one
def sortStartAlgoritem (_pointsArray):
    # array of points that are not sorted yet
    pointsRemaining = copy.deepcopy(_pointsArray)
    # first and last point
    firstPoint = pointsRemaining[0]
    lastPoint = pointsRemaining[len(pointsRemaining)-1]
    # removing first and last point
    pointsRemaining.remove(firstPoint)
    pointsRemaining.remove(lastPoint)
    
    # adding first point into our sorted array
    pointsArrayNew = [firstPoint]
    
    # sort loop
    while (len(pointsRemaining) > 0):
        pointLastInArray = pointsArrayNew[-1]
        anchorIndex = pointLastInArray.quadrant
        
        minTriangleDistance = sys.maxsize
        minTrianglePointIndex  = None
        
        for i in range(len(pointsRemaining)):
            point = pointsRemaining[i]
            pointDist = calculateDistanceBetwenTwoPoints(pointLastInArray, point)
            triangleDistance = (pointDist**2 + point.anchorDistances[anchorIndex] +
                                pointLastInArray.anchorDistances[anchorIndex])
            if (triangleDistance < minTriangleDistance):
                minTriangleDistance = triangleDistance
                minTrianglePointIndex = i
        
        pointsArrayNew.append(pointsRemaining[minTrianglePointIndex])
        pointToRemove = pointsRemaining[minTrianglePointIndex]
        pointsRemaining.remove(pointToRemove)
        
    pointsArrayNew.append(lastPoint)
    

    return pointsArrayNew

# first/start sort algorithm v2.0 - a bit random
def sortStartAlgoritem2 (_pointsArray):
    
    pointsArray = copy.deepcopy(_pointsArray)
    del (pointsArray[0])
    newPointsArray = []
    
    newPointsArray.append(copy.deepcopy(pointsArray[0]))
    del pointsArray[0]
        
    
    def calclulatePathIncrese (point1, point2, newPoint):
        originalDistance = calculateDistanceBetwenTwoPoints(point1, point2)
        newDistance = calculateDistanceBetwenTwoPoints(point1, newPoint) + calculateDistanceBetwenTwoPoints(newPoint, point2)
        
        pathIncreseDist = newDistance - originalDistance
        return pathIncreseDist
    
    
    while (len(pointsArray) > 0):
        index = random.randint(0, len(pointsArray) - 1)
        newPoint = pointsArray[index]
        
        minIncrese = [-1, -1]
        for i in range (len(newPointsArray)):
    
            point1 = newPointsArray[i]
    
            if (i == len(newPointsArray) - 1):
                point2 = newPointsArray[0]
            else:
                point2 = newPointsArray[i + 1]
    
            pathIncrese = calclulatePathIncrese(point1, point2, newPoint)
            
            if (minIncrese[0] == -1 or pathIncrese < minIncrese[0]):
                minIncrese = [pathIncrese, i]
        
        newPointsArray.insert(minIncrese[1] + 1, copy.deepcopy(newPoint))
        
        del (pointsArray[index])
        
    newPointsArray.append(copy.deepcopy(newPointsArray[0]))
    
    return newPointsArray
    


# tring to switch two next points 
def sortSwitchPrevPoint(_pointArray):

    for i in range (0, len(_pointArray) -2):
        point1 = _pointArray[i-1]
        point2 = _pointArray[i]
        point3 = _pointArray[i+1]
        point4 = _pointArray[i + 2]
        
        distance12 = (calculateDistanceBetwenTwoPoints(point1, point2) +
                      calculateDistanceBetwenTwoPoints(point3, point4))
        distance13 = (calculateDistanceBetwenTwoPoints(point1, point3) +
                      calculateDistanceBetwenTwoPoints(point2, point4))
        
        if (distance13 < distance12):
            _pointArray = moveElementInArray(i+1, i, _pointArray)
    
    # first and last point are a bit special
    point1 = _pointArray[1]
    point2 = _pointArray[0]
    point3 = _pointArray[len(_pointArray)-2]
    point4 = _pointArray[len(_pointArray)-3]
    
    distance1 = (calculateDistanceBetwenTwoPoints(point3, point4) +
                 calculateDistanceBetwenTwoPoints(point2, point1))
    distance2 = (calculateDistanceBetwenTwoPoints(point4, point2) +
                 calculateDistanceBetwenTwoPoints(point3, point1))
    
    if (distance2 < distance1):
        _pointArray = moveElementInArray(len(_pointArray) -2, 1, _pointArray)
    
    return (_pointArray)

# if 12345 is less optimal than 14325, then switch order of those points
def sortSwitchNextTwoPoints(_pointsArray):
    
    for i in range(0, len(_pointsArray)-4):
        point1 = _pointsArray[i]
        point2 = _pointsArray[i+1]
        point4 = _pointsArray[i+3]
        point5 = _pointsArray[i+4]
        
        distanceOriginal = (calculateDistanceBetwenTwoPoints(point1, point2) +
                            calculateDistanceBetwenTwoPoints(point4, point5))
        distanceChanged = (calculateDistanceBetwenTwoPoints(point1, point4) +
                           calculateDistanceBetwenTwoPoints(point2, point5))
        
        if (distanceChanged < distanceOriginal):
            indexPoint2 = i + 1
            indexPoint4 = i + 3
            _pointsArray.remove(point2)
            _pointsArray.remove(point4)
            _pointsArray.insert(indexPoint2, point4)
            _pointsArray.insert(indexPoint4, point2)
            
    return _pointsArray

# if 123456 is les optimal than 154326, then switch order of those points 
def sortSwitchNextThreePoints(_pointsArray):
    
    for i in range(0, len(_pointsArray)-5):
        point1 = _pointsArray[i]
        point2 = _pointsArray[i+1]
        point3 = _pointsArray[i+2]
        point4 = _pointsArray[i+3]
        point5 = _pointsArray[i+4]
        point6 = _pointsArray[i+5]
        
        distanceOriginal = (calculateDistanceBetwenTwoPoints(point1, point2) +
                            calculateDistanceBetwenTwoPoints(point5, point6))
        distanceChanged = (calculateDistanceBetwenTwoPoints(point1, point5) +
                           calculateDistanceBetwenTwoPoints(point2, point6))
        
        if (distanceChanged < distanceOriginal):
            indexPoint2 = i + 1
            
            _pointsArray.remove(point3)
            _pointsArray.remove(point4)
            _pointsArray.remove(point5)
            _pointsArray.insert(indexPoint2, point3)
            _pointsArray.insert(indexPoint2, point4)
            _pointsArray.insert(indexPoint2, point5)
            
        
    return _pointsArray


# second sort algoritm - trying to switch points between them self
def sortSwitchLoop (_pointsArray):
    newPointArray = copy.deepcopy(_pointsArray)
    totalDistanceCurrent = calculateTotalTravelDistance(_pointsArray)
    pointsArray = _pointsArray
    totalDistanceMinimal = totalDistanceCurrent
    pointsArrayWithMinimalDistance = []
    
    while True:
        pointsArray = sortSwitchPrevPoint(pointsArray)
        pointsArray = sortSwitchNextTwoPoints(pointsArray)
        pointsArray = sortSwitchNextThreePoints(pointsArray)
        totalDistnceCurrent = calculateTotalTravelDistance(pointsArray)
        if (totalDistnceCurrent < totalDistanceMinimal):
            totalDistanceMinimal = totalDistnceCurrent
            pointsArrayWithMinimalDistance = copy.deepcopy(pointsArray)
        else:
            break
    
    if (len(pointsArrayWithMinimalDistance) > 0):
        newPointArray = pointsArrayWithMinimalDistance


    return newPointArray

# find a point between points with max distance
def sortAlgoritmReduceMaxDistance(_pointsArray):
    maxDistance = 0
    indexMaxDistance = -1
    
    # look for max distance
    for i in range (1, len(_pointsArray)- 2):
        point1 = _pointsArray[i]
        point2 = _pointsArray[i + 1]
        
        distanceTwoPoint = calculateDistanceBetwenTwoPoints(point1, point2)
                            
        if (maxDistance < distanceTwoPoint):
            maxDistance = distanceTwoPoint
            indexMaxDistance = i
    
    # points with max distance between themself
    point1 = _pointsArray[indexMaxDistance]
    point2 = _pointsArray[indexMaxDistance + 1]
    pointPrev = _pointsArray[indexMaxDistance - 1]
    
    
    minTriangleDistance = sys.maxsize
    pointMinTrinagle = None
    
    distanceTriangleOriginal = getTriangleDistance(point1, point2, 2)
    
    for point in _pointsArray:
        if (point == point1 or point == point2 or point == pointPrev or 
            point == _pointsArray[len(_pointsArray)-1]):
            continue
        
        triangleDistance = getTriangleDistance(point1, point)
        triangleDistance2 = getTriangleDistance(point2, point)
                
        # se pravi če je razdalaja trikotnika manjsa za 2. točko kot v originalu
        # in če je najmanjša mozna do točke 1
        if (triangleDistance < minTriangleDistance and 
            triangleDistance2 < distanceTriangleOriginal):
            
            minTriangleDistance = triangleDistance
            pointMinTrinagle = point
    
    indexStartInsert = _pointsArray.index(pointMinTrinagle)
    direction = 0
    
    distDirBack = getTriangleDistance(point2, _pointsArray[indexStartInsert - 1])
    distDirForw = getTriangleDistance(point2, _pointsArray[indexStartInsert + 1])
    
    if (distDirForw < distDirBack):
        direction = 1
    else:
        direction = -1
    
    # points to be inserted
    pointsToInsert = [_pointsArray[indexStartInsert]]
    distPrevTriangle = getTriangleDistance(point2, _pointsArray[indexStartInsert])
    indexCurr = indexStartInsert
    while (True):
        indexCurr += direction
        if (indexCurr > len(_pointsArray) -2):
            indexCurr -= len(_pointsArray) - 1
        newPoint = _pointsArray[indexCurr]
        distNewTriangle = getTriangleDistance(point2, newPoint)

        if (distNewTriangle < distPrevTriangle):
            distPrevTriangle = distNewTriangle
            pointsToInsert.append(newPoint)
        else:
            distSecondTriangle = getTriangleDistance(point2, _pointsArray[indexCurr + direction])

            if (distSecondTriangle < distPrevTriangle):
                pointsToInsert.append(newPoint)
            else:
                break
    
    # popravimo index, če so točke za vstavljanje v arrayu pred točko za katero vstavljamo
    # correcting index, if needed
    if (indexStartInsert < indexMaxDistance):
        indexMaxDistance -= len(pointsToInsert) -1
    
    for point in pointsToInsert:
        _pointsArray.remove(point)
    
    for point in pointsToInsert:
        _pointsArray.insert(indexMaxDistance, point)
        indexMaxDistance += 1
    
    return _pointsArray

# third sorting algoritm - find a point between points with max distance
def sortLoopAlgoritmReduceMaxDistance(_pointsArray):
    totalDistMin = calculateTotalTravelDistance(_pointsArray)
    pointsArrayMinDist = copy.deepcopy(_pointsArray)
    
    failCounter = 0
    while (True):
        if (failCounter > 5):
            break
        
        _pointsArray = sortAlgoritmReduceMaxDistance(_pointsArray)
        _pointsArray = sortSwitchLoop(_pointsArray)
        
        totalNewDist = calculateTotalTravelDistance(_pointsArray)
        
        if (totalNewDist < totalDistMin):
            totalDistMin = totalNewDist
            pointsArrayMinDist = copy.deepcopy(_pointsArray)
        else:
            failCounter += 1
        
    return pointsArrayMinDist

# fourth sort algoritm - resolve intersections
def sortIntersections(_pointsArray):
    
    def doesLinesIntersect(line1, line2):
        x1 = line1[0][0]
        y1 = line1[0][1]
        x2 = line1[1][0]
        y2 = line1[1][1]
        x3 = line2[0][0]
        y3 = line2[0][1]
        x4 = line2[1][0]
        y4 = line2[1][1]
        
        xS = (x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4)
        d = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
        yS = (x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4)
        
        if (d == 0):
            return False
        ix= xS / d 
        iy= yS / d
        
        xSmaler = []
        ySmaler = []
        xBigger = []
        yBigger = []
        
        if (x1 < x2):
            xSmaler.append(x1)
            xBigger.append(x2)
        else:
            xSmaler.append(x2)
            xBigger.append(x1)
        if (x3 < x4):
            xSmaler.append(x3)
            xBigger.append(x4)
        else:
            xSmaler.append(x4)
            xBigger.append(x3)
            
        if (y1 < y2):
            ySmaler.append(y1)
            yBigger.append(y2)
        else:
            ySmaler.append(y2)
            yBigger.append(y1)
        if (y3 < y4):
            ySmaler.append(y3)
            yBigger.append(y4)
        else:
            ySmaler.append(y4)
            yBigger.append(y3)
            
        for x in xSmaler:
            if (x > ix):
                return False
        for x in xBigger:
            if (x < ix):
                return False
        for y in ySmaler:
            if (y > iy):
                return False
        for y in yBigger:
            if (y < iy):
                return False
        
        return True
        
    def rearangeElements (indexStart, indexEnd, pointArr):
        point1 = pointArr[indexStart]
        point2 = pointArr[indexStart + 1]
        point3 = pointArr[indexEnd - 1]
        point4 = pointArr[indexEnd]
        
        
        distStart = (calculateDistanceBetwenTwoPoints(point1, point2) +
                     calculateDistanceBetwenTwoPoints(point3, point4))
        distNew = (calculateDistanceBetwenTwoPoints(point1, point3) +
                   calculateDistanceBetwenTwoPoints(point2, point4))
        
        if (distNew < distStart):
            middlePoints = []
            for p in range(indexStart + 1, indexEnd):
                middlePoints.append(pointArr[p])
            # another loop so the index matches ...
            for midPoint in middlePoints:
                pointArr.remove(midPoint)
            for midPoint in middlePoints:
                pointArr.insert(indexStart + 1, midPoint)
        return pointArr
    
    checkingPointsNum = 200
    
    pointsArray = copy.deepcopy(_pointsArray)
    pointLast =pointsArray[len(pointsArray) -1]
    pointsArray.remove(pointLast)
    
    minDist = calculateTotalTravelDistance(pointsArray)
    while(True):
        for i in range (1, len(pointsArray)):
            point1 = pointsArray[i-1]
            point2 = pointsArray[i]
            
            line1 = (point1.posNumeric, point2.posNumeric)
            
            for j in range (i+1, i + checkingPointsNum):
                point3 = None
                try:
                    point3 = pointsArray[j]
                except IndexError:
                    continue
                point4 = None
                if (j == len(pointsArray)):
                    point4 = pointsArray[0]
                else:
                    try:
                        point4 = pointsArray[j + 1]
                    except IndexError:
                        continue
                line2 = (point3.posNumeric, point4.posNumeric)
                
                if (doesLinesIntersect(line1, line2)):
                    pointsArray = rearangeElements(i - 1, j + 1, pointsArray) 
                    break
        
        pointsArray.append(copy.deepcopy(pointsArray[0]))
        
        pointsArray = sortSwitchLoop(pointsArray)
        pointsArray = sortLoopAlgoritmReduceMaxDistance(pointsArray)
        
        newDist = calculateTotalTravelDistance(pointsArray)
        if (newDist < minDist):
            minDist = newDist
            pointsArray.remove(pointsArray[len(pointsArray)-1])
        else:
            break
        
        
    return pointsArray

# Main function
def main (_numberOfPoints, _plotGraph = True):
    # number of points and grid size
    numberOfPoints = _numberOfPoints
#    gridSize = 2                    # if we wish a specific grid size
    gridSize = numberOfPoints/4     # grid size relative to number of points
    
    
    # geberating random points
    pointsArray = generateRandomPoints(numberOfPoints, gridSize)
    # if we want to use specific points
#    pointsArray = generateCustomePoints()   #10.627,75

    # checking for actual grid size 
    xPos = []
    yPos = []
    for singlePoint in pointsArray:
        xPos.append(singlePoint.xPos)
        yPos.append(singlePoint.yPos)
    xGridMinMax = [min(xPos), max(xPos)]
    yGridMinMax = [min(yPos), max(yPos)]
    # generating anchor positions
    anchorPotitions = generateAnchorPositions(xGridMinMax, yGridMinMax)
    
    # generating anchor distances for each point
    for point in pointsArray:
        point.generateAnchorDistances(anchorPotitions)
    
    # total distance in before sorting
    totalDistnceStart = calculateTotalTravelDistance(pointsArray)
    # currnet total distance
    totalDistnceCurrent = totalDistnceStart
    
    
    
    
    
#    # first sorting
    
#    pointsArray = sortStartAlgoritem(pointsArray)
    pointsArray = sortStartAlgoritem2(pointsArray)
    firstSortTotalDistance = calculateTotalTravelDistance(pointsArray)
     # second sorting
    pointsArray = sortSwitchLoop(pointsArray)
    secondSortTotalDistance = calculateTotalTravelDistance(pointsArray)    
    # third sorting
    pointsArray = sortLoopAlgoritmReduceMaxDistance(pointsArray)
    thirdSortTotalDistance = calculateTotalTravelDistance(pointsArray)  
    # fourth sorting
    pointsArray = sortIntersections(pointsArray)
    fourthSortTotalDistance = calculateTotalTravelDistance(pointsArray)  
    
    # calculating total distance in the end
    totalDistnceCurrent = calculateTotalTravelDistance(pointsArray)

    # show the graph if wanted
    if _plotGraph:
        graphPlot(pointsArray, "r", 1.7)

    # print starting and finished total distances
    print (f"\nTotal distance on start:  {totalDistnceStart}")
    print (f"Total distance after first sort:  {firstSortTotalDistance}")
    print (f"Total distance after second sort:  {secondSortTotalDistance}")
    print (f"Total distance after third sort:  {thirdSortTotalDistance}")
    print (f"Total distance after fourth sort:  {fourthSortTotalDistance}")
    print(f"Total distance on finish:  {totalDistnceCurrent}")
    
    
    

startTime = datetime.datetime.now()
main(2000, True)
endTime = datetime.datetime.now()
print ("\n Time needed: " + str(endTime - startTime))



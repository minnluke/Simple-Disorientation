import rhinoscriptsyntax as rs
import random

#Minn Maung 05.02.2022
#Simple Disorientation

rs.EnableRedraw(False)

###n is volume of room###
n = rs.GetReal("Please provide the volume of room")
rect = rs.AddRectangle((0,0,0),n,n)
rs.HideObject(rect)
center = rs.CurveAreaCentroid(rect)
center = rs.AddPoint(center[0])
rs.HideObject(center)
center0 = rs.CopyObject(center,(0,0,n))
path = rs.AddLine(center,center0)
rs.HideObject(path)

box = rs.ExtrudeCurve(rect,path)
rs.CapPlanarHoles(box)

boxList = []
boxList.append(box)

###randomly generating the surface of the object###

objList = []
i = rs.GetInteger("Please provide number of room")
for i in range (0,i):
    sc = random.uniform(0.1,1)
    sc0 = random.uniform(0.1,1)
    
###creating the surfaces around a center point###
    polySrf = boxList[-1]
    
    areaCen = rs.SurfaceAreaCentroid(polySrf)
    areaCen = rs.AddPoint(areaCen[0])
    rs.HideObject(areaCen)
    
    expPoly = rs.ExplodePolysurfaces(polySrf)
    rs.HideObject(expPoly)
    
    rand = random.randint(0,len(expPoly)-1)
    
    cent = rs.SurfaceAreaCentroid(expPoly[rand])
    cent = rs.AddPoint(cent[0])
    rs.HideObject(cent)
    
    vect = rs.VectorCreate(cent,areaCen)
    vect = vect*2
    
    newPoly = rs.CopyObject(polySrf,vect)
    rs.HideObject(newPoly)
    areaCen0 = rs.SurfaceAreaCentroid(newPoly)
    areaCen0 = rs.AddPoint(areaCen0[0])
    rs.HideObject(areaCen0)
    
    expNewPoly = rs.ExplodePolysurfaces(newPoly)
    rs.HideObject(expNewPoly)
    scNewPoly = rs.ScaleObject(newPoly,areaCen0,(sc,sc,sc),True)
    rs.HideObject(scNewPoly)
    expScPoly = rs.ExplodePolysurfaces(scNewPoly)
    rs.HideObject(expScPoly)
    
    for m in range (0,len(expNewPoly)):
        
        loftList = []
        
        bor0 = rs.DuplicateSurfaceBorder(expNewPoly[m])
        refCen = rs.CurveAreaCentroid(bor0)
        refCen = rs.AddPoint(refCen[0])
        rs.HideObject(refCen)
        bor0 = rs.ScaleObject(bor0,refCen,(sc0,sc0,sc0))
        loftList.append(bor0)
        
        bor1 = rs.DuplicateSurfaceBorder(expScPoly[m])
        loftList.append(bor1)
        
        newSrf = rs.AddLoftSrf(loftList,None,None,3)
        objList.append(newSrf)
    
        rs.HideObject(polySrf)
    
        boxList.append(newPoly)

###Deleting curves###
crvs=rs.ObjectsByType(4, True)
rs.DeleteObjects(crvs)

###adding materiality and color to each of the panels###
for i in range (0,len(objList)):
    
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    Color = rs.CreateColor(r,g,b)
    rs.AddMaterialToObject(objList[i])
    rs.ObjectColor(objList[i],Color)
    Index = rs.ObjectMaterialIndex(objList[i])
    rs.MaterialColor(Index,Color)

print(objList)
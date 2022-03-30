import maya.cmds as cmds

#curve = cmds.listConnections(t='animCurve')

#offset translateX curve (test)
cmds.keyframe(attribute='translateX', o="move", relative = True, valueChange=5.0)


#Get the value of translateY at the current frame
# Answer return 0
time_ = cmds.currentTime( query=True )
value_ =cmds.keyframe('pCube1',at='ty',t=(time_,time_),q=True,eval=True)
print(value_)




#Mistake
# value_ = cmds.getAttr('pCube1_translateY',time=1)
# print(value_)
# object = "pCube1"
# attr = "ty"

# value_ =cmds.keyframe(object + "." + attr)
# print(value_)

#cmds.scaleKey(curve[2], valuePivot=0, valueScale=10 ) 






#Create Offset Func
#get to select all animation curve 
#offset curve


import maya.cmds as cmds

curves_attrs = cmds.listConnections(t='animCurve', c=True, p=True, d=False)
input_attrs = curves_attrs[0::2]

for input_ in input_attrs:
    node = input_.split(".")[0]
    attr = ".".join(input_.split(".")[1:])   
    # print(node)
    # print(attr)


#Get the value of translateY at the current frame
time_ = cmds.currentTime( query=True )
key_val =cmds.keyframe("pCube1",at='translateY',t=(time_,time_),q=True,eval=True)
print(key_value)

#keyフレームの値とチャンネルボックスの値が違うのだけプリント
ch_val = cmds.getAttr("pCube1.translateY")
print(ch_val)

#compare values of list 値が異なったら　ノード名とアトリビュート名をプリント
# if key_val != ch_val:
#     print(node)
#     print(attr)


#違う値の差分をだして、その値を使ってカーブをオフセット



#offset translateX curve (test)
#cmds.keyframe(attribute='translateX', o="move", relative = True, valueChange=5.0)



#Mistake
# value_ = cmds.getAttr('pCube1_translateY',time=1)
# print(value_)
# object = "pCube1"
# attr = "ty"

# value_ =cmds.keyframe(object + "." + attr)
# print(value_)

#cmds.scaleKey(curve[2], valuePivot=0, valueScale=10 ) 
#input_attrs = [attrs for attrs in curves_attrs if attrs % 2 != 0]





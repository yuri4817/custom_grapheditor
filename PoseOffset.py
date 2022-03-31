import maya.cmds as cmds

#get curve attributes
curves_attrs = cmds.listConnections(t='animCurve', c=True, p=True, d=False)
input_attrs = curves_attrs[0::2]

for input_ in input_attrs:
    node = input_.split(".")[0]
    attr = ".".join(input_.split(".")[1:])  

    time_ = cmds.currentTime( query=True )
    key_val =cmds.keyframe(node,at=attr,t=(time_,time_),q=True,eval=True)
    #print(key_val)
    ch_val = [cmds.getAttr(input_)]
    #print(input_, ch_val)

    #keyフレームの値とチャンネルボックスの値が違うのだけプリント
    if key_val != ch_val:
        print(input_,key_val,ch_val)
        diff_val = ch_val[0] - key_val[0]
        #print(diff_val)

        #違う値の差分とどのアトリビュートかをだして、その値を使ってカーブをオフセット
        cmds.keyframe(at=attr, o="move", r=True, vc=diff_val)





#Mistake
# value_ = cmds.getAttr('pCube1_translateY',time=1)
# print(value_)
# object = "pCube1"
# attr = "ty"

# value_ =cmds.keyframe(object + "." + attr)
# print(value_)

#cmds.scaleKey(curve[2], valuePivot=0, valueScale=10 ) 
#input_attrs = [attrs for attrs in curves_attrs if attrs % 2 != 0]

#print(set(key_val) ^ set(ch_val))




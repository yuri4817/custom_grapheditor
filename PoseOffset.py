import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader


def poseOffset():
    curves_attrs = cmds.listConnections(t='animCurve', c=True, p=True, d=False)
    input_attrs = curves_attrs[0::2]

    for input_ in input_attrs:
        node = input_.split(".")[0]
        attr = ".".join(input_.split(".")[1:])  

        time_ = cmds.currentTime( query=True )
        key_val =cmds.keyframe(node,at=attr,t=(time_,time_),q=True,eval=True)
        ch_val = [cmds.getAttr(input_)]

        #keyフレームの値とチャンネルボックスの値が違うのだけプリント
        if key_val != ch_val:
            print(input_,key_val,ch_val)
            diff_val = ch_val[0] - key_val[0]
            #print(diff_val)

            #違う値の差分とどのアトリビュートかをだして、その値を使ってカーブをオフセット
            cmds.keyframe(at=attr, o="move", r=True, vc=diff_val)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        poseOffset()
        self.ui = QUiLoader().load("D:\\github\\CustomEditor\\poseoffset.ui")
        self.setCentralWidget(self.ui)
    #     for op in ('translate', 'rotate', 'scale'):
    #         for axis in ('X', 'Y', 'Z'): 
    #             name = op + axis  
    #             obj = getattr(self.ui, name)
    #             obj.toggled.connect(lambda value, name_=name: graphEditorFilterAttributes([name_], [value]))
    #     self.ui.translate.clicked.connect(lambda: self.togglebutton('translate'))
        

    # def togglebutton(self, op):
    #     value = not all((getattr(self.ui, op + axis).isChecked() for axis in ('X', 'Y', 'Z')))
    #     for axis in ('X', 'Y', 'Z'): 
    #         name = op + axis  
    #         obj = getattr(self.ui, name)
    #         blocked = obj.blockSignals(True)
    #         obj.setChecked(value)
    #         obj.blockSignals(blocked)
        
    #     names = [op + 'X', op + 'Y', op + 'Z']
    #     values = [value, value, value]
    #     graphEditorFilterAttributes(names, values)



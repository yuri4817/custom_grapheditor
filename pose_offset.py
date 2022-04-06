import os
import imp
import inspect
from maya import cmds
from maya import mel
from maya import OpenMayaUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = QUiLoader().load("D:\\github\\CustomEditor\\poseoffset.ui")
        self.setCentralWidget(self.ui)

        self.ui.poseoffset.clicked.connect(self.poseOffset)

    def poseOffset(self):
        curves_attrs = cmds.listConnections(t='animCurve', c=True, p=True, d=False)
        input_attrs = curves_attrs[0::2]

        for input_ in input_attrs:
            node = input_.split(".")[0]
            attr = ".".join(input_.split(".")[1:])  

            time_ = cmds.currentTime( query=True )
            key_val =cmds.keyframe(node,at=attr,t=(time_,time_),q=True,eval=True)[0]
            ch_val = cmds.getAttr(input_)

            #keyフレームの値とチャンネルボックスの値が違うのだけプリント
            if key_val != ch_val:
                print(input_,key_val,ch_val)
                diff_val = ch_val - key_val
                #print(diff_val)

                #違う値の差分とどのアトリビュートかをだして、その値を使ってカーブをオフセット
                cmds.keyframe(at=attr, o="move", r=True, vc=diff_val)
    window = MainWindow()
    window.show()


#wt-0 0,10
#wt-1 4,8

#wt
#0-10の範囲のキーフレームの値を取得
#4-8の範囲だけオフセット。それ以外の範囲は各キーフレーム値に対して掛け算していく？

# -*- coding:utf-8 -*-
from __future__ import print_function, absolute_import, division

import os
from maya import cmds
from maya import mel
from maya import OpenMaya
from maya import OpenMayaUI
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
import shiboken2


class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.ui = QUiLoader().load(os.path.splitext(__file__)[0] + "_v1" + ".ui")
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.ui)
        self.setLayout(layout)

        self.ui.poseoffset.clicked.connect(self.poseOffset)
        self.ui.gradctrl = cmds.gradientControlNoAttr(dc = self.dragCallback)
        ptr = OpenMayaUI.MQtUtil.findControl(self.ui.gradctrl)
        widget = shiboken2.wrapInstance(long(ptr), QWidget)
        self.ui.gradientControlLayout.addWidget(widget)

    def poseOffset(self):
        curves_attrs = cmds.listConnections(t='animCurve', c=True, p=True, d=False)
        input_attrs = curves_attrs[0::2]

        for input_ in input_attrs:
            node = input_.split(".")[0]
            attr = ".".join(input_.split(".")[1:])  

            time_ = cmds.currentTime( query=True )
            key_val =cmds.keyframe(node,at=attr,t=(time_,time_),q=True,eval=True)[0]
            ch_val = cmds.getAttr(input_)

            if key_val != ch_val:
                print(input_,key_val,ch_val)
                diff_val = ch_val - key_val
            
                cmds.keyframe(at=attr, o="move", r=True, vc=diff_val)


    def dragCallback(self, *args):
        _values = cmds.gradientControlNoAttr(self.ui.gradctrl, q=True, asString = True)
        _values_list = _values.split(",")
        key_index = cmds.gradientControlNoAttr(self.ui.gradctrl, q=True, ck=True)
        # key_index -= 1  key_indexが１番開始ならいるかも
        x_val = _values_list[3 * key_index + 1]
        y_val = _values_list[3 * key_index + 0]
        interp_val = _values_list[3 * key_index + 2]    




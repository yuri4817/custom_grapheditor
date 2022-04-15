# -*- coding:utf-8 -*-
from __future__ import print_function, absolute_import, division

import os
from maya import cmds
from maya import mel
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader



def graphEditorOutlineEds():
    graph_panels = set()
    for panel in cmds.getPanel(type='scriptedPanel') or []:
        if cmds.scriptedPanel(panel, query=True, type=True) != 'graphEditor':
            continue
        graph_panels.add(panel)
    outliner_editors = set()
    for editor in cmds.lsUI(editors=True) or []:
        if not cmds.outlinerEditor(editor, exists=True):
            continue
        if cmds.outlinerEditor(editor, q=True, masterOutliner=True):
            continue
        if cmds.outlinerEditor(editor, q=True, panel=True) not in graph_panels:
            continue
        outliner_editors.add(editor)
    return list(outliner_editors)



def graphEditorFilterAttributes(attrs, values):
    if len(attrs) != len(values):
        raise ValueError
    
    cmd = ''
    for editor in graphEditorOutlineEds():
        for attr, value in zip(attrs, values):
            cmd += 'filterUISelectAttributesCheckbox {} {:d} {};'.format(attr, value, editor)
    mel.eval(cmd)  

class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        graphEditorFilterAttributes(['translateX','translateY','translateZ','rotateX','rotateY','rotateZ','scaleX','scaleY','scaleZ','visibility'], [False,False,False,False,False,False,False,False,False,False])
        self.ui = QUiLoader().load(os.path.splitext(__file__)[0] + ".ui")
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.ui)
        self.setLayout(layout)
        for op in ('translate', 'rotate', 'scale'):
            for axis in ('X', 'Y', 'Z'): 
                name = op + axis  
                obj = getattr(self.ui, name)
                obj.toggled.connect(lambda value, name_=name: graphEditorFilterAttributes([name_], [value]))
        self.ui.v.toggled.connect(lambda value: graphEditorFilterAttributes(['visibility'], [value]))
        self.ui.translate.clicked.connect(lambda: self.togglebutton('translate'))
        self.ui.rotate.clicked.connect(lambda: self.togglebutton('rotate'))
        self.ui.scale.clicked.connect(lambda: self.togglebutton('scale'))
        self.ui.visibility.clicked.connect(lambda: self.togglebutton('visibility'))


        

    def togglebutton(self, op):
        if op in ("translate", "rotate", "scale"):
            value = not all((getattr(self.ui, op + axis).isChecked() for axis in ('X', 'Y', 'Z')))
            for axis in ('X', 'Y', 'Z'): 
                name = op + axis  
                obj = getattr(self.ui, name)
                blocked = obj.blockSignals(True)
                obj.setChecked(value)
                obj.blockSignals(blocked)
        
            names = [op + 'X', op + 'Y', op + 'Z']
            values = [value, value, value]

            graphEditorFilterAttributes(names, values)
        else:
            value = not self.ui.v.isChecked()
            blocked = self.ui.v.blockSignals(True)
            self.ui.v.setChecked(value)
            self.ui.v.blockSignals(blocked)
            names = ["visibility"]
            values = [value]
            graphEditorFilterAttributes(names, values)





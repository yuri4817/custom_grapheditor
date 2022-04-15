# -*- coding:utf-8 -*-
from __future__ import print_function, absolute_import, division

from maya import cmds
import custom_grapheditor.mwidget
import custom_grapheditor.curvefilter
import custom_grapheditor.poseoffset
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
reload(custom_grapheditor.mwidget)
reload(custom_grapheditor.curvefilter)
reload(custom_grapheditor.poseoffset)

class Window(custom_grapheditor.mwidget.MayaQWidgetDockableMixin,QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(custom_grapheditor.curvefilter.Widget())
        layout.addWidget(custom_grapheditor.poseoffset.Widget())
        self.setLayout(layout)
        self.setWindowTitle("Custom GraphEditor")



def show():
    Window.delete()
    window = Window()
    window.show(dockable=True, restore=True, retain=False)
    cmds.GraphEditor()
    graph_panels = []
    for panel in cmds.getPanel(type='scriptedPanel') or []:
        if cmds.scriptedPanel(panel, query=True, type=True) != 'graphEditor':
            continue
        graph_panels.append(panel)
    graph_window = cmds.scriptedPanel('graphEditor1', q=True, control=True).split('|')[0]
    cmds.workspaceControl(window.name, edit=True, dockToControl=[graph_window, 'bottom'])
      




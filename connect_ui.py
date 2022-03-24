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

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        graphEditorFilterAttributes(['translateX','translateY','translateZ','rotateX','rotateY','rotateZ','scaleX','scaleY','scaleZ','visibility'], [False,False,False,False,False,False,False,False,False,False])
        self.ui = QUiLoader().load("D:\\github\\CustomEditor\\graphEditorFilterAttributes.ui")
        self.setCentralWidget(self.ui)
        for op in ('translate', 'rotate', 'scale'):
            for axis in ('X', 'Y', 'Z'): 
                name = op + axis  
                obj = getattr(self.ui, name)
                obj.toggled.connect(lambda value, name_=name: graphEditorFilterAttributes([name_], [value]))
        self.ui.visibility.toggled.connect(lambda value: graphEditorFilterAttributes(['visibility'], [value]))
        self.ui.translate.clicked.connect(lambda: self.togglebutton('translate'))
        self.ui.rotate.clicked.connect(lambda: self.togglebutton('rotate'))
        self.ui.scale.clicked.connect(lambda: self.togglebutton('scale'))
        

    def togglebutton(self, op):
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




# Create UI of maya workspace

# class MayaQWidgetDockable(MayaQWidgetDockableMixin, QWidget):
#     def __init__(self, *args, **kwargs):
#         super(MayaQWidgetDockable, self).__init__(*args, **kwargs)
#         self.setObjectName(self.__class__.__name__)
#         self.setAttribute(Qt.WA_DeleteOnClose)
#         # self.setProperty('saveWindowPref', True)
#     @property
#     def name(self):
#         return self.__class__.__name__ + 'WorkspaceControl'
#     def show(self, **kwargs):
#         mdl_name = inspect.getmodule(self).__name__
#         cls_name = self.__class__.__name__
#         pkg_name = mdl_name.split('.')[0]
#         pkg_path = os.path.dirname(imp.find_module(pkg_name)[1])
#         kwargs['uiScript'] = 'import sys; None if {!r} in sys.path else sys.path.append({!r}); import {}; {}.{}()._restore()'.format(
#             pkg_path, pkg_path, mdl_name, mdl_name, cls_name)
#         super(MayaQWidgetDockable, self).show(**kwargs)
#         print(kwargs['uiScript'])
#     @classmethod
#     def delete(cls):
#         name = cls.__name__ + 'WorkspaceControl'
#         if cmds.workspaceControl(name, q=True, ex=True):
#             cmds.workspaceControl(name, e=True, cl=True)
#             try:
#                 cmds.deleteUI(name, ctl=True)
#             except RuntimeError:
#                 pass
#     def _restore(self):
#         workspace_control = OpenMayaUI.MQtUtil.getCurrentParent()
#         mixin_ptr = OpenMayaUI.MQtUtil.findControl(self.objectName())
#         OpenMayaUI.MQtUtil.addWidgetToMayaLayout(long(mixin_ptr), long(workspace_control))

from maya import cmds
from maya import OpenMayaUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import shiboken2
class MayaQWidgetDockable(MayaQWidgetDockableMixin, QWidget):
    def __init__(self, *args, **kwargs):
        super(MayaQWidgetDockable, self).__init__(*args, **kwargs)
        self.setObjectName(self.__class__.__name__)
        self.setAttribute(Qt.WA_DeleteOnClose)
        # self.setProperty('saveWindowPref', True)
    @property
    def name(self):
        return self.__class__.__name__ + 'WorkspaceControl'
    def createMayaWidget(self):
        pass
    def show(self, **kwargs):
        mdl_name = inspect.getmodule(self).__name__
        cls_name = self.__class__.__name__
        pkg_name = mdl_name.split('.')[0]
        pkg_path = os.path.dirname(imp.find_module(pkg_name)[1])
        kwargs['uiScript'] = 'import sys; None if {!r} in sys.path else sys.path.append({!r}); import {}; {}.{}()._restore()'.format(
            pkg_path, pkg_path, mdl_name, mdl_name, cls_name)
        ex = cmds.workspaceControl(self.name, q=True, ex=True)
        super(MayaQWidgetDockable, self).show(**kwargs)
        if ex:
            return
        layout = self.findChild(QLayout)
        if layout is None:
            layout = QVBoxLayout()
            layout.setObjectName(self.__class__.__name__ + 'Layout')
            layout.setContentsMargins(0, 0, 0, 0)
            self.setLayout(layout)
        parent = cmds.setParent(q=True)
        if (layout is None) or (not layout.objectName()):
            name = self.name
        else:
            ptr = shiboken2.getCppPointer(layout)
            name = OpenMayaUI.MQtUtil.fullName(long(ptr[0]))
        cmds.setParent(name)
        self.createMayaWidget()
        cmds.setParent(parent)
    @classmethod
    def delete(cls):
        name = cls.__name__ + 'WorkspaceControl'
        if cmds.workspaceControl(name, q=True, ex=True):
            cmds.workspaceControl(name, e=True, cl=True)
            try:
                cmds.deleteUI(name, ctl=True)
            except RuntimeError:
                pass
    def _restore(self):
        workspace_control = OpenMayaUI.MQtUtil.getCurrentParent()
        mixin_ptr = OpenMayaUI.MQtUtil.findControl(self.objectName())
        OpenMayaUI.MQtUtil.addWidgetToMayaLayout(long(mixin_ptr), long(workspace_control))
        layout = self.findChild(QLayout)
        if layout is None:
            layout = QVBoxLayout()
            layout.setObjectName(self.__class__.__name__ + 'Layout')
            layout.setContentsMargins(0, 0, 0, 0)
            self.setLayout(layout)
        if (layout is None) or (not layout.objectName()):
            name = self.name
        else:
            ptr = shiboken2.getCppPointer(layout)
            name = OpenMayaUI.MQtUtil.fullName(long(ptr[0]))
        parent = cmds.setParent(q=True)
        cmds.setParent(name)
        self.createMayaWidget()
        cmds.setParent(parent)


class CustomGraphEditor(MayaQWidgetDockable):
    def __init__(self, *args, **kwargs):
        super(CustomGraphEditor, self).__init__(*args, **kwargs)
        layout = QHBoxLayout()
        layout.addWidget(MainWindow())
        self.setLayout(layout)
        self.setWindowTitle('CustomGraphEditor')

def show():
    CustomGraphEditor.delete()
    CustomGraphEditor().show(dockable=True, restore=True, retain=False)
if __name__ == '__main__':
    show()



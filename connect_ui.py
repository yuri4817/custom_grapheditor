from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
import functools


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
        self.ui = QUiLoader().load("D:\\github\\CustomEditor\\graphEditorFilterAttributes.ui")
        self.setCentralWidget(self.ui)
        for op in ('translate', 'rotate', 'scale'):
            for axis in ('X', 'Y', 'Z'): 
                name = op + axis  
                obj = getattr(self.ui, name)
                # obj.toggled.connect(functools.partial(graphEditorFilterAttribute,name))
                obj.toggled.connect(lambda value, name_ = name:graphEditorFilterAttributes([name_], [value]))
        
        self.ui.visibility.toggled.connect(lambda value, name = 'visibility':graphEditorFilterAttributes(name, [value]))
        self.ui.translate.clicked.connect(lambda:self.togglebutton('translate'))
        self.ui.rotate.clicked.connect(lambda:self.togglebutton('rotate'))
        self.ui.scale.clicked.connect(lambda:self.togglebutton('scale'))
        

    def togglebutton(self, op):
        # bool_list = []
        # for op in ('translate',):
        #     # test = all((getattr(self.ui, op + axis).isChecked() for axis in ('X', 'Y', 'Z')))
        #     # #print(test)
        # for axis in ('X', 'Y', 'Z'): 
        #     name = op + axis  
        #     obj = getattr(self.ui, name)
        #     #print(obj)
        #     obj.isChecked()
        #     #print(obj.isChecked())
            
        #     bool_list.append(obj.isChecked())

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
            
        
        # for axis in ('X', 'Y', 'Z'): 
        #     name = op + axis  
        #     obj = getattr(self.ui, name)
        #     blocked = obj.blockSignals(True)
        #     obj.setChecked(True)
        #     obj.blockSignals(blocked)
        # names = [op + 'X', op + 'Y', op + 'Z']
        # graphEditorFilterAttributes(names, [True,True,True])



#block signal
#call function 
#change checkbox
#don't block signal
        

    

window = MainWindow()
window.show()



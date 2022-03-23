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

#graphEditorFilterAttributes(['translateX', 'rotateZ', 'scaleY'], [True, False, False])


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = QUiLoader().load("D:\\graphEditorFilterAttributes.ui")
        self.setCentralWidget(self.ui)
        for op in ('translate', 'rotate', 'scale'):
            for axis in ('X', 'Y', 'Z'): 
                name = op + axis  
                obj = getattr(self.ui, name)
                # obj.toggled.connect(functools.partial(
                #     graphEditorFilterAttribute,name))
                obj.toggled.connect(lambda value, name_ = name:graphEditorFilterAttributes([name_], [value]))
        self.ui.visibility.toggled.connect(graphEditorFilterAttributes)
        #self.togglebutton()
        self.ui.translate.clicked.connect(self.togglebutton)
        #print(self.togglebutton)

    def togglebutton(self):
        bool_list = []
        for op in ('translate',):
            # test = all((getattr(self.ui, op + axis).isChecked() for axis in ('X', 'Y', 'Z')))
            # #print(test)
            for axis in ('X', 'Y', 'Z'): 
                name = op + axis  
                obj = getattr(self.ui, name)
                #print(obj)
                obj.isChecked()
                #print(obj.isChecked())
                #return "haichu"
                bool_list.append(obj.isChecked())
        if  all(bool_list) == True:
            #print("pika")
            
            for op in ('translate',):
                for axis in ('X', 'Y', 'Z'): 
                    name = op + axis  
                    obj = getattr(self.ui, name)
                    #print(obj)
                    obj.setChecked(False)
            
        else:
            #print("raichu")
            for op in ('translate',):
                for axis in ('X', 'Y', 'Z'): 
                    name = op + axis  
                    obj = getattr(self.ui, name)
                    obj.setChecked(True)



        

        
    
    # def graphEditorFilterAttributes(self):
    #     values = []
    #     for op in ('translate', 'rotate', 'scale'):
    #         for axis in ('X', 'Y', 'Z'): 
    #             name = op + axis   
    #             obj = getattr(self.ui, name)
    #             values.append(obj.isChecked())
    #     values.append(self.ui.visibility.isChecked())
    #     graphEditorFilterAttributes(*values)
    

window = MainWindow()
window.show()

#window.graphEditorFilterAttributes()


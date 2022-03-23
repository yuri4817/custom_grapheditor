from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
import functools


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = QUiLoader().load("D:\\MAC_Demo\\resources\\tools\\maya\\python\\graph_editor\\graphEditorFilterAttributes.ui")
        self.setCentralWidget(self.ui)
        for op in ('translate', 'rotate', 'scale'):
            for axis in ('X', 'Y', 'Z'): 
                name = op + axis  
                obj = getattr(self.ui, name)
                obj.toggled.connect(functools.partial(
                    graphEditorFilterAttribute,name))
                #obj.toggled.connect(lambda value, name_=name:graphEditorFilterAttribute(name_, value))

                
    #     self.ui.visibility.stateChanged.connect(graphEditorFilterAttribute)
 
    
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


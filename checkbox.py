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




def graphEditorFilterAttributes(tx, ty, tz, rx, ry, rz, sx, sy, sz, v):
    graph_outliner_editors = graphEditorOutlineEds()
    
    values = [[tx,ty,tz],[rx,ry,rz],[sx,sy,sz]]
    attrs = [["translateX","translateY","translateZ"],["rotateX","rotateY","rotateZ"],["scaleX","scaleY","scaleZ"]]
    v_val = v
    
    for val, attr in zip(values,attrs):
        for v, a in zip(val, attr):
           if v == True:
               a = ("filterUISelectAttributesCheckbox " + a + " 1 ")
           if v == False:
                a = ("filterUISelectAttributesCheckbox " + a + " 0 ")

           for g in graph_outliner_editors:
                 mel.eval(a + g + ";")
                 
                 mel.eval("filterUISelectAttributesCheckbox visibility 1 " + g + ";") 
                 if v_val == False:
                      mel.eval("filterUISelectAttributesCheckbox visibility 0 " + g + ";") 
    
         
        

graphEditorFilterAttributes(
True, False, False,
False, False, False,
False, False, False,
False)


    
    
    
    
    
    
    
    
    
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
    cmd = ''
    values = ((tx, ty, tz), (rx, ry, rz), (sx, sy, sz))
    for editor in graphEditorOutlineEds():
        for op, values_ in zip(('translate', 'rotate', 'scale'), values):
            for axis, value in zip(('X', 'Y', 'Z'), values_):
                cmd += 'filterUISelectAttributesCheckbox {}{} {:d} {};'.format(op, axis, value, editor)
        cmd += 'filterUISelectAttributesCheckbox visibility {:d} {};'.format(v, editor)
    mel.eval(cmd)
    
    
    
graphEditorFilterAttributes(
    True, False, False,
    False, True, False,
    False, False, True,
    True)
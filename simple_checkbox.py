def graphEditorFilterAttribute(attr, value):
    for editor in graphEditorOutlineEds():
        if value == True:
            mel.eval("filterUISelectAttributesCheckbox " + attr + " 1 " + editor + ";")
        if value == False:
            mel.eval("filterUISelectAttributesCheckbox " + attr + " 0 " + editor + ";")

        
        
graphEditorFilterAttribute("scaleZ",True)



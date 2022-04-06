# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import imp
import inspect

from maya import cmds
from maya import OpenMayaUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin as _MayaQWidgetDockableMixin
from PySide2 import QtCore


class _GCProtector(object):
    widgets = []


class MayaQWidgetDockableMixin(_MayaQWidgetDockableMixin):
    def __init__(self, *args, **kwargs):
        super(MayaQWidgetDockableMixin, self).__init__(*args, **kwargs)
        self.setObjectName(self.__class__.__name__)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    
    def show(self, **kwargs):
        cls_name = self.__class__.__name__
        mdl_name = inspect.getmodule(self).__name__
        pkg_name = mdl_name.split('.')[0]
        pkg_path = os.path.dirname(imp.find_module(pkg_name)[1])

        if 'uiScript' in kwargs:
            kwargs['uiScript'] += '; import sys; None if {!r} in sys.path else sys.path.append({!r}); import {}; {}.{}.restore()'.format(
                pkg_path, pkg_path, mdl_name, mdl_name, cls_name)
        else:
            kwargs['uiScript'] = 'import sys; None if {!r} in sys.path else sys.path.append({!r}); import {}; {}.{}.restore()'.format(
                pkg_path, pkg_path, mdl_name, mdl_name, cls_name)
        
        super(MayaQWidgetDockableMixin, self).show(**kwargs)
        
    @property
    def name(self):
        return self.__class__.__name__ + 'WorkspaceControl'
    
    @classmethod
    def delete(cls):
        if cmds.workspaceControl(cls.__name__ + 'WorkspaceControl', q=True, ex=True):
            try:
                cmds.workspaceControl(cls.__name__ + 'WorkspaceControl', e=True, cl=True)
                cmds.deleteUI(cls.__name__ + 'WorkspaceControl', ctl=True)
            except RuntimeError:
                pass

    @classmethod
    def restore(cls):
        widget = cls()
        _GCProtector.widgets.append(widget)

        workspace_control = OpenMayaUI.MQtUtil.getCurrentParent()
        mixin_ptr = OpenMayaUI.MQtUtil.findControl(cls.__name__)
        OpenMayaUI.MQtUtil.addWidgetToMayaLayout(long(mixin_ptr), long(workspace_control))
        
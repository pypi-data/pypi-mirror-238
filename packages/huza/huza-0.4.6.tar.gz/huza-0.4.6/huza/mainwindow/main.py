# coding=utf-8
from typing import Union
from PyQt5.QtWidgets import QTabWidget, QMainWindow

try:
    from huza.base.mainwindow_run import MainWindowRun
except ImportError:
    MainWindowRun = None
from huza.mainwindow.main_actions import *
from huza.mainwindow.main_docks import *
from huza.mainwindow.main_ribbon import *
from huza.ribbon.RibbonTab import RibbonTab
from huza.ribbon.RibbonWidget import RibbonWidget
from huza.util.mainui import *


class MainWindow_Form(object):
    init_ribbon = init_ribbon
    init_docks = init_docks
    addAction = addAction
    set_dock_view = setDockView
    set_dock_view_none = set_dock_view_none
    set_all_dock_visible = set_all_dock_visible
    get_extra = get_extra
    get_action = get_action
    get_dock = get_dock
    get_dock_current_ui = get_dock_current_ui
    get_dock_ui = get_dock_ui
    del_dock_ui = del_dock_ui
    get_all_dock = get_all_dock
    get_all_action = get_all_action
    get_all_dockview = get_all_dockview
    get_ui = get_ui
    _get_tab_name = get_tab_name
    _get_panel_name = get_panel_name

    def __init__(self, extra, icon_list):
        self.extra = extra
        self.icon_list = icon_list
        self.iconlist = self.icon_list
        self.runobj: MainWindowRun = None
        super(MainWindow_Form, self).__init__()

    def setupUi(self, Form):
        self.form: QMainWindow = Form
        self.docks = {}
        self.actions = {}
        self.signals = {}
        self.dockviews = {}  # 保存所有dock里面的widget对象
        self.load()

    def bind_signal(self, signal, func):
        self.signals[signal] = func

    def emit(self, signal, data):
        self.form.signal.emit(signal, data)

    def load(self):
        self.addRibbon()
        self._init_dock_env()

    def signalHeadle(self, key, args):
        if key in self.signals:
            self.signals[key](args)
        else:
            logger.warning(f'signal [{key}] emited, but there is no binding')

    def addRibbon(self):
        self.form._ribbon = RibbonWidget(self.form)
        self.form.addToolBar(self.form._ribbon)
        self._ribbon = self.form._ribbon

    def get_ribbon_tab(self) -> QTabWidget:
        return self.form._ribbon._ribbon_widget

    def get_ribbon_tab_item(self, tabname) -> Union[RibbonTab, None]:
        return self._get_tab_name(tabname)

    def get_ribbon_panel(self, tabname, panelname) -> Union[RibbonPane, None]:
        tabwidget = self.get_ribbon_tab_item(tabname)
        if tabwidget is None:
            return None
        return self._get_panel_name(tabwidget, panelname)

    def _init_dock_env(self):
        self.form.setDockNestingEnabled(True)
        w = self.form.takeCentralWidget()
        self.form.setContextMenuPolicy(Qt.PreventContextMenu)
        if w:
            del w

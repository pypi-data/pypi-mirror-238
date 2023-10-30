import re
from PyQt5 import QtGui, QtCore
from loguru import logger

from huza.icons.iconbase import DefaultIconHandler, IconHandler, Default1IconHandler, Default3IconHandler


class IconListHandlerBase(object):
    def __init__(self):
        self._iconlist = {'default': DefaultIconHandler(),
                          'd1': Default1IconHandler(),
                          'd3': Default3IconHandler(),
                          }

    def __getattr__(self, attr):
        if self._iconlist.get(attr) is not None:
            iconhandler = self._iconlist.get(attr)
            return iconhandler
        return None


class IconListHandler(IconListHandlerBase):
    def add_icon_list(self, name, img_database):
        if name in ['default', 'd1', 'd3']:
            raise Exception(f'不能覆盖默认的图表集 {name}')
        if name in self._iconlist:
            raise Exception(f'图表集已经存在 {name}')
        if not re.match(r'^[_]?[a-zA-Z]+[0-9]*$', name):
            raise Exception(f'图表集命名不规范 {name}')
        iconhandler = IconHandler()
        iconhandler._set_img_database(img_database)
        self._iconlist[name] = iconhandler


if __name__ == '__main__':
    from huza.icons.images.img import image_dict
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    c = IconListHandler()
    c.add_icon_list('dd', image_dict)
    dd = c.default.Calculatehortestpath_grid_671
    print(dd)

from tkinter import Label, X, Y, LEFT, TOP, Widget, RIGHT, BOTH
from typing import List, Callable

from ttkbootstrap import Frame, DARK, SECONDARY, LIGHT

from pytkUI.boot_utils import get_color
from pytkUI.ext.icon import Icon


class TabItem:
    def __init__(self, icon, label, frame: Widget, side=TOP, active=False):
        self.side = side
        self.icon = icon
        self.label = label
        self.frame = frame
        self.active = active


class Menu:
    def __init__(self, tab_item, nav_menu, icon, label):
        self.tab_item = tab_item
        self.nav_menu = nav_menu
        self.icon = icon
        self.label = label


class NavMenu(Frame):
    def __init__(self, parent, tab_items: List[TabItem], on_selected: Callable, default_color=DARK,
                 hover_color=SECONDARY, selected_color=SECONDARY, icon_txt_color=LIGHT, width=150, item_height=50):
        self.default_color = default_color
        self.hover_color = hover_color
        self.selected_color = selected_color

        self.icon_txt_color = get_color(icon_txt_color)
        self.selected_menu = None
        self.on_selected = on_selected

        super(NavMenu, self).__init__(parent, bootstyle=self.default_color, width=width)
        self.pack_propagate(False)
        self.nav_items = []
        for tab_item in tab_items:
            self.nav_items.append(self.__create_menu(tab_item, height=item_height))

        fm = self.nav_items[0]
        self.__click(fm.tab_item, fm.nav_menu, fm.icon, fm.label)

    def __create_menu(self, tab_item: TabItem, height):
        nav_menu = Frame(self, height=height, bootstyle=self.default_color, padding=(12, 0, 0, 0))
        icon = Icon(nav_menu, icon_name=tab_item.icon, size=30, color=self.icon_txt_color, name="icon")
        label = Label(nav_menu, text=tab_item.label, font=("", 12), name="label")

        nav_menu.pack_propagate(False)
        nav_menu.pack(fill=X, ipadx=10, ipady=10, side=tab_item.side)
        nav_menu.bind("<Enter>", lambda e: self.__enter(tab_item, nav_menu, icon, label))
        nav_menu.bind("<Leave>", lambda e: self.__leave(tab_item, nav_menu, icon, label))
        nav_menu.bind("<Button-1>", lambda e: self.__click(tab_item, nav_menu, icon, label))
        icon.bind("<Button-1>", lambda e: self.__click(tab_item, nav_menu, icon, label))
        label.bind("<Button-1>", lambda e: self.__click(tab_item, nav_menu, icon, label))

        icon.configure(background=get_color(self.default_color))
        icon.pack(side=LEFT, padx=(0, 12))

        label.pack(side=LEFT)
        label.configure(background=get_color(self.default_color), fg=self.icon_txt_color)

        return Menu(tab_item, nav_menu, icon, label)

    def __enter(self, _, menu, icon, label):
        if menu == self.selected_menu:
            return
        menu.configure(bootstyle=self.hover_color)
        icon.configure(background=get_color(self.hover_color))
        label.configure(background=get_color(self.hover_color))

    def __leave(self, _, menu, icon, label):
        if menu == self.selected_menu:
            return
        menu.configure(bootstyle=self.default_color)
        icon.configure(background=get_color(self.default_color))
        label.configure(background=get_color(self.default_color))

    def __click(self, menu, nav_menu, icon, label):
        if self.selected_menu is not None:
            _icon = self.selected_menu.children.get("icon")
            _label = self.selected_menu.children.get("label")
            tmp = self.selected_menu
            self.selected_menu = nav_menu
            self.__leave(None, tmp, _icon, _label)
        else:
            self.selected_menu = nav_menu

        nav_menu.configure(bootstyle=self.selected_color)
        icon.configure(background=get_color(self.selected_color))
        label.configure(background=get_color(self.selected_color))

        self.on_selected(menu)


class ExtTabs(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.nav = None
        self.cur_frame = None

    def init(self, tabs: List[TabItem]):
        self.nav = NavMenu(self, tab_items=tabs, on_selected=self.on_selected)
        self.nav.pack(side=LEFT, fill=Y)

    def on_selected(self, menu: TabItem):
        if self.cur_frame:
            self.cur_frame.forget()
        menu.frame.pack(side=RIGHT, fill=BOTH, expand=True)
        self.cur_frame = menu.frame

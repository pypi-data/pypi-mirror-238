from tkinter import Label

from pytkUI.utils import load_font_icon


class Icon(Label):
    def __init__(self, parent, icon_name, size, color, **kwargs):
        self.color = color
        self.size = size
        self.icon_name = icon_name
        super().__init__(parent, image=load_font_icon(self.icon_name, self.size, self.color), **kwargs)

    def change(self, icon_name=None, size=None, color=None):
        if icon_name:
            self.icon_name = icon_name
        if size:
            self.size = size
        if color:
            self.color = color
        self.configure(image=load_font_icon(self.icon_name, self.size, self.color))

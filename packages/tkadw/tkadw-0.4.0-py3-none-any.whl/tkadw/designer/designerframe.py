from functools import partial

from tkadw.windows.canvas.drawengine import AdwDrawEngine
from tkinter import Widget, Frame


class AdwDesignerFrame(AdwDrawEngine):
    def __init__(self, master=None, widget: Widget = Frame,
                 candragged: bool = True,
                 *args, **kwargs):
        """
        代码修改自 https://blog.csdn.net/tinga_kilin/article/details/113773393
        """
        super().__init__(master=master)

        self.default_palette()

        self.configure(bd=0, highlightthickness=0)

        try:
            self.configure(background=self.master.cget("background"))
            if hasattr(self.master, "frame_back"):
                self.configure(background=self.master.frame_back)
            self.update()
        except:
            pass

        self.widget = widget(self, *args, **kwargs)
        self.widget.pack(fill='both', expand=True, pady=9, padx=9)

        self.widget.bind("<Button-1>", self.mouse_down, add='+')
        self.candragged(candragged)
        self.widget.bind('<FocusOut>', lambda event: self.delete('all'))
        self.widget.bind('<FocusIn>', lambda event: (self._draw(), self.show()))

        self.is_sizing = False
        self.old_width = 0
        self.old_height = 0
        self.old_pos_x = 0
        self.old_pos_y = 0
        self.start_x = 0
        self.start_y = 0
        self.start_root_x = 0
        self.start_root_y = 0
        self.on_resize_complete = None

    def candragged(self, b: bool):
        if b:
            self._candragged = self.widget.bind("<B1-Motion>", self.drag, add='+')
        else:
            if hasattr(self, "_candragged"):
                self.widget.unbind("<B1-Motion>", self._candragged)

    def _mouse_down(self, event):
        self.startx = event.x
        self.starty = event.y

    def _drag(self, event):
        try:
            self.place(x=self.winfo_x() + (event.x - self.startx), y=self.winfo_y() + (event.y - self.starty))
        except AttributeError:
            raise ValueError("The widget %s is not draggable" % widget)

    def set_on_resize_complete(self, on_resize_complete):
        self.on_resize_complete = on_resize_complete

    def _draw(self):
        self.delete("all")
        self.create_rectangle(-1, -1, -2, -2, tag='side', dash=4, outline=self._frame_border)
        self.tag_bind('side', "<Button-1>", self._mouse_down, add='+')
        self.tag_bind('side', "<B1-Motion>", self._drag, add='+')
        self.tag_bind('side', '<Enter>', lambda event: self.config(cursor='fleur'))
        self.tag_bind('side', '<Leave>', lambda event: self.config(cursor='arrow'))
        for name in ('nw', 'w', 'sw', 'n', 's', 'ne', 'e', 'se'):
            self.create_rectangle(-1, -1, -2, -2, tag=name, outline=self._frame_grip)
            self.tag_bind(name, "<Enter>", partial(self.on_mouse_enter, name))
            self.tag_bind(name, "<Leave>", partial(self.on_mouse_leave, name))
            self.tag_bind(name, "<Button-1>", partial(self.on_mouse_click, name))
            self.tag_bind(name, "<B1-Motion>", partial(self.on_mouse_move, name))
            self.tag_bind(name, "<ButtonRelease-1>", partial(self.on_mouse_release, name))

    def show(self, is_fill=False):
        width = self.winfo_width()
        height = self.winfo_height()
        self.coords('side', 6, 6, width - 6, height - 6)
        self.coords('nw', 0, 0, 7, 7)
        self.coords('sw', 0, height - 8, 7, height - 1)
        self.coords('w', 0, (height - 7) / 2, 7, (height - 7) / 2 + 7)
        self.coords('n', (width - 7) / 2, 0, (width - 7) / 2 + 7, 7)
        self.coords('s', (width - 7) / 2, height - 8, (width - 7) / 2 + 7, height - 1)
        self.coords('ne', width - 8, 0, width - 1, 7)
        self.coords('se', width - 8, height - 8, width - 1, height - 1)
        self.coords('e', width - 8, (height - 7) / 2, width - 1, (height - 7) / 2 + 7)
        if is_fill:
            for name in ('nw', 'w', 'sw', 'n', 's', 'ne', 'e', 'se'):
                self.itemconfig(name, fill='blue')

    def hide(self):
        self.coords('side', -1, -1, -2, -2, )
        for name in ('nw', 'w', 'sw', 'n', 's', 'ne', 'e', 'se'):
            self.coords(name, -1, -1, -2, -2)

    def on_mouse_enter(self, tag_name, event):
        if tag_name in ("nw", "sw", "ne", "se"):
            self["cursor"] = "sizing"
        elif tag_name in ("w", "e"):
            self["cursor"] = "sb_h_double_arrow"
        else:
            self["cursor"] = "sb_v_double_arrow"

    def on_mouse_leave(self, tag_name, event):
        if self.is_sizing:
            return
        self["cursor"] = "arrow"

    def on_mouse_click(self, tag_name, event):
        self.is_sizing = True
        self.start_x = event.x
        self.start_y = event.y
        self.start_root_x = event.x_root
        self.start_root_y = event.y_root
        self.old_width = self.winfo_width()
        self.old_height = self.winfo_height()
        self.old_pos_x = int(self.place_info()['x'])
        self.old_pos_y = int(self.place_info()['y'])

    def on_mouse_move(self, tag_name, event):
        if not self.is_sizing:
            return
        if 'e' in tag_name:
            width = max(0, self.old_width + (event.x - self.start_x))
            self.place_configure(width=width)
        if 'w' in tag_name:
            width = max(0, self.old_width + (self.start_root_x - event.x_root))
            to_x = event.x - self.start_x + int(self.place_info()['x'])
            self.place_configure(width=width, x=to_x)
        if 's' in tag_name:
            height = max(0, self.old_height + (event.y - self.start_y))
            self.place_configure(height=height)
        if 'n' in tag_name:
            height = max(0, self.old_height + (self.start_root_y - event.y_root))
            to_y = event.y - self.start_y + int(self.place_info()['y'])
            self.place_configure(height=height, y=to_y)
        self.after_idle(self.show)

    def on_mouse_release(self, tag_name, event):
        self.is_sizing = False
        if self.on_resize_complete is not None:
            self.on_resize_complete()
        self["cursor"] = "arrow"

    def mouse_down(self, event):
        self.widget.focus_set()
        self.__startx = event.x
        self.__starty = event.y

    def drag(self, event):
        self.place(x=self.winfo_x() + (event.x - self.__startx), y=self.winfo_y() + (event.y - self.__starty))

    def default_palette(self):
        self.palette_light()

    def palette_light(self):
        self.palette(
            {
                "designer_frame": {
                    "border": "gray",
                    "grip": "gray"
                }
            }
        )

    def palette_dark(self):
        self.palette(
            {
                "designer_frame": {
                    "border": "gray",
                    "grip": "gray"
                }
            }
        )

    def palette(self, dict=None):
        if dict is not None:
            if "designer_frame" in dict:
                self.frame_grip = dict["designer_frame"]["grip"]
                self.frame_border = dict["designer_frame"]["border"]

            self._palette = dict

            self._frame_grip = self.frame_grip
            self._frame_border = self.frame_border

            try:
                self._draw()
            except AttributeError:
                pass
        else:
            return self._palette


if __name__ == '__main__':
    from tkadw import Adwite, AdwTButton

    root = Adwite()
    root.geometry('500x500')

    frame = AdwDesignerFrame(root, AdwTButton, text="可拖拽缩放按钮")
    frame.place(x=50, y=50, width=100, height=100)
    frame.update()

    frame2 = AdwDesignerFrame(root, AdwTButton, text="可拖拽缩放按钮")
    frame2.palette(
        {
            "designer_frame": {
                "border": "red",
                "grip": "blue"
            }
        }
    )
    frame2.place(x=50, y=200, width=100, height=100)
    frame2.update()

    root.mainloop()

from tkinter import Event, Widget, Tk, Frame


x, y = 0, 0


def click(event: Event):
    global x, y
    x, y = event.x, event.y


def move(event: Event, widget: Widget, window: Tk):
    global x, y
    new_x = (event.x - x) + window.winfo_x()
    new_y = (event.y - y) + window.winfo_y()
    if new_y <= 0:
        new_y = 0
    window.geometry(f"+{new_x}+{new_y}")


def bind_move(widget: Widget, window: Tk):
    widget.bind("<Button-1>", click)
    widget.bind("<B1-Motion>", lambda event: move(event, widget, window))


def tag_bind_move(widget: Widget, tag, window: Tk):
    widget.tag_bind(tag, "<Button-1>", click)
    widget.tag_bind(tag, "<B1-Motion>", lambda event: move(event, widget, window))


class DragArea(object):
    def __init__(self, widget: Widget = Frame, master: Widget = None, window: Tk = None, *args, **kwargs):
        self._widget = widget(master, args, **kwargs)

        if window is None:
            from tkinter import _default_root

            window: widget = _default_root

        bind_move(self._widget, window)

        if hasattr(self._widget, "children"):
            for index in self._widget.children:
                try:
                    bind_move(index, window)
                except:
                    tag_bind_move(self._widget, index, window)

        if hasattr(self._widget, "frame"):
            bind_move(self._widget.frame, window)

        if hasattr(self._widget, "frame_f"):
            tag_bind_move(self._widget, self._widget.frame_f, window)

        if hasattr(self._widget, "frame_frame"):
            tag_bind_move(self._widget, self._widget.frame_f, window)

    @property
    def widget(self) -> Widget:
        return self._widget


if __name__ == '__main__':
    from tkadw import Adwite, AdwTFrame, AdwTButton

    root = Adwite(default_theme="win11")
    root.geometry("200x250")
    root.titlebar(False)

    area = DragArea(AdwTFrame, root, root, height=40)
    area.widget.pack(fill="x", side="top")

    button = AdwTButton(area.widget, text="X", height=30, width=30, command=lambda: root.quit())
    button.pack(fill="y", side="right", padx=3, pady=3)

    root.mainloop()
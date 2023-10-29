from tkinter import Widget
from _tkinter import TclError


def put_configure(widget: Widget, x=0, y=0, width=0, height=0, top=None, bottom=None, left=None, right=None):
    def configure(evt):
        if top is not None:
            y = top
        if left is not None:
            x = left
        if right is not None:
            width = widget.master.winfo_width() - x - right
        if bottom is not None:
            height = widget.master.winfo_height() -y -bottom
        widget.place(x=x, y=y, width=width, height=height)
    configure(None)
    return widget.master.bind("<Configure>", configure, add="+"), widget.bind("<Configure>", configure, add="+"), \
        {"in": widget.place_info()["in"], "x": x, "y": y, "width": width, "height": height, "top": top, "bottom": bottom, "left": left, "right": right}


def put_forget(widget: Widget, putid):
    """
Exception in Tkinter callback
Traceback (most recent call last):
  File "C:\Python311\Lib\tkinter\__init__.py", line 1948, in __call__
    return self.func(*args)
           ^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\tkinter\__init__.py", line 2369, in destroy
    Misc.destroy(self)
  File "C:\Python311\Lib\tkinter\__init__.py", line 687, in destroy
    self.tk.deletecommand(name)
_tkinter.TclError: can't delete Tcl command

进程已结束,退出代码0
    """
    widget.place_forget()
    widget.unbind("<Configure>", putid)


class AdwLayoutPut:
    def put_configure(self, *args, **kwargs):
        r = put_configure(self, *args, **kwargs)
        self.putid = r[0]
        self.putid2 = r[1]
        self.putinfo = r[2]

    put = put_configure

    def put_forget(self):
        return put_forget(self, self.putid), put_forget(self, self.putid2)

    def put_info(self):
        return self.putinfo


if __name__ == "__main__":
    from tkadw import Adwite, AdwTButton

    class TestButton(AdwTButton):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, command=self.put_forget, **kwargs)

    root = Adwite()
    btn1 = TestButton(root, text="1", width=40, height=40)
    btn1.put(left=5, right=45, top=5, bottom=45)
    btn2 = TestButton(root, text="2", width=40, height=40)
    btn2.put(left=45, right=5, top=45, bottom=5)
    print(btn1.place_info())
    print(btn1.put_info())
    root.mainloop()
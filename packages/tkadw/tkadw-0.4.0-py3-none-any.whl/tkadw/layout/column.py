from tkinter import Pack

START = "start"
END = "end"


def column_configure(widget: Pack, fill="both", expand="yes", anchor="center", padx=0, pady=0, ipadx=0, ipady=0):
    widget.pack(side="left", fill=fill, expand=expand, anchor=anchor,
                padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)


class AdwLayoutColumn:
    def column_configure(self, *args, **kwargs):
        column_configure(self, *args, **kwargs)

    column = column_configure

    def column_forget(self):
        self.pack_forget()

    def column_info(self):
        return self.pack_info()


if __name__ == '__main__':
    from tkadw import Adwite, AdwTButton

    class TestButton(AdwTButton):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, command=self.destroy, **kwargs)

    root = Adwite()
    for index in range(5):
        w = TestButton(root, text=index, width=40, height=40)
        w.column(padx=5, pady=5)
        print(w.column_info())
    root.mainloop()
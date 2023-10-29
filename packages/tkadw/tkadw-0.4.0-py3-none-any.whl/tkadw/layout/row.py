from tkinter import Pack

START = "start"
END = "end"


def row_configure(widget: Pack, fill="both", expand="yes", anchor="center", padx=0, pady=0, ipadx=0, ipady=0):
    widget.pack(side="top", fill=fill, expand=expand, anchor=anchor,
                padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)


class AdwLayoutRow:
    def row_configure(self, *args, **kwargs):
        row_configure(self, *args, **kwargs)

    row = row_configure

    def row_forget(self):
        self.pack_forget()

    def row_info(self):
        return self.pack_info()


if __name__ == '__main__':
    from tkadw import Adwite, AdwTButton

    class TestButton(AdwTButton):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, command=self.destroy, **kwargs)

    root = Adwite()
    for index in range(5):
        TestButton(root, text=index, width=40, height=40).row(padx=5, pady=5)
    root.mainloop()
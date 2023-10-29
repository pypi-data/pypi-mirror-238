from tkadw.windows.theme import AdwTButton, AdwTFrame, AdwTLabel, Adwite
from sys import platform


class AdwCustomTk(Adwite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frameless()
        self.build()
        
        self.x, self.y = 0, 0

    def frameless(self):
        self.wm_overrideredirect(True)

        try:
            from ctypes import windll
            GWL_EXSTYLE = -20
            WS_EX_APPWINDOW = 0x00040000
            WS_EX_TOOLWINDOW = 0x00000080
            hwnd = windll.user32.GetParent(self.winfo_id())
            style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style = style & ~WS_EX_TOOLWINDOW
            style = style | WS_EX_APPWINDOW
            res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        except:
            self.wm_attributes("-topmost", True)

        self.minsize(150, 180)

    def build(self):
        self.frame_border = AdwTFrame(self)
        self.frame_border.pack(fill="both", expand=True, padx=3, pady=3)

        self.frame_title = AdwTFrame(self.frame_border.frame, borderwidth=0)

        self.frame_title.pack(fill="x", side="top", padx=2, pady=2)
        self.bind_move(self.frame_title.frame)

        self.label_title = AdwTLabel(self.frame_title.frame, text=self.wm_title())
        self.label_title.pack(side="left", anchor="w", padx=10, pady=5)
        self.bind_move(self.label_title)

        self.maximized = False

        self.button_close = AdwTButton(self.frame_title.frame, text="✕", width=30, height=30, command=lambda: self.destroy())
        self.button_close.pack(side="right", anchor="e", padx=5, pady=5)

        self.button_minimize = AdwTButton(self.frame_title.frame, text="–", width=30, height=30, command=lambda: self.minimize())
        self.button_minimize.pack(side="right", anchor="e", padx=5, pady=5)

    def minimize(self):
        try:
            from ctypes import windll
            hwnd = windll.user32.GetParent(self.winfo_id())
            windll.user32.ShowWindow(hwnd, 2)
        except:
            pass

    def bind_move(self, widget):
        widget.bind("<Button-1>", self._click)
        widget.bind("<B1-Motion>", self._move)

    def create_sizegrip(self):
        from tkinter import ttk
        ttk.Style().configure("CTkCustom.TSizegrip", background="#ffffff")
        self.sizegrip = ttk.Sizegrip(self.frame_border, style="CTkCustom.TSizegrip")
        self.sizegrip.pack(side="bottom", anchor="se", padx=5, pady=5, ipady=2)
        return self.sizegrip

    @property
    def titlebar(self):
        return self.frame_title

    @property
    def titlebar_title(self):
        return self.label_title

    @property
    def titlebar_closebutton(self):
        return self.button_close

    @property
    def mainframe(self):
        return self.frame_border

    def _click(self, event):
        self.x, self.y = event.x, event.y

    def _move(self, event):
        new_x = (event.x - self.x) + self.winfo_x()
        new_y = (event.y - self.y) + self.winfo_y()
        if new_y <= 0:
            new_y = 0
        s = f"+{new_x}+{new_y}"
        self.geometry(s)


class AdwCustomSVTTk(AdwCustomTk):
    def build(self):
        from sv_ttk import use_dark_theme
        use_dark_theme()
        self.frame_border = ttk.Frame(self, style="Card.TFrame")
        self.frame_border.pack(fill="both", expand=True, padx=3, pady=3)

        self.frame_title = ttk.Frame(self.frame_border, borderwidth=0)
        self.frame_title.pack(fill="x", side="top", padx=2, pady=2)
        self.bind_move(self.frame_title)

        self.label_title = ttk.Label(self.frame_title, text=self.wm_title())
        self.label_title.pack(side="left", anchor="w", padx=10, pady=5)
        self.bind_move(self.label_title)

        self.maximized = False

        self.button_close = ttk.Button(self.frame_title, text="✕", command=lambda: self.destroy())
        self.button_close.pack(side="right", anchor="e", padx=5, pady=5)

        self.button_minimize = ttk.Button(self.frame_title, text="–", command=lambda: self.minimize())
        self.button_minimize.pack(side="right", anchor="e", padx=5, pady=5)

    def create_sizegrip(self):
        self.sizegrip = ttk.Sizegrip(self.frame_border)
        self.sizegrip.pack(side="bottom", anchor="se", padx=5, pady=5, ipady=2)
        return self.sizegrip


if __name__ == '__main__':
    root = AdwCustomTk()
    root.create_sizegrip()
    root.mainloop()
from tkadw.windows.canvas.entry import AdwDrawEntry


class FluentEntry(AdwDrawEntry):
    def __init__(self, *args, width=160, height=50, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        try:
            from tkextrafont import Font
            import os.path
            self.entry_text_font = Font(
                family="General Sans")
        except:
            from tkinter.font import families
            if "General Sans" in families():
                from tkinter.font import Font, names
                self.entry_text_font = Font(
                    family="General Sans")
        self.entry_text_font.configure(size=13)

    def _draw(self, evt):
        super()._draw(evt)

        self.create_gradient_v_rectangle(0,
                                         0,
                                         self._entry_border_width,
                                         self.winfo_height() / 2,
                                         "gradient_border_left_1",
                                         self._entry_border, self.entry_border2)

        self.create_gradient_v_rectangle(0,
                                         self.winfo_height() / 2,
                                         self._entry_border_width,
                                         self.winfo_height() / 2,
                                         "gradient_border_left_2",
                                         self.entry_border2, self._entry_border)

        self.create_gradient_v_rectangle(self.winfo_width()-self._entry_border_width,
                                         0,
                                         self._entry_border_width,
                                         self.winfo_height() / 2,
                                         "gradient_border_right_1",
                                         self._entry_border, self.entry_border2)

        self.create_gradient_v_rectangle(self.winfo_width()-self._entry_border_width,
                                         self.winfo_height() / 2,
                                         self._entry_border_width,
                                         self.winfo_height() / 2,
                                         "gradient_border_right_2",
                                         self.entry_border2, self._entry_border)

    def default_palette(self):
        self.palette_light()

    def palette_dark(self):
        self.palette(
            {
                "entry": {
                    "padding": (6, 6),

                    "back": "#080808",
                    "border": "#111111",
                    "border2": "#5f5f5f",
                    "text_back": "#cfcfcf",
                    "border_width": 2,

                    "bottom_line": "#0099bc",
                    "bottom_width": 0,

                    "focusin": {
                        "back": "#0D0D0D",
                        "border": "#111111",
                        "text_back": "#cfcfcf",
                        "border_width": 2,

                        "bottom_line": "#3bb1cc",
                        "bottom_width": 2,
                    }
                },
            }
        )

    def palette_light(self):
        self.palette(
            {
                "entry": {
                    "padding": (6, 6),

                    "back": "#f7f7f7",
                    "border": "#dbdbdb",
                    "border2": "#7e7e7e",
                    "text_back": "#000000",
                    "border_width": 2,

                    "bottom_line": "#0099bc",
                    "bottom_width": 0,

                    "focusin": {
                        "back": "#ececec",
                        "border": "#dbdbdb",
                        "text_back": "#000000",
                        "border_width": 2,

                        "bottom_line": "#3bb1cc",
                        "bottom_width": 2,
                    }
                },
            }
        )

    def palette(self, dict=None):
        super().palette(dict)
        if "entry" in dict:
            self.entry_border2 = dict["entry"]["border2"]


class FluentDarkEntry(FluentEntry):
    def default_palette(self):
        self.palette_dark()


if __name__ == '__main__':
    from tkadw import Adw

    root = Adw()
    entry = FluentEntry()
    entry.pack(fill="both", expand="yes", padx=15, pady=15)
    root.mainloop()
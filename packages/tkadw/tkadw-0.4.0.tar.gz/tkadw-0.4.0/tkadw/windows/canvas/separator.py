from tkadw.windows.canvas.widget import AdwWidget


class AdwDrawBasicSeparator(AdwWidget):
    def __init__(self, *args, width=50, height=3, **kwargs):
        super().__init__(*args, width=width, height=height, highlightthickness=0, **kwargs)

        self.default_palette()

        self._draw(None)

    def _draw(self, evt=None):
        self.delete("all")

        self.separator = self.create_line(
            self.separator_border_width,
            self.winfo_height()/2,
            self.winfo_width()-self.separator_border_width,
            self.winfo_height() / 2,
            width=self.separator_border_width,
            fill=self.separator_back,
        )

        if self.separator_rounded:
            self.itemconfigure(self.separator, capstyle="round", joinstyle="round", smooth=True)

    def default_palette(self):
        self.palette_light()

    def palette_light(self):
        self.palette(
            {
                "separator": {
                    "back": "gray15",
                    "border_width": 1,

                    "rounded": True
                }
            }
        )

    def palette_dark(self):
        self.palette(
            {
                "separator": {
                    "back": "gray85",
                    "border_width": 1,

                    "rounded": True
                }
            }
        )

    def palette(self, dict=None):
        if dict is not None:
            if "separator" in dict:
                self.separator_back = dict["separator"]["back"]
                self.separator_border_width = dict["separator"]["border_width"]

                self.separator_rounded = dict["separator"]["rounded"]

            self._palette = dict

            try:
                self._draw(None)
            except AttributeError:
                pass
        else:
            return self._palette


class AdwDrawSeparator(AdwDrawBasicSeparator):
    def default_palette(self):
        self.palette_light()


class AdwDrawDarkSeparator(AdwDrawBasicSeparator):
    def default_palette(self):
        self.palette_dark()


if __name__ == '__main__':
    from tkadw import Adw
    root = Adw()
    separator = AdwDrawSeparator()
    separator.pack(fill="both", expand="yes")
    separator = AdwDrawDarkSeparator()
    separator.pack(fill="both", expand="yes")
    root.mainloop()
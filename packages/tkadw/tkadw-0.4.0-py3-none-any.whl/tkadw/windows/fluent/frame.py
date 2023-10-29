from tkadw.windows.canvas.frame import AdwDrawFrame


class FluentFrame(AdwDrawFrame):
    def default_palette(self):
        self.palette_light()

    def palette_light(self):
        self.palette(
            {
                "frame": {
                    "back": "#f8f8f8",
                    "border": "#dbdbdb",
                    "border_width": 2,
                }
            }
        )

    def palette_dark(self):
        self.palette(
            {
                "frame": {
                    "back": "#050505",
                    "border": "#111111",
                    "border_width": 2,
                }
            }
        )


class FluentDarkFrame(FluentFrame):
    def default_palette(self):
        self.palette_dark()


if __name__ == '__main__':
    from tkadw import Adw

    root = Adw()
    frame = FluentFrame()
    frame.pack(fill="both", expand="yes")
    root.mainloop()
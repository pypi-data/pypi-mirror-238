from tkadw.windows.canvas.widget import AdwWidget


# Frame
class AdwDrawBasicScrollBar(AdwWidget):
    def __init__(self, *args, width=200, height=200, **kwargs):
        super().__init__(*args, width=width, height=height, bd=0, highlightthickness=0, **kwargs)

        self.default_palette()

        self._draw(None)

    def _draw(self, evt):
        self.delete("all")

        # 绘制框架边框
        self.frame_frame = self.create_rectangle(
            0, 0, self.winfo_width(), self.winfo_height(),
            width=self.frame_border_width,
            outline=self.frame_border, fill=self.frame_back,
        )

        self.frame.configure(background=self.frame_back, bd=0, )


    def default_palette(self):
        self.palette_light()

    def palette_light(self):
        self.palette(
            {
                "frame": {
                    "back": "#ffffff",
                    "border": "#eaeaea",
                    "border_width": 2,
                    "padding": 0
                }
            }
        )

    def palette_dark(self):
        self.palette(
            {
                "frame": {
                    "back": "#0f0f0f",
                    "border": "#333333",
                    "border_width": 2,
                    "padding": 0
                }
            }
        )

    def palette(self, dict=None):
        if dict is not None:
            if "frame" in dict:
                self.frame_back = dict["frame"]["back"]
                self.frame_border = dict["frame"]["border"]
                self.frame_border_width = dict["frame"]["border_width"]
                self.frame_padding = dict["frame"]["padding"]

            self._palette = dict

            try:
                self._draw(None)
            except AttributeError:
                pass
        else:
            return self._palette
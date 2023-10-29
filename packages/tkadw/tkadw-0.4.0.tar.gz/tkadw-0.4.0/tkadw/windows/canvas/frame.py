from tkadw.windows.canvas.widget import AdwWidget
from tkinter import Frame


# Frame
class AdwDrawBasicFrame(AdwWidget):
    def __init__(self, *args, width=200, height=200, **kwargs):
        super().__init__(*args, width=width, height=height, bd=0, highlightthickness=0, **kwargs)

        self.default_palette()

        self.frame = Frame(self)

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

        # 绘制框架区域
        self.frame_f = self.create_window(
            self.winfo_width() / 2, self.winfo_height() / 2,
            window=self.frame,
            width=self.winfo_width() - 6 - self.frame_border_width - self.frame_padding,
            height=self.winfo_height() - 6 - self.frame_border_width - self.frame_padding,
        )

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


class AdwDrawFrame(AdwDrawBasicFrame):
    def default_palette(self):
        self.palette_light()


class AdwDrawDarkFrame(AdwDrawBasicFrame):
    def default_palette(self):
        self.palette_dark()


class AdwDrawBasicRoundFrame(AdwDrawBasicFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.configure(background=self.master.cget("background"))
        except:
            pass

    def _draw(self, evt):
        self.delete("all")

        # 绘制框架边框
        self.frame_frame = self.create_round_rect2(
            self.frame_border_width, self.frame_border_width,
            self.winfo_width() - self.frame_border_width, self.winfo_height() - self.frame_border_width,
            self.frame_radius,
            width=self.frame_border_width,
            outline=self.frame_border, fill=self.frame_back,
        )

        self.frame.configure(background=self.frame_back, bd=0, )

        # 绘制框架区域
        self.frame_f = self.create_window(
            self.winfo_width() / 2, self.winfo_height() / 2,
            window=self.frame,
            width=self.winfo_width() - 6 - self.frame_border_width - self.frame_padding,
            height=self.winfo_height() - 6 - self.frame_border_width - self.frame_padding,
        )

    def default_palette(self):
        self.palette_light()

    def palette_light(self):
        self.palette(
            {
                "frame": {
                    "radius": 6,
                    "back": "#0f0f0f",
                    "border": "#333333",
                    "border_width": 2,
                    "padding": 0
                }
            }
        )

    def palette_dark(self):
        self.palette(
            {
                "frame": {
                    "radius": 6,
                    "back": "#0f0f0f",
                    "border": "#333333",
                    "border_width": 2,
                    "padding": 0
                }
            }
        )

    def palette(self, dict=None):
        super().palette(dict)
        if dict is not None:
            if "frame" in dict:
                self.frame_radius = dict["frame"]["radius"]
        if dict is None:
            return self._palette


class AdwDrawRoundFrame(AdwDrawBasicRoundFrame):
    def default_palette(self):
        self.palette_light()


class AdwDrawDarkRoundFrame(AdwDrawBasicRoundFrame):
    def default_palette(self):
        self.palette_dark()


class AdwDrawBasicRoundFrame3(AdwDrawBasicRoundFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.configure(background=self.master.cget("background"))
        except:
            pass

    def _draw(self, evt):
        self.delete("all")

        # 绘制框架边框
        self.create_round_rect4(
            self.frame_border_width, self.frame_border_width,
            self.winfo_width() - self.frame_border_width,
            self.winfo_height() - self.frame_border_width,
            self.frame_radius,
            width=self.frame_border_width,
            outline=self.frame_border, fill=self.frame_back,
        )

        self.entry_frame = "button_frame"

        self.frame.configure(background=self.frame_back, bd=0, )

        # 绘制框架区域
        self.frame_f = self.create_window(
            self.winfo_width() / 2, self.winfo_height() / 2,
            window=self.frame,
            width=self.winfo_width() - 6 - self.frame_border_width - self.frame_padding,
            height=self.winfo_height() - 6 - self.frame_border_width - self.frame_padding,
        )

    def default_palette(self):
        self.palette_light()


class AdwDrawRoundFrame3(AdwDrawBasicRoundFrame3):
    def default_palette(self):
        self.palette_light()


class AdwDrawDarkRoundFrame3(AdwDrawBasicRoundFrame3):
    def default_palette(self):
        self.palette_dark()


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()

    frame = AdwDrawDarkFrame()
    frame.pack(fill="both", expand="yes", )

    frame2 = AdwDrawDarkFrame(frame.frame)
    frame2.pack(fill="both", expand="yes", padx=8, pady=8)

    frame3 = AdwDrawDarkRoundFrame()
    frame3.pack(fill="both", expand="yes", )

    frame4 = AdwDrawDarkRoundFrame(frame3.frame)
    frame4.pack(fill="both", expand="yes", padx=8, pady=8)

    frame5 = AdwDrawDarkRoundFrame3()
    frame5.pack(fill="both", expand="yes", )

    frame6 = AdwDrawDarkRoundFrame3(frame5.frame)
    frame6.pack(fill="both", expand="yes", padx=8, pady=8)

    root.mainloop()

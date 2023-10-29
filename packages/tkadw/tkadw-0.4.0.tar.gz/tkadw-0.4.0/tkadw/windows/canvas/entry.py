from tkinter.font import Font, nametofont
from tkadw.windows.canvas.widget import AdwWidget


# Entry
class AdwDrawBasicEntry(AdwWidget):
    def __init__(self, *args, width=120, height=40, animated=5, text: str = "",
                 show: str = None, **kwargs):

        super().__init__(*args, width=width, height=height, highlightthickness=0, **kwargs)

        from tkinter import StringVar, Entry

        self.var = StringVar()
        self.var.set(text)

        self.entry_text_font = nametofont("TkDefaultFont")

        self.entry = Entry(
            self, bd=0, textvariable=self.var, highlightthickness=0, font=self.entry_text_font,
            show=show
        )

        self.default_palette()

        self.text: str = text

        self._entry_back = self.entry_back
        self._entry_border = self.entry_border
        self._entry_text_back = self.entry_text_back
        self._entry_border_width = self.entry_border_width
        self._entry_bottom_line = self.entry_bottom_line
        self._entry_bottom_width = self.entry_bottom_width

        self.bind("<Button>", self._click, add="+")
        self.bind("<Enter>", self._hover, add="+")
        self.bind("<Leave>", self._hover_release, add="+")
        # self.bind("<FocusIn>", self._focus, add="+")
        self.entry.bind("<FocusIn>", self._focus, add="+")
        # self.bind("<FocusOut>", self._focusout, add="+")
        self.entry.bind("<FocusOut>", self._focusout, add="+")

        self._draw(None)

    def set(self, text: str):
        self.var.set(text)

    def get(self):
        return self.var.get()

    def _draw(self, evt=None):
        self.delete("all")

        self.entry.configure(font=self.entry_text_font)

        # 绘制输入框边框
        self.entry_frame = self.create_rectangle(
            0, 0, self.winfo_width() - 1, self.winfo_height() - 1,
            width=self._entry_border_width,
            outline=self._entry_border, fill=self._entry_back,
        )

        # 绘制输入框输入区域
        self.entry_text = self.create_window(
            self.winfo_width() / 2, self.winfo_height() / 2,
            width=self.winfo_width() - self._entry_border_width - 5 - self.entry_padding[0],
            height=self.winfo_height() - self._entry_border_width - 5 - self.entry_padding[1],
            window=self.entry
        )

        # 绘制输入框美化效果
        from _tkinter import TclError
        try:
            self.entry_bottom = self.create_rectangle(self._entry_border_width,
                                                      self.winfo_height() - self._entry_bottom_width - self._entry_border_width,
                                                      self.winfo_width() - self._entry_border_width,
                                                      self.winfo_height() - self._entry_border_width,
                                                      fill=self._entry_bottom_line, outline=self._entry_bottom_line,
                                                      width=0)
        except TclError:
            pass

        if self._entry_bottom_width == 0:
            self.delete(self.entry_bottom)

        self.tag_raise(self.entry_bottom, self.entry_text)

        self.entry.configure(background=self._entry_back, foreground=self._entry_text_back,
                             insertbackground=self._entry_text_back)

    def _focus(self, evt=None):
        self._entry_back = self.entry_focusin_back
        self._entry_border = self.entry_focusin_border
        self._entry_border_width = self.entry_focusin_border_width
        self._entry_text_back = self.entry_focusin_text_back

        self._entry_bottom_line = self.entry_focusin_bottom_line
        self._entry_bottom_width = self.entry_focusin_bottom_width

        self._draw(None)

    def _focusout(self, evt=None):
        self._entry_back = self.entry_back
        self._entry_border = self.entry_border
        self._entry_border_width = self.entry_border_width
        self._entry_text_back = self.entry_text_back
        self._entry_bottom_line = self.entry_bottom_line
        self._entry_bottom_width = self.entry_bottom_width

        self._draw(None)

    def _click(self, evt=None):
        self.focus_set()

    def _hover(self, evt=None):
        self.hover = True

    def _hover_release(self, evt=None):
        if not self.focus_get():
            self.hover = False
            self._entry_back = self.entry_back
            self._entry_border = self.entry_border
            self._entry_border_width = self.entry_border_width
            self._entry_text_back = self.entry_text_back
            self._entry_bottom_line = self.entry_bottom_line
            self._entry_bottom_width = self.entry_bottom_width

            self._draw(None)

    def font(self, font: Font = None):
        if font is None:
            return self.entry_text_font
        else:
            self.entry_text_font = font

    def default_palette(self):
        self.palette_light()

    def palette_light(self):
        self.palette(
            {
                "entry": {
                    "padding": (3, 4),

                    "back": "#fdfdfd",
                    "border": "#eaeaea",
                    "text_back": "#5f5f5f",
                    "border_width": 1,

                    "bottom_line": "#eaeaea",
                    "bottom_width": 0,

                    "focusin": {
                        "back": "#f9f9f9",
                        "border": "#e2e2e2",
                        "text_back": "#1a1a1a",
                        "border_width": 1,

                        "bottom_line": "#185fb4",
                        "bottom_width": 2,
                    }
                },
            }
        )

    def palette_dark(self):
        self.palette(
            {
                "entry": {
                    "padding": (3, 4),

                    "back": "#353535",
                    "border": "#454545",
                    "text_back": "#cecece",
                    "border_width": 1,

                    "bottom_line": "#ffffff",
                    "bottom_width": 0,

                    "focusin": {
                        "back": "#2f2f2f",
                        "border": "#383838",
                        "text_back": "#ffffff",
                        "border_width": 1,

                        "bottom_line": "#4cc2ff",
                        "bottom_width": 2,
                    }
                },
            }
        )

    def palette(self, dict=None):
        if dict is not None:
            if "entry" in dict:
                self.entry_padding = dict["entry"]["padding"]

                self.entry_back = dict["entry"]["back"]
                self.entry_border = dict["entry"]["border"]
                self.entry_text_back = dict["entry"]["text_back"]
                self.entry_border_width = dict["entry"]["border_width"]

                self.entry_bottom_line = dict["entry"]["bottom_line"]
                self.entry_bottom_width = dict["entry"]["bottom_width"]

                if "focusin" in dict["entry"]:
                    self.entry_focusin_back = dict["entry"]["focusin"]["back"]
                    self.entry_focusin_border = dict["entry"]["focusin"]["border"]
                    self.entry_focusin_text_back = dict["entry"]["focusin"]["text_back"]
                    self.entry_focusin_border_width = dict["entry"]["focusin"]["border_width"]

                    self.entry_focusin_bottom_line = dict["entry"]["focusin"]["bottom_line"]
                    self.entry_focusin_bottom_width = dict["entry"]["focusin"]["bottom_width"]

            self._palette = dict

            self._entry_back = self.entry_back
            self._entry_border = self.entry_border
            self._entry_text_back = self.entry_text_back
            self._entry_border_width = self.entry_border_width
            self._entry_bottom_line = self.entry_bottom_line
            self._entry_bottom_width = self.entry_bottom_width

            try:
                self._draw(None)
            except AttributeError:
                pass
        else:
            return self._palette


class AdwDrawEntry(AdwDrawBasicEntry):
    def default_palette(self):
        self.palette_light()


class AdwDrawDarkEntry(AdwDrawBasicEntry):
    def default_palette(self):
        self.palette_dark()


# Rounded Entry
class AdwDrawBasicRoundEntry(AdwDrawBasicEntry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _other(self):
        if hasattr(self, "button_frame_back"):
            self.configure(background=self.button_frame_back, borderwidth=0)

    def border_radius(self, radius=None):
        if radius is None:
            return self.button_radius
        else:
            self.button_radius = radius

    def _draw(self, evt):
        self.delete("all")

        # 绘制输入框边框
        self.entry_frame = self.create_round_rect2(
            2, 2, self.winfo_width() - 3, self.winfo_height() - 3, self.entry_radius,
            width=self._entry_border_width,
            outline=self._entry_border, fill=self._entry_back,
        )

        # 绘制输入框输入区
        self.entry_text = self.create_window(
            self.winfo_width() / 2, self.winfo_height() / 2,
            width=self.winfo_width() - self._entry_border_width - 5 - self.entry_padding[0],
            height=self.winfo_height() - self._entry_border_width - 5 - self.entry_padding[1],
            window=self.entry
        )

        # 绘制输入框美化效果
        self.entry_bottom = self.create_rectangle(3 + self.entry_radius / 2,
                                                  self.winfo_height() - self._entry_bottom_width - 3,
                                                  self.winfo_width() - 3 - self.entry_radius / 2,
                                                  self.winfo_height() - 3.5,
                                                  fill=self._entry_bottom_line, outline=self._entry_bottom_line,
                                                  width=0)

        if self._entry_bottom_width == 0:
            self.delete(self.entry_bottom)

        self.tag_raise(self.entry_bottom, self.entry_text)

        self.entry.configure(background=self._entry_back, foreground=self._entry_text_back,
                             insertbackground=self._entry_text_back)

    def default_palette(self):
        self.palette_light()

    def palette_light(self):
        self.palette(
            {
                "entry": {
                    "radius": 6,
                    "padding": (3, 4),

                    "back": "#fdfdfd",
                    "border": "#eaeaea",
                    "text_back": "#5f5f5f",
                    "border_width": 1,

                    "bottom_line": "#eaeaea",
                    "bottom_width": 0,

                    "focusin": {
                        "back": "#f9f9f9",
                        "border": "#e2e2e2",
                        "text_back": "#1a1a1a",
                        "border_width": 1,

                        "bottom_line": "#185fb4",
                        "bottom_width": 2,
                    }
                },
            }
        )

    def palette_dark(self):
        self.palette(
            {
                "entry": {
                    "radius": 6,
                    "padding": (3, 4),

                    "back": "#353535",
                    "border": "#454545",
                    "text_back": "#cecece",
                    "border_width": 1,

                    "bottom_line": "#ffffff",
                    "bottom_width": 0,

                    "focusin": {
                        "back": "#2f2f2f",
                        "border": "#454545",
                        "text_back": "#ffffff",
                        "border_width": 1,

                        "bottom_line": "#4cc2ff",
                        "bottom_width": 2,
                    }
                },
            }
        )

    def palette(self, dict=None):
        super().palette(dict)
        if "entry" in dict:
            self.entry_radius = dict["entry"]["radius"]


class AdwDrawRoundEntry(AdwDrawBasicRoundEntry):
    def default_palette(self):
        self.palette_light()


class AdwDrawRoundDarkEntry(AdwDrawBasicRoundEntry):
    def default_palette(self):
        self.palette_dark()


class AdwDrawBasicRoundEntry3(AdwDrawBasicRoundEntry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _other(self):
        self.configure(background=self.master.cget("bg"), borderwidth=0)

    def border_radius(self, radius=None):
        if radius is None:
            return self.button_radius
        else:
            self.button_radius = radius

    def _draw(self, evt):
        self.delete("all")

        # 绘制输入框边框
        self.create_round_rect4(
            0,
            0,
            self.winfo_width() - 1,
            self.winfo_height() - 1,
            self.entry_radius,
            width=self._entry_border_width,
            outline=self._entry_border, fill=self._entry_back,
        )

        self.entry_frame = "button_frame"

        # 绘制输入框输入区域
        self.entry_text = self.create_window(
            self.winfo_width() / 2, self.winfo_height() / 2,
            width=self.winfo_width() - self._entry_border_width - self.entry_padding[0] - 2,
            height=self.winfo_height() - self._entry_border_width - self.entry_padding[1] - 2,
            window=self.entry
        )

        # 绘制输入框美化效果
        self.entry_bottom = self.create_rectangle(1 + self.entry_radius / 5,
                                                  self.winfo_height() - self._entry_bottom_width - 1,
                                                  self.winfo_width() - 1 - self.entry_radius / 5,
                                                  self.winfo_height() - 1,
                                                  fill=self._entry_bottom_line, outline=self._entry_bottom_line,
                                                  width=0)

        if self._entry_bottom_width == 0:
            self.delete(self.entry_bottom)

        self.tag_raise(self.entry_bottom, self.entry_text)

        self.entry.configure(background=self._entry_back, foreground=self._entry_text_back,
                             insertbackground=self._entry_text_back)

    def default_palette(self):
        self.palette_light()


class AdwDrawRoundEntry3(AdwDrawBasicRoundEntry3):
    def default_palette(self):
        self.palette_light()


class AdwDrawRoundDarkEntry3(AdwDrawBasicRoundEntry3):
    def default_palette(self):
        self.palette_dark()


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()

    entry1 = AdwDrawEntry(text="Hello")
    entry1.pack(fill="x", padx=5, pady=5)

    entry2 = AdwDrawDarkEntry(text="Hello")
    entry2.pack(fill="x", padx=5, pady=5)

    entry3 = AdwDrawRoundEntry(text="Hello")
    entry3.pack(fill="x", padx=5, pady=5)

    entry4 = AdwDrawRoundDarkEntry(text="Hello")
    entry4.pack(fill="x", padx=5, pady=5)

    entry5 = AdwDrawRoundEntry3(text="Hello")
    entry5.pack(fill="x", padx=5, pady=5)

    entry6 = AdwDrawRoundDarkEntry3(text="Hello")
    entry6.pack(fill="x", padx=5, pady=5)

    entry_pwd1 = AdwDrawEntry(text="Hello", show=">")
    entry_pwd1.pack(fill="x", padx=5, pady=5)

    root.mainloop()

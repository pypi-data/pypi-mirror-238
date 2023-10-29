from tkinter.font import Font, nametofont
from tkadw.windows.canvas.widget import AdwWidget


# Button
class AdwDrawBasicButton(AdwWidget):

    """
    自绘基础按钮
    """

    def __init__(self, *args, width=120, height=40, text: str = "", command=None, **kwargs):
        super().__init__(*args, width=width, height=height, bd=0, highlightthickness=0, **kwargs)

        self.default_palette()

        self.text = text

        self._button_back = self.button_back
        self._button_border = self.button_border
        self._button_border_width = self.button_border_width
        self._button_text_back = self.button_text_back

        self.button_text_font = nametofont("TkDefaultFont")

        # 绑定事件
        self.bind("<Button>", self._click, add="+")
        self.bind("<ButtonRelease>", self._unclick, add="+")
        self.bind("<Enter>", self._hover, add="+")
        self.bind("<Leave>", self._hover_release, add="+")

        # 绑定点击事件（不是按下）
        if command is not None:
            self.bind("<<Click>>", lambda event: command())

        self._draw(None)

    def configure(self, **kwargs):
        if "command" in kwargs:
            self.command = kwargs.pop("command")
            self.bind("<<Click>>", lambda event: self.command())
        elif "text" in kwargs:
            self.text = kwargs.pop("text")
            self._draw(None)
        else:
            super().configure(**kwargs)

    def update(self) -> None:
        """
        多执行一道绘制
        """
        super().update()
        self._draw(None)

    def _draw(self, evt=None):
        self.delete("all")

        # 绘制按钮边框
        self.button_frame = self.create_rectangle(
            self._button_border_width - 1, self._button_border_width - 1,
            self.winfo_width() - self._button_border_width + 1,
            self.winfo_height() - self._button_border_width + 1,
            width=self._button_border_width,
            outline=self._button_border, fill=self._button_back,
        )

        # 绘制按钮文本
        self.button_text = self.create_text(
            self.winfo_width() / 2, self.winfo_height() / 2,
            text=self.text, fill=self._button_text_back,
            font=self.button_text_font
        )

    def _click(self, evt=None):
        self.hover = True
        self._button_back = self.button_pressed_back
        self._button_border = self.button_pressed_border
        self._button_border_width = self.button_pressed_border_width
        self._button_text_back = self.button_pressed_text_back

        self.focus_set()

        self._draw(None)

    def _unclick(self, evt=None):
        if self.hover:
            self._button_back = self.button_active_back
            self._button_border = self.button_active_border
            self._button_border_width = self.button_active_border_width
            self._button_text_back = self.button_active_text_back

            self._draw(None)

            self.event_generate("<<Click>>")

    def _hover(self, evt=None):
        self.hover = True
        self._button_back = self.button_active_back
        self._button_border = self.button_active_border
        self._button_border_width = self.button_active_border_width
        self._button_text_back = self.button_active_text_back

        self._draw(None)

    def _hover_release(self, evt=None):
        self.hover = False
        self._button_back = self.button_back
        self._button_border = self.button_border
        self._button_border_width = self.button_border_width
        self._button_text_back = self.button_text_back

        self._draw(None)

    def font(self, font: Font = None):
        if font is None:
            return self.button_text_font
        else:
            self.button_text_font = font

    def default_palette(self):
        self.palette_light()

    def palette_light(self):
        self.palette(
            {
                "button": {
                    "back": "#fdfdfd",
                    "border": "#eaeaea",
                    "text_back": "#1a1a1a",
                    "border_width": 1,

                    "active": {
                        "back": "#f9f9f9",
                        "border": "#aaaaaa",
                        "text_back": "#5f5f5f",
                        "border_width": 1,
                    },

                    "pressed": {
                        "back": "#f9f9f9",
                        "border": "#e2e2e2",
                        "text_back": "#8a8a8a",
                        "border_width": 1,
                    },
                }
            }
        )

    def palette_dark(self):
        self.palette(
            {
                "button": {
                    "back": "#353535",
                    "border": "#454545",
                    "text_back": "#ffffff",
                    "border_width": 1,

                    "active": {
                        "back": "#3a3a3a",
                        "border": "#454545",
                        "text_back": "#cecece",
                        "border_width": 1,
                    },

                    "pressed": {
                        "back": "#2f2f2f",
                        "border": "#454545",
                        "text_back": "#9a9a9a",
                        "border_width": 1,
                    },
                }
            }
        )

    def palette(self, dict=None):
        if dict is not None:
            if "button" in dict:
                self.button_back = dict["button"]["back"]
                self.button_border = dict["button"]["border"]
                self.button_text_back = dict["button"]["text_back"]
                self.button_border_width = dict["button"]["border_width"]

                if "active" in dict["button"]:
                    self.button_active_back = dict["button"]["active"]["back"]
                    self.button_active_border = dict["button"]["active"]["border"]
                    self.button_active_text_back = dict["button"]["active"]["text_back"]
                    self.button_active_border_width = dict["button"]["active"]["border_width"]

                if "pressed" in dict["button"]:
                    self.button_pressed_back = dict["button"]["pressed"]["back"]
                    self.button_pressed_border = dict["button"]["pressed"]["border"]
                    self.button_pressed_text_back = dict["button"]["pressed"]["text_back"]
                    self.button_pressed_border_width = dict["button"]["pressed"]["border_width"]

            self._palette = dict

            self._button_back = self.button_back
            self._button_border = self.button_border
            self._button_border_width = self.button_border_width
            self._button_text_back = self.button_text_back

            try:
                self._draw(None)
            except AttributeError:
                pass
        else:
            return self._palette


class AdwDrawButton(AdwDrawBasicButton):
    def default_palette(self):
        self.palette_light()


class AdwDrawDarkButton(AdwDrawBasicButton):
    def default_palette(self):
        self.palette_dark()


class AdwDrawAccentButton(AdwDrawBasicButton):
    def default_palette(self):
        self.palette(
            {
                "button": {
                    "back": "#0067c0",
                    "border": "#1473c5",
                    "text_back": "#ffffff",
                    "border_width": 1,

                    "active": {
                        "back": "#1975c5",
                        "border": "#1473c5",
                        "text_back": "#ffffff",
                        "border_width": 1,
                    },

                    "pressed": {
                        "back": "#3284cb",
                        "border": "#3284cb",
                        "text_back": "#fdfdfd",
                        "border_width": 1,
                    },
                }
            }
        )


# Round Button
class AdwDrawBasicRoundButton(AdwDrawBasicButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _other(self):
        self.configure(background=self.master.cget("bg"), borderwidth=0)

    def _draw(self, evt):
        self.delete("all")

        # 绘制按钮边框
        self.button_frame = self.create_round_rect2(
            self._button_border_width - 1,
            self._button_border_width - 1,
            self.winfo_width() - self._button_border_width * 2 + 1,
            self.winfo_height() - self._button_border_width * 2 + 1, self.button_radius,
            width=self._button_border_width,
            outline=self._button_border, fill=self._button_back,
        )

        # 绘制按钮文本
        self.button_text = self.create_text(
            self.winfo_width() / 2, self.winfo_height() / 2,
            text=self.text, fill=self._button_text_back,
            font=self.button_text_font
        )

    def default_palette(self):
        self.palette_light()

    def palette_light(self):
        self.palette(
            {
                "button": {
                    "radius": 8,
                    "back": "#fdfdfd",
                    "border": "#eaeaea",
                    "text_back": "#1a1a1a",
                    "border_width": 1,

                    "active": {
                        "back": "#f9f9f9",
                        "border": "#454545",
                        "text_back": "#5f5f5f",
                        "border_width": 1,
                    },

                    "pressed": {
                        "back": "#f9f9f9",
                        "border": "#e2e2e2",
                        "text_back": "#8a8a8a",
                        "border_width": 1,
                    },
                }
            }
        )

    def palette_dark(self):
        self.palette(
            {
                "button": {
                    "radius": 8,
                    "back": "#353535",
                    "border": "#454545",
                    "text_back": "#ffffff",
                    "border_width": 1,

                    "active": {
                        "back": "#3a3a3a",
                        "border": "#454545",
                        "text_back": "#cecece",
                        "border_width": 1,
                    },

                    "pressed": {
                        "back": "#2f2f2f",
                        "border": "#454545",
                        "text_back": "#9a9a9a",
                        "border_width": 1,
                    },
                }
            }
        )

    def palette(self, dict=None):
        super().palette(dict)
        if "button" in dict:
            self.button_radius = dict["button"]["radius"]


class AdwDrawRoundButton(AdwDrawBasicRoundButton):
    def default_palette(self):
        self.palette_light()


class AdwDrawRoundAccentButton(AdwDrawBasicRoundButton):
    def default_palette(self):
        self.palette(
            {
                "button": {
                    "radius": 8,
                    "back": "#0067c0",
                    "border": "#1473c5",
                    "text_back": "#ffffff",
                    "border_width": 1,

                    "active": {
                        "back": "#1975c5",
                        "border": "#1473c5",
                        "text_back": "#ffffff",
                        "border_width": 1,
                    },

                    "pressed": {
                        "back": "#3284cb",
                        "border": "#3284cb",
                        "text_back": "#fdfdfd",
                        "border_width": 1,
                    },
                }
            }
        )


class AdwDrawRoundDarkButton(AdwDrawBasicRoundButton):
    def default_palette(self):
        self.palette_dark()


class AdwDrawRoundButton2(AdwDrawBasicRoundButton):
    # 使用此控件，不建议使用边框属性
    def _draw(self, evt):
        self.delete("all")

        # 绘制按钮文本
        self.create_round_rect3(
            "button_frame",
            self._button_border_width - 1,
            self._button_border_width - 1,
            self.winfo_width() - self._button_border_width * 2,
            self.winfo_height() - self._button_border_width * 2,
            self.button_radius,
            outline=self._button_border, fill=self._button_back,
        )

        self.button_frame = "button_frame"

        # 绘制按钮文本
        self.button_text = self.create_text(
            self.winfo_width() / 2, self.winfo_height() / 2,
            text=self.text, fill=self._button_text_back,
            font=self.button_text_font
        )

    def default_palette(self):
        self.palette_light()


class AdwDrawRoundAccentButton2(AdwDrawRoundButton2):
    def default_palette(self):
        self.palette(
            {
                "button": {
                    "radius": 8,
                    "back": "#0067c0",
                    "border": "#1473c5",
                    "text_back": "#ffffff",
                    "border_width": 1,

                    "active": {
                        "back": "#1975c5",
                        "border": "#1473c5",
                        "text_back": "#ffffff",
                        "border_width": 1,
                    },

                    "pressed": {
                        "back": "#3284cb",
                        "border": "#3284cb",
                        "text_back": "#fdfdfd",
                        "border_width": 1,
                    },
                }
            }
        )


class AdwDrawRoundDarkButton2(AdwDrawRoundButton2):
    def default_palette(self):
        self.palette_dark()


class AdwDrawRoundButton3(AdwDrawBasicRoundButton):
    def _draw(self, evt):
        self.delete("all")

        # 绘制按钮边框
        self.create_round_rect4(
            self._button_border_width - 1, self._button_border_width - 1,
            self.winfo_width() - self._button_border_width,
            self.winfo_height() - self._button_border_width,
            self.button_radius,
            width=self._button_border_width,
            outline=self._button_border, fill=self._button_back,
        )

        self.button_frame = "button_frame"

        # 绘制按钮文本
        self.button_text = self.create_text(
            self.winfo_width() / 2, self.winfo_height() / 2,
            text=self.text, fill=self._button_text_back,
            font=self.button_text_font
        )

    def default_palette(self):
        self.palette_light()


class AdwDrawRoundAccentButton3(AdwDrawRoundButton3):
    def default_palette(self):
        self.palette(
            {
                "button": {
                    "radius": 8,
                    "back": "#0067c0",
                    "border": "#1473c5",
                    "text_back": "#ffffff",
                    "border_width": 1,

                    "active": {
                        "back": "#1975c5",
                        "border": "#1473c5",
                        "text_back": "#ffffff",
                        "border_width": 1,
                    },

                    "pressed": {
                        "back": "#3284cb",
                        "border": "#3284cb",
                        "text_back": "#fdfdfd",
                        "border_width": 1,
                    },
                }
            }
        )


class AdwDrawRoundDarkButton3(AdwDrawRoundButton3):
    def default_palette(self):
        self.palette_dark()


# Circular Button
class AdwDrawBasicCircularButton(AdwDrawBasicButton):
    def __init__(self, *args, width=120, height=120, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

    def _draw(self, evt):
        self.delete("all")

        # 绘制按钮框架
        self.button_frame = self.create_oval(
            1.5, 1.5, self.winfo_width() - 3, self.winfo_height() - 3,
            width=self.button_border_width,
            outline=self._button_border, fill=self._button_back,
        )

        # 绘制按钮文本
        self.button_text = self.create_text(
            self.winfo_width() / 2, self.winfo_height() / 2,
            text=self.text, fill=self._button_text_back,
            font=self.button_text_font
        )

        def palette(self, dict=None):
            if dict is not None:
                if "circular_button" in dict:
                    self.button_back = dict["circular_button"]["back"]
                    self.button_border = dict["circular_button"]["border"]
                    self.button_text_back = dict["circular_button"]["text_back"]
                    self.button_border_width = dict["circular_button"]["border_width"]

                    if "active" in dict["circular_button"]:
                        self.button_active_back = dict["circular_button"]["active"]["back"]
                        self.button_active_border = dict["circular_button"]["active"]["border"]
                        self.button_active_text_back = dict["circular_button"]["active"]["text_back"]
                        self.button_active_border_width = dict["circular_button"]["active"]["border_width"]

                    if "pressed" in dict["circular_button"]:
                        self.button_pressed_back = dict["circular_button"]["pressed"]["back"]
                        self.button_pressed_border = dict["circular_button"]["pressed"]["border"]
                        self.button_pressed_text_back = dict["circular_button"]["pressed"]["text_back"]
                        self.button_pressed_border_width = dict["circular_button"]["pressed"]["border_width"]

                self._palette = dict

                self._button_back = self.button_back
                self._button_border = self.button_border
                self._button_border_width = self.button_border_width
                self._button_text_back = self.button_text_back

                try:
                    self._draw(None)
                except AttributeError:
                    pass
            else:
                return self._palette


class AdwDrawCircularButton(AdwDrawBasicCircularButton):
    def default_palette(self):
        self.palette_light()


class AdwDrawCircularDarkButton(AdwDrawBasicCircularButton):
    def default_palette(self):
        self.palette_dark()


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()

    button = AdwDrawButton(text="Hello")
    button.bind("<<Click>>", lambda evt: print("button clicked"))
    button.pack(fill="x", padx=5, pady=5)

    button4 = AdwDrawRoundButton(text="Hello")
    button4.bind("<<Click>>", lambda evt: print("button4 clicked"))
    button4.pack(fill="x", padx=5, pady=5)

    button7 = AdwDrawRoundButton2(text="Hello")
    button7.bind("<<Click>>", lambda evt: print("button4 clicked"))
    button7.pack(fill="x", padx=5, pady=5)

    button10 = AdwDrawRoundButton3(text="Hello")
    button10.bind("<<Click>>", lambda evt: print("button4 clicked"))
    button10.pack(fill="x", padx=5, pady=5)

    button13 = AdwDrawCircularButton(text="Hello")
    button13.bind("<<Click>>", lambda evt: print("button6 clicked"))
    button13.pack(fill="x", padx=5, pady=5)

    root.mainloop()

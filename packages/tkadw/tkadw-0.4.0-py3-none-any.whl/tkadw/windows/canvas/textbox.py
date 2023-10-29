from tkinter.font import Font, nametofont
from tkadw.windows.canvas.widget import AdwWidget


# Text
class AdwDrawBasicText(AdwWidget):
    def __init__(self, *args, text: str = "", width=120, height=80, **kwargs):

        super().__init__(*args, width=width, height=height, highlightthickness=0, **kwargs)

        from tkinter import Text

        self.text_text_font = nametofont("TkDefaultFont")

        self.text = Text(self, bd=0, font=self.text_text_font, undo=True, highlightthickness=0)

        self.text.insert("1.0", text)

        self._other()

        self.default_palette()

        self._text_back = self.text_back
        self._text_border = self.text_border
        self._text_text_back = self.text_text_back
        self._text_bottom_line = self.text_bottom_line
        self._text_bottom_width = self.text_bottom_width

        self.bind("<Configure>", self._draw, add="+")
        self.bind("<Button>", self._click, add="+")
        self.bind("<Enter>", self._hover, add="+")
        self.bind("<Leave>", self._hover_release, add="+")
        #self.bind("<FocusIn>", self._focus, add="+")
        self.text.bind("<FocusIn>", self._focus, add="+")
        #self.bind("<FocusOut>", self._focusout, add="+")
        self.text.bind("<FocusOut>", self._focusout, add="+")

        self.bind("<Control-z>", lambda event: self.undo(), add="+")
        self.bind("<Control-Z>", lambda event: self.undo(), add="+")
        self.bind("<Control-Shift-z>", lambda event: self.redo(), add="+")
        self.bind("<Control-Shift-Z>", lambda event: self.redo(), add="+")

        self.text.bind("<Control-z>", lambda event: self.undo(), add="+")
        self.text.bind("<Control-Z>", lambda event: self.undo(), add="+")
        self.text.bind("<Control-Shift-z>", lambda event: self.redo(), add="+")
        self.text.bind("<Control-Shift-Z>", lambda event: self.redo(), add="+")

        self._draw(None)

    def tbbox(self, *args, **kwargs):
        return self.text.bbox(*args, **kwargs)

    def compare(self, *args, **kwargs):
        return self.text.compare(*args, **kwargs)

    def count(self, *args, **kwargs):
        return self.text.count(*args, **kwargs)

    def debug(self, *args, **kwargs):
        return self.text.debug(*args, **kwargs)

    def tdelete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def dump(self, *args, **kwargs):
        return self.text.dump(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def tindex(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def tinsert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def search(self, *args, **kwargs):
        return self.text.search(*args, **kwargs)

    def see(self, *args, **kwargs):
        return self.text.see(*args, **kwargs)

    def undo(self):
        try:
            self.text.edit_undo()
        except:
            pass

    def redo(self):
        try:
            self.text.edit_redo()
        except:
            pass

    def _other(self):
        if hasattr(self, "button_frame_back"):
            self.configure(background=self.button_frame_back, borderwidth=0)

    def _draw(self, evt):
        self.delete("all")

        self.text_frame = self.create_rectangle(
            0, 0, self.winfo_width() - 1, self.winfo_height() - 1,
            width=self.text_border_width,
            outline=self._text_border, fill=self._text_back,
        )

        self.text_text = self.create_window(
            self.winfo_width() / 2, self.winfo_height() / 2,
            width=self.winfo_width() - self.text_border_width - 5 - self.text_padding[0],
            height=self.winfo_height() - self.text_border_width - 5 - self.text_padding[1],
            window=self.text
        )

        self.text_bottom = self.create_rectangle(1, self.winfo_height() - self._text_bottom_width - 1,
                                                 self.winfo_width() - 1, self.winfo_height() - 1,
                                                 fill=self._text_bottom_line, outline=self._text_bottom_line,
                                                 width=0)

        if self._text_bottom_width == 0:
            self.delete(self.text_bottom)

        self.tag_raise(self.text_bottom, self.text_text)

        self.text.configure(background=self._text_back, foreground=self._text_text_back, autoseparators=True, insertbackground=self._text_text_back)

    def _focus(self, evt=None):
        self._text_back = self.text_focusin_back
        self._text_border = self.text_focusin_border
        self._text_text_back = self.text_focusin_text_back
        self._text_bottom_line = self.text_focusin_bottom_line
        self._text_bottom_width = self.text_focusin_bottom_width

        self._draw(None)

    def _focusout(self, evt=None):
        self._text_back = self.text_back
        self._text_border = self.text_border
        self._text_text_back = self.text_text_back
        self._text_bottom_line = self.text_bottom_line
        self._text_bottom_width = self.text_bottom_width

        self._draw(None)

    def _click(self, evt=None):
        self.focus_set()

    def _hover(self, evt=None):
        self.hover = True

    def _hover_release(self, evt=None):
        if not self.focus_get():
            self.hover = False
            self._text_back = self.text_back
            self._text_border = self.text_border
            self._text_text_back = self.text_text_back
            self._text_bottom_line = self.text_bottom_line
            self._text_bottom_width = self.text_bottom_width

            self._draw(None)

    def font(self, font: Font = None):
        if font is None:
            return self.text_text_font
        else:
            self.text_text_font = font
        self.update()

    def default_palette(self):
        self.palette_light()

    def palette_light(self):
        self.palette(
            {
                "text": {
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
                "text": {
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
        if dict is not None:
            if "text" in dict:
                self.text_padding = dict["text"]["padding"]

                self.text_back = dict["text"]["back"]
                self.text_border = dict["text"]["border"]
                self.text_text_back = dict["text"]["text_back"]
                self.text_border_width = dict["text"]["border_width"]

                self.text_bottom_line = dict["text"]["bottom_line"]
                self.text_bottom_width = dict["text"]["bottom_width"]

                if "focusin" in dict["text"]:
                    self.text_focusin_back = dict["text"]["focusin"]["back"]
                    self.text_focusin_border = dict["text"]["focusin"]["border"]
                    self.text_focusin_text_back = dict["text"]["focusin"]["text_back"]
                    self.text_focusin_border_width = dict["text"]["focusin"]["border_width"]

                    self.text_focusin_bottom_line = dict["text"]["focusin"]["bottom_line"]
                    self.text_focusin_bottom_width = dict["text"]["focusin"]["bottom_width"]

            self._text_back = self.text_back
            self._text_border = self.text_border
            self._text_text_back = self.text_text_back
            self._text_bottom_line = self.text_bottom_line
            self._text_bottom_width = self.text_bottom_width

            self._palette = dict

            try:
                self._draw(None)
            except AttributeError:
                pass
        else:
            return self._palette


class AdwDrawText(AdwDrawBasicText):
    def default_palette(self):
        self.palette_light()


class AdwDrawDarkText(AdwDrawBasicText):
    def default_palette(self):
        self.palette_dark()


# Rounded text
class AdwDrawBasicRoundText(AdwDrawBasicText):
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

        self.text_frame = self.create_round_rect2(
            2, 2, self.winfo_width() - 3, self.winfo_height() - 3, self.text_radius,
            width=self.text_border_width,
            outline=self._text_border, fill=self._text_back,
        )

        self.text_text = self.create_window(
            self.winfo_width() / 2, self.winfo_height() / 2,
            width=self.winfo_width() - self.text_border_width - 5 - self.text_padding[0],
            height=self.winfo_height() - self.text_border_width - 5 - self.text_padding[1],
            window=self.text
        )

        self.text_bottom = self.create_rectangle(3 + self.text_radius / 2,
                                                 self.winfo_height() - self._text_bottom_width - 3,
                                                 self.winfo_width() - 3 - self.text_radius / 2,
                                                 self.winfo_height() - 3.5,
                                                 fill=self._text_bottom_line, outline=self._text_bottom_line,
                                                 width=0)

        if self._text_bottom_width == 0:
            self.delete(self.text_bottom)

        self.tag_raise(self.text_bottom, self.text_text)

        self.text.configure(background=self._text_back, foreground=self._text_text_back, insertbackground=self._text_text_back)

    def default_palette(self):
        self.palette_light()

    def palette_light(self):
        self.palette(
            {
                "text": {
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
                "text": {
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
        if "text" in dict:
            self.text_radius = dict["text"]["radius"]


class AdwDrawRoundText(AdwDrawBasicRoundText):
    def default_palette(self):
        self.palette_light()


class AdwDrawRoundDarkText(AdwDrawBasicRoundText):
    def default_palette(self):
        self.palette_dark()


class AdwDrawBasicRoundText3(AdwDrawBasicRoundText):
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

        self.create_round_rect4(
            0,
            0,
            self.winfo_width() - 1,
            self.winfo_height() - 1,
            self.text_radius,
            width=self.text_border_width,
            outline=self._text_border, fill=self._text_back,
        )

        self.text_frame = "button_frame"

        self.text_text = self.create_window(
            self.winfo_width() / 2, self.winfo_height() / 2,
            width=self.winfo_width() - self.text_border_width - self.text_padding[0] - 2,
            height=self.winfo_height() - self.text_border_width - self.text_padding[1] - 2,
            window=self.text
        )

        self.text_bottom = self.create_rectangle(1 + self.text_radius / 5,
                                                 self.winfo_height() - self._text_bottom_width - 1,
                                                 self.winfo_width() - 1 - self.text_radius / 5,
                                                 self.winfo_height() - 1,
                                                 fill=self._text_bottom_line, outline=self._text_bottom_line,
                                                 width=0)

        if self._text_bottom_width == 0:
            self.delete(self.text_bottom)

        self.tag_raise(self.text_bottom, self.text_text)

        self.text.configure(background=self._text_back, foreground=self._text_text_back, insertbackground=self._text_text_back)

    def default_palette(self):
        self.palette_light()

    def palette_light(self):
        self.palette(
            {
                "text": {
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
                "text": {
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


class AdwDrawRoundText3(AdwDrawBasicRoundText3):
    def default_palette(self):
        self.palette_light()


class AdwDrawRoundDarkText3(AdwDrawBasicRoundText3):
    def default_palette(self):
        self.palette_dark()


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()

    text1 = AdwDrawText()
    text1.pack(fill="x", padx=5, pady=5)

    text2 = AdwDrawDarkText()
    text2.pack(fill="x", padx=5, pady=5)

    text3 = AdwDrawRoundText()
    text3.pack(fill="x", padx=5, pady=5)

    text4 = AdwDrawRoundDarkText()
    text4.pack(fill="x", padx=5, pady=5)

    text5 = AdwDrawRoundText3()
    text5.pack(fill="x", padx=5, pady=5)

    text6 = AdwDrawRoundDarkText3()
    text6.pack(fill="x", padx=5, pady=5)

    root.mainloop()

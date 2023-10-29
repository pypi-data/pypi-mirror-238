from tkadw.windows.canvas.widget import AdwWidget


class AdwDrawBasicCheckBox(AdwWidget):
    def __init__(self, *args, width=30, height=30, **kwargs):
        super().__init__(*args, width=width, height=height, bd=0, highlightthickness=0, **kwargs)

        self.default_palette()

        self._checkbox_back = self.checkbox_back
        self._checkbox_border = self.checkbox_border
        self._checkbox_border_width = self.checkbox_border_width

        self.bind("<Button>", self._click, add="+")
        self.bind("<ButtonRelease>", self._unclick, add="+")
        self.bind("<Enter>", self._hover, add="+")
        self.bind("<Leave>", self._hover_release, add="+")

        self._draw(None)

    def _draw(self, evt):
        self.delete("all")

        self.checkbox_frame = self.create_rectangle(
            1.5, 1.5, self.winfo_width() - 3, self.winfo_height() - 3,
            width=self._checkbox_border_width,
            outline=self._checkbox_border, fill=self._checkbox_back,
        )

        self.checkbox_mark_line1 = self.create_line(self.winfo_x() + 5 + self.checkbox_mark_size,
                                                    self.winfo_y() + 10,
                                                    self.winfo_x() + 5 + self.checkbox_mark_size,
                                                    self.winfo_y() + 10 + self.checkbox_mark_size,
                                                    width=2, fill='black')

    def _click(self, evt=None):
        self.hover = True
        self._checkbox_back = self.checkbox_pressed_back
        self._checkbox_border = self.checkbox_pressed_border
        self._checkbox_border_width = self.checkbox_pressed_border_width

        self.focus_set()

        self._draw(None)

    def _unclick(self, evt=None):
        if self.hover:
            self._checkbox_back = self.checkbox_active_back
            self._checkbox_border = self.checkbox_active_border
            self._checkbox_border_width = self.checkbox_active_border_width

            self._draw(None)

            self.event_generate("<<Click>>")

    def _hover(self, evt=None):
        self.hover = True
        self._checkbox_back = self.checkbox_active_back
        self._checkbox_border = self.checkbox_active_border
        self._checkbox_border_width = self.checkbox_active_border_width

        self._draw(None)

    def _hover_release(self, evt=None):
        self.hover = False
        self._checkbox_back = self.checkbox_back
        self._checkbox_border = self.checkbox_border
        self._checkbox_border_width = self.checkbox_border_width

        self._draw(None)

    def default_palette(self):
        self.palette_light()

    def palette_light(self):
        self.palette(
            {
                "checkbox": {
                    "back": "#fdfdfd",
                    "border": "#eaeaea",
                    "border_width": 1,

                    "mark": {
                        "back": "#000000",
                        "size": 3
                    },

                    "active": {
                        "back": "#f9f9f9",
                        "border": "#aaaaaa",
                        "border_width": 1,
                        "checkbox_mark": "#eaeaea"
                    },

                    "pressed": {
                        "back": "#f9f9f9",
                        "border": "#e2e2e2",
                        "border_width": 1,
                        "checkbox_mark": "#000000"
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
            if "checkbox" in dict:
                self.checkbox_back = dict["checkbox"]["back"]
                self.checkbox_border = dict["checkbox"]["border"]
                self.checkbox_border_width = dict["checkbox"]["border_width"]

                if "mark" in dict["checkbox"]:
                    self.checkbox_mark_back = dict["checkbox"]["mark"]["back"]
                    self.checkbox_mark_size = dict["checkbox"]["mark"]["size"]

                if "active" in dict["checkbox"]:
                    self.checkbox_active_back = dict["checkbox"]["active"]["back"]
                    self.checkbox_active_border = dict["checkbox"]["active"]["border"]
                    self.checkbox_active_border_width = dict["checkbox"]["active"]["border_width"]

                    self.checkbox_active_mark = dict["checkbox"]["active"]["checkbox_mark"]

                if "pressed" in dict["checkbox"]:
                    self.checkbox_pressed_back = dict["checkbox"]["pressed"]["back"]
                    self.checkbox_pressed_border = dict["checkbox"]["pressed"]["border"]
                    self.checkbox_pressed_border_width = dict["checkbox"]["pressed"]["border_width"]

                    self.checkbox_pressed_mark = dict["checkbox"]["pressed"]["checkbox_mark"]

            self._palette = dict

            try:
                self._draw(None)
            except AttributeError:
                pass
        else:
            return self._palette


if __name__ == '__main__':
    from tkinter import Tk
    root = Tk()
    box = AdwDrawBasicCheckBox()
    box.pack()
    root.mainloop()
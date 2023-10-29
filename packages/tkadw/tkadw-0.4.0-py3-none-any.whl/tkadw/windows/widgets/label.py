from tkinter import Label
from tkadw.layout import AdwLayout


class AdwBasicLabel(Label, AdwLayout):
    def __init__(self, *args, text: str = "", **kwargs):
        super().__init__(*args, text=text, **kwargs)

        self._other()

        self.default_palette()

        self.bind("<Configure>", self._draw, add="+")
        self.bind("<Enter>", self._draw(), add="+")
        self.bind("<Leave>", self._draw(), add="+")

    def _draw(self, evt=None):
        if self.label_back == "transparent":
            self.configure(background=self.master.cget("bg"))
        self.configure(foreground=self.label_text_back)

    def _other(self):
        pass

    def default_palette(self):
        self.palette_light()

    def palette_light(self):
        self.palette(
            {
                "label": {
                    "back": "transparent",
                    "text_back": "#000000",
                }
            }
        )

    def palette_dark(self):
        self.palette(
            {
                "label": {
                    "back": "transparent",
                    "text_back": "#ffffff",
                }
            }
        )

    def palette(self, dict=None):
        if dict is not None:
            if "label" in dict:
                self.label_back = dict["label"]["back"]
                self.label_text_back = dict["label"]["text_back"]

            self._palette = dict

            try:
                self._draw(None)
            except AttributeError:
                pass
        else:
            return self._palette


class AdwLabel(AdwBasicLabel):
    def default_palette(self):
        self.palette_light()


class AdwDarkLabel(AdwBasicLabel):
    def default_palette(self):
        self.palette_dark()


if __name__ == '__main__':
    from tkinter import Tk
    root = Tk()
    label = AdwLabel(text="hello")
    label.pack()
    label2 = AdwDarkLabel(text="hello")
    label2.pack()
    root.mainloop()

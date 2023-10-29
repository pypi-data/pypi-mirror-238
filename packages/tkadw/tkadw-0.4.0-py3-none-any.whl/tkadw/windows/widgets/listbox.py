from tkadw.windows.canvas.frame import AdwDrawFrame, AdwDrawRoundFrame, AdwDrawRoundFrame3
from tkadw.windows.canvas.drawengine import AdwDrawEngine


class _Item:
    def __init__(self, canvas: AdwDrawEngine, listbox, item, i1, i2, iactive, irelease):
        self.canvas = canvas
        self.listbox = listbox
        self.item = item
        self.i1 = i1
        self.i2 = i2
        self.iactive = iactive
        self.irelease = irelease
        i = """
        self.canvas.tag_bind(i1, "<Button>", lambda evt: self.active(evt, item))
        self.canvas.tag_bind(i1, "<ButtonRelease>", lambda evt: self.release(evt, item))
        self.canvas.tag_bind(i2, "<Button>", lambda evt: self.active(evt, item))
        self.canvas.tag_bind(i2, "<ButtonRelease>", lambda evt: self.release(evt, item))
        """

        if self.listbox.select() == item:
            self.canvas.itemconfigure(
                self.i1, outline=self.iactive[1], fill=self.iactive[0]
            )
            self.canvas.itemconfigure(
                self.i2, fill=self.iactive[2]
            )

        it = """
        self.canvas.tag_bind(i1, "<Button>", self._click, add="+")
        self.canvas.tag_bind(i1, "<ButtonRelease>", self._unclick, add="+")
        self.canvas.tag_bind(i1, "<Enter>", self._hover, add="+")
        self.canvas.tag_bind(i1, "<Leave>", self._hover_release, add="+")
        """

        self.canvas.tag_bind(i1, "<Button>", self._click2, add="+")
        self.canvas.tag_bind(i2, "<Button>", self._click2, add="+")

    def _click2(self, evt=None):
        self.listbox.select(self.item)

    def _click(self, evt=None):
        self.hover = True

    def _unclick(self, evt=None):
        if self.hover:
            self.listbox.select(self.item)

    def _hover(self, evt=None):
        self.hover = True

    def _hover_release(self, evt=None):
        self.hover = False

    def click(self, event, item):
        self.canvas.itemconfigure(
            self.i1, outline=self.iactive[1], fill=self.iactive[0]
        )
        self.canvas.itemconfigure(
            self.i2, fill=self.iactive[2]
        )

    def release(self, event, item):
        self.canvas.itemconfigure(
            self.i1, outline=self.irelease[1], fill=self.irelease[0]
        )
        self.canvas.itemconfigure(
            self.i2, fill=self.irelease[2]
        )


class AdwListBox(AdwDrawFrame):
    def __init__(self, *args, items: list = [], item_selected=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.selectitem = None

        self.configure(items=items)

        self.item_canvas = AdwDrawEngine(self.frame, bd=0, highlightthickness=0)
        self.item_canvas.pack(fill="both", expand="yes", padx=3, pady=3)

        self.itemselected = item_selected

    def select(self, item=None):
        if item is None:
            return self.selectitem
        else:
            #print(item)
            self.focus_set()
            self.selectitem = item
            self.event_generate("<<ItemSelected>>")
            if self.itemselected is not None:
                self.itemselected()
            self._draw(None)

    def configure(self, **kwargs):
        if "items" in kwargs:
            self._items = kwargs.pop("items")
        if "item_selected" in kwargs:
            self.itemselected = kwargs.pop("item_selected")
        else:
            super().configure(**kwargs)

    def _draw(self, evt):
        super()._draw(evt)
        try:
            def release(event, item):
                pass

            self.item_canvas.delete("all")
            self.item_canvas.configure(background=self.frame_back)
            _i = 0
            self.items = {}
            for item in self._items:
                i1 = self.item_canvas.create_rectangle(
                    self.item_padding,
                    _i * self.item_height + self.item_padding,
                    self.item_canvas.winfo_width()-self.item_padding,
                    (_i + 1) * self.item_height,
                    outline=self.item_border, fill=self.item_back
                )
                i2 = self.item_canvas.create_text(
                    0+self.item_padding+5,
                    _i * self.item_height + self.item_padding + self.item_height/2,
                    text=item, anchor="w", fill=self.item_text
                )
                _i += 1

                i3 = _Item(self.item_canvas, self, item, i1, i2,
                           [self.item_active_back, self.item_active_border, self.item_active_text],
                           [self.item_back, self.item_border, self.item_text], )

                self.items[item] = [i1, i2]

        except:
            pass

    def palette(self, dict=None):
        if dict is not None:
            if "listbox" in dict:
                self.frame_back = dict["listbox"]["back"]
                self.frame_border = dict["listbox"]["border"]
                self.frame_border_width = dict["listbox"]["border_width"]
                self.frame_padding = dict["listbox"]["padding"]

                if "radius" in dict["listbox"]:
                    self.frame_radius = dict["listbox"]["radius"]

                self.item_back = dict["listbox"]["item_back"]
                self.item_border = dict["listbox"]["item_border"]
                self.item_text = dict["listbox"]["item_text"]

                if "item_radius" in dict["listbox"]:
                    self.item_radius = dict["listbox"]["item_radius"]

                self.item_active_back = dict["listbox"]["active"]["item_back"]
                self.item_active_border = dict["listbox"]["active"]["item_border"]
                self.item_active_text = dict["listbox"]["active"]["item_text"]

                self.item_height = dict["listbox"]["item_height"]
                self.item_padding = dict["listbox"]["item_padding"]

            self._palette = dict

            try:
                self._draw(None)
            except AttributeError:
                pass
        else:
            return self._palette

    def palette_light(self):
        self.palette(
            {
                "listbox": {
                    "back": "#ffffff",
                    "border": "#eaeaea",
                    "border_width": 2,
                    "padding": 0,
                    "radius": 3,

                    "item_back": "#ffffff",
                    "item_border": "#eaeaea",
                    "item_text": "#000000",

                    "item_radius": 6,
                    "item_height": 40,
                    "item_padding": 3,

                    "active": {
                        "item_back": "#185fb4",
                        "item_border": "#185fb4",
                        "item_text": "#ffffff",
                    },
                }
            }
        )

    def palette_dark(self):
        self.palette(
            {
                "listbox": {
                    "back": "#0f0f0f",
                    "border": "#333333",
                    "border_width": 2,
                    "padding": 0,
                    "radius": 3,

                    "item_back": "#0f0f0f",
                    "item_border": "#333333",
                    "item_text": "#ffffff",

                    "item_radius": 6,
                    "item_height": 40,
                    "item_padding": 3,

                    "active": {
                        "item_back": "#4cc2ff",
                        "item_border": "#4cc2ff",
                        "item_text": "#000000",
                    },
                }
            }
        )


class AdwRoundListBox2(AdwListBox, AdwDrawRoundFrame):
    def __init__(self, *args, items: list = [], **kwargs):
        super().__init__(*args, items=items, **kwargs)

    def _draw(self, evt):
        super()._draw(evt)
        try:
            def release(event, item):
                pass

            self.item_canvas.delete("all")
            self.item_canvas.configure(background=self.frame_back)
            _i = 0
            self.items = {}
            for item in self._items:
                i1 = self.item_canvas.create_round_rect2(
                    self.item_padding,
                    _i * self.item_height + self.item_padding,
                    self.item_canvas.winfo_width()-self.item_padding,
                    (_i + 1) * self.item_height,
                    radius=self.frame_radius,
                    outline=self.item_border, fill=self.item_back
                )
                i2 = self.item_canvas.create_text(
                    0+self.item_padding+5,
                    _i * self.item_height + self.item_padding + self.item_height/2,
                    text=item, anchor="w", fill=self.item_text
                )
                _i += 1

                i3 = _Item(self.item_canvas, self, item, i1, i2,
                           [self.item_active_back, self.item_active_border, self.item_active_text],
                           [self.item_back, self.item_border, self.item_text], )

                self.items[item] = [i1, i2]

        except:
            pass


class AdwRoundListBox3(AdwListBox, AdwDrawRoundFrame3):
    def __init__(self, *args, items: list = [], **kwargs):
        super().__init__(*args, items=items, **kwargs)

    def default_palette(self):
        self.palette(
            {
                "listbox": {
                    "back": "#ffffff",
                    "border": "#eaeaea",
                    "border_width": 2,
                    "padding": 0,
                    "radius": 8,

                    "item_back": "#ffffff",
                    "item_border": "#eaeaea",
                    "item_text": "#000000",

                    "item_radius": 10,
                    "item_height": 40,
                    "item_padding": 3,

                    "active": {
                        "item_back": "#185fb4",
                        "item_border": "#185fb4",
                        "item_text": "#ffffff",
                    },
                }
            }
        )

    def _draw(self, evt):
        super()._draw(evt)
        try:
            def release(event, item):
                pass

            self.item_canvas.delete("all")
            self.item_canvas.configure(background=self.frame_back)
            _i = 0
            self.items = {}
            for item in self._items:
                i1 = self.item_canvas.create_round_rect4(
                    self.item_padding,
                    _i * self.item_height + self.item_padding,
                    self.item_canvas.winfo_width()-self.item_padding,
                    (_i + 1) * self.item_height,
                    radius=self.frame_radius,
                    outline=self.item_border, fill=self.item_back
                )
                i2 = self.item_canvas.create_text(
                    0+self.item_padding+5,
                    _i * self.item_height + self.item_padding + self.item_height/2,
                    text=item, anchor="w", fill=self.item_text
                )
                _i += 1

                i3 = _Item(self.item_canvas, self, item, i1, i2,
                           [self.item_active_back, self.item_active_border, self.item_active_text],
                           [self.item_back, self.item_border, self.item_text], )

                self.items[item] = [i1, i2]

        except:
            pass


if __name__ == '__main__':
    from tkadw import Adw, Adwite, pypi_org_dark_theme

    root = Adw()
    #root = Adwite()
    #root.set_default_theme("Pypi", "dark")

    listbox = AdwRoundListBox3()
    #listbox.palette(pypi_org_dark_theme)

    listbox.configure(items=["Hello", "World"])

    listbox.row(padx=5, pady=5)

    root.mainloop()
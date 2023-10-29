from tkadw.windows.canvas.drawengine import AdwDrawEngine


class AgwSurface(AdwDrawEngine):
    def __init__(self, window, background="#000000"):
        super().__init__(window, highlightthickness=0, background=background)

    def show(self):
        self.pack(fill="both", expand="yes")


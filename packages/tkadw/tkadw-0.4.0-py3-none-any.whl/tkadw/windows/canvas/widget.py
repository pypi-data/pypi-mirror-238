from tkadw.windows.canvas.drawengine import AdwDrawEngine
from tkadw.layout import AdwLayout


class AdwWidget(AdwDrawEngine, AdwLayout):

    """
    基础绘制组件类

    特性：自动将背景颜色设为父组件背景颜色
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bind("<Configure>", self._draw, add="+")
        self._other()

    def _other(self):
        from tkadw.windows.canvas.frame import AdwDrawBasicFrame
        if hasattr(self.master, "frame_back"):
            self.configure(background=self.master.frame_back)
        self.configure(background=self.master.cget("bg"), borderwidth=0)

    def update(self) -> None:
        super().update()
        self._draw(None)

    def _draw(self, evt=None):
        pass
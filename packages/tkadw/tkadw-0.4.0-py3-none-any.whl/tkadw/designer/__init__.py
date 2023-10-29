from tkadw.designer.designerframe import AdwDesignerFrame

from tkadw.windows.theme import Adwite


__all__ = [
    "AdwDesigner",
    "AdwDesignerFrame"
]


class AdwDesigner(Adwite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("AdwDesigner")

        self.geometry("700x380")
from tkadw.windows.widgets.adw import Adw


class AgwWindow(Adw):
    def __init__(self, *args, resizable: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        self.resizable(resizable, resizable)

    def create_surface(self, *args, **kwargs):
        from tkadw.game.surface import AgwSurface
        _surface = AgwSurface(self)
        _surface.show()
        return _surface

    def run(self):
        self.mainloop()


if __name__ == '__main__':
    window = AgwWindow()
    surface = window.create_surface()
    window.run()
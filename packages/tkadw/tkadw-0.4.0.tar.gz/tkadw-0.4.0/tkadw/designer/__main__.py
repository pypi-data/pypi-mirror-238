if __name__ == '__main__':
    from tkadw import *

    root = AdwDesigner(default_theme="Pypi")

    designer_panel = AdwTFrame()

    designer_panel.column(padx=5, pady=5)

    root.mainloop()
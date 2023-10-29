import os.path
import os


def appconfig():
    if os.path.exists("app.config"):
        import configparser
        config = configparser.ConfigParser()
        config.read('app.config', encoding='UTF-8')

        if "title" in config["app"]:
            from tkinter import _default_root
            _default_root.title(config["app"]["title"])

        if "x" or "y" in config["app"]:
            from tkinter import _default_root

            pos = (int(config["app"]["x"]), int(config["app"]["y"]))

            _default_root.geometry(f"+{pos[0]}+{pos[1]}")

        if "width" or "height" in config["app"]:
            from tkinter import _default_root

            size = (int(config["app"]["width"]), int(config["app"]["height"]))

            _default_root.geometry(f"{size[0]}x{size[1]}")


if __name__ == '__main__':
    from tkadw import Adwite
    root = Adwite()
    appconfig()
    root.mainloop()
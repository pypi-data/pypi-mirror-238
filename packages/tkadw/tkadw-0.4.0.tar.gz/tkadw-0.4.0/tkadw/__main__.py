if __name__ == '__main__':
    from tkadw import *
    root = Adwite("win11", windark=False)
    root.set_default_theme("win11", "light")
    root.geometry("200x90")

    root.title("adw")

    version = AdwTLabel(root, text=f"tkadw`s version is {get_version()}")
    version.pack(anchor="center", padx=5, pady=5)

    button = AdwTButton(root, text="Quit", command=lambda: root.quit(), height=23)
    button.pack(anchor="center", padx=5, pady=5)

    root.mainloop()
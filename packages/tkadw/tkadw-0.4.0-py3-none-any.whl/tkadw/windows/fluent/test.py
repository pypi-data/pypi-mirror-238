from tkadw.windows.fluent import *
from tkadw import *

root = Adw()

frame = FluentFrame(root)

button = FluentButton(frame.frame, text="FluentButton")
button.pack(fill="x", padx=15, pady=15)

entry = FluentEntry(frame.frame)
entry.pack(fill="x", padx=15, pady=(0, 15))

frame.pack(fill="both", expand="yes", side="left")

frame2 = FluentDarkFrame(root)

button = FluentDarkButton(frame2.frame, text="FluentDarkButton")
button.pack(fill="x", padx=15, pady=15)

entry = FluentDarkEntry(frame2.frame)
entry.pack(fill="x", padx=15, pady=(0, 15))

frame2.pack(fill="both", expand="yes", side="right")

root.mainloop()
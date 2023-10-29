from tkadw.windows.canvas.frame import AdwDrawFrame, AdwDrawRoundFrame, AdwDrawDarkRoundFrame3


class AdwBasicTask(AdwDrawFrame):
    def _draw(self, evt=None):
        super()._draw(evt)

        self.task_top = self.create_rectangle(self.frame_border_width,
                                              self.frame_border_width,
                                              self.frame_border_width,
                                              self.frame_border_width,
                                              fill=self.task_top, outline=self.task_top,
                                              width=self.task_top_width)

    def palette(self, dict=None):
        if dict is not None:
            if "task" in dict:
                self.frame_back = dict["task"]["back"]
                self.frame_border = dict["task"]["border"]
                self.frame_border_width = dict["task"]["border_width"]
                self.frame_padding = dict["task"]["padding"]
                self.task_top = dict["task"]["top_line"]
                self.task_top_width = dict["task"]["top_width"]

            self._palette = dict

            try:
                self._draw(None)
            except AttributeError:
                pass
        else:
            return self._palette


if __name__ == '__main__':
    from tkadw.windows.widgets.adw import Adw
    root = Adw()
    task = AdwBasicTask()
    task.pack(fill="both", side="top", padx=5, pady=5)
    root.mainloop()
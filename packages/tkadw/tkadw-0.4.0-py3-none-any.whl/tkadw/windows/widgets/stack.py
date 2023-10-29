from tkinter import Frame, Widget


class AdwStack(Frame):
    def __init__(self, *args, **kwargs):
        """
        用于切换不同的界面
        """
        super().__init__(*args, **kwargs)
        self._pages = {}

    def add_page(self, page: Widget, id: int = 0):
        """
        添加页面

        :param page: 页面组件
        :param id: 组件ID
        """
        self._pages[id] = page

    def show_page(self, id: int):
        """
        显示页面，会将其他页面隐藏

        :param id: 被显示的页面ID
        """
        self._pages[id].pack(fill=tk.BOTH, expand=tk.YES)
        for item in self._pages.keys():
            if not item == id:
                self.hide_page(item)

    def hide_page(self, id: int):
        """
        内置函数，最好不要使用，因为几乎没有什么用
        """
        self._pages[id].pack_forget()

    def get_page(self, id: int):
        """
        获取页面

        :param id: 所要获取的页面ID
        """
        return self._pages[id]

    def get_pages(self):
        """
        获取所有页面
        """
        return self._pages
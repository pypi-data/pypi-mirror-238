from tkadw import *
from tkinter.font import nametofont, families, Font

index = """
tkAdw文档
*********

文档 > 主页

* 00 | 应用程序接口

  * 按钮

  * 绘画引擎

  * 条目输入框

  * 容器

  * 标签

  * 多文档窗口

  * 分割线

  * 文本输入框

  * 小组件

  * 主题组件

* 01 | 简介

  * tkAdw是什么

  * 我为什么要做tkAdw

  * 其他类似扩展库

* 02 | 主题组件

  * 主题原理

  * 设置主题

  * 使用主题组件

  * 版本警告

"""

p00 = """
00 | 应用程序接口
*****************

文档 > 应用程序接口 : sphinx.ext.autodoc

======================================================================


按钮
====

class tkadw.windows.canvas.button.AdwDrawAccentButton(*args, width=120, height=40, text: str = '', command=None, **kwargs)

class tkadw.windows.canvas.button.AdwDrawBasicButton(*args, width=120, height=40, text: str = '', command=None, **kwargs)

   自绘基础按钮

   configure(**kwargs)

      Configure resources of a widget.

      The values for resources are specified as keyword arguments. To
      get an overview about the allowed keyword arguments call the
      method keys.

   update() -> None

      多执行一道绘制

class tkadw.windows.canvas.button.AdwDrawBasicCircularButton(*args, width=120, height=120, **kwargs)

class tkadw.windows.canvas.button.AdwDrawBasicRoundButton(*args, **kwargs)

class tkadw.windows.canvas.button.AdwDrawButton(*args, width=120, height=40, text: str = '', command=None, **kwargs)

class tkadw.windows.canvas.button.AdwDrawCircularButton(*args, width=120, height=120, **kwargs)

class tkadw.windows.canvas.button.AdwDrawCircularDarkButton(*args, width=120, height=120, **kwargs)

class tkadw.windows.canvas.button.AdwDrawDarkButton(*args, width=120, height=40, text: str = '', command=None, **kwargs)

class tkadw.windows.canvas.button.AdwDrawRoundAccentButton(*args, **kwargs)

class tkadw.windows.canvas.button.AdwDrawRoundAccentButton2(*args, **kwargs)

class tkadw.windows.canvas.button.AdwDrawRoundAccentButton3(*args, **kwargs)

class tkadw.windows.canvas.button.AdwDrawRoundButton(*args, **kwargs)

class tkadw.windows.canvas.button.AdwDrawRoundButton2(*args, **kwargs)

class tkadw.windows.canvas.button.AdwDrawRoundButton3(*args, **kwargs)

class tkadw.windows.canvas.button.AdwDrawRoundDarkButton(*args, **kwargs)

class tkadw.windows.canvas.button.AdwDrawRoundDarkButton2(*args, **kwargs)

class tkadw.windows.canvas.button.AdwDrawRoundDarkButton3(*args, **kwargs)


绘画引擎
========

class tkadw.windows.canvas.drawengine.AdwDrawEngine(*args, **kwargs)

   create_gradient_circular(x, y, width, height, tags, color1, color2, *args, **kwargs)

      创建垂直渐变圆形

      参数:
         * **x** – 图形x位置

         * **y** – 图形y位置

         * **width** – 图形宽度

         * **height** – 图形高度

         * **tags** – 标签名

         * **color1** – 渐变颜色1

         * **color2** – 渐变颜色2

      返回:
   create_gradient_h_rectangle(x, y, width, height, tags, color1, color2, *args, **kwargs)

      创建垂直渐变矩形

      参数:
         * **x** – 图形x位置

         * **y** – 图形y位置

         * **width** – 图形宽度

         * **height** – 图形高度

         * **tags** – 标签名

         * **color1** – 渐变颜色1

         * **color2** – 渐变颜色2

      返回:
   create_gradient_v_rectangle(x, y, width, height, tags, color1, color2, *args, **kwargs)

      创建水平渐变矩形

      参数:
         * **x** – 图形x位置

         * **y** – 图形y位置

         * **width** – 图形宽度

         * **height** – 图形高度

         * **tags** – 标签名

         * **color1** – 渐变颜色1

         * **color2** – 渐变颜色2

      返回:
   create_round_rect(x1, y1, x2, y2, radius: float = 5, width=2, fill='white', outline='black')

      创建圆角矩形 ： 自绘版

   create_round_rect2(x0, y0, x3, y3, radius, *args, **kwargs)

      创建圆角矩形 ： 其他开发者制作 ： 边框有问题（不推荐）

   create_round_rect3(tag, x, y, width, height, radius, fill: str = 'black', outline: str = 'black', *args, **kwargs)

      创建圆角矩形 ： 其他开发者制作 ： 圆角看起来更舒服

   create_round_rect4(x1, y1, x2, y2, radius, **kwargs)

      创建圆角矩形 ： 其他开发者制作

   create_round_rectangle(x1, y1, x2, y2, radius: float = 5, width=2, fill='white', outline='black')

      创建圆角矩形 ： 自绘版

   create_round_rectangle2(x0, y0, x3, y3, radius, *args, **kwargs)

      创建圆角矩形 ： 其他开发者制作 ： 边框有问题（不推荐）

   create_round_rectangle3(tag, x, y, width, height, radius, fill: str = 'black', outline: str = 'black', *args, **kwargs)

      创建圆角矩形 ： 其他开发者制作 ： 圆角看起来更舒服

   create_round_rectangle4(x1, y1, x2, y2, radius, **kwargs)

      创建圆角矩形 ： 其他开发者制作

   gradient_demo()

      启动渐变引擎示例

   gradient_draw(tags: str, x: int, y: int, width: int, height: int, orient, color1, color2, *args, **kwargs)

      绘制渐变图形

   gradient_init()

      初始化渐变引擎

   gradient_recolor(tags: str, x: int, y: int, color1, color2)

      修改渐变组件的颜色

   gradient_redraw(*args, **kwargs)

      同gradient_draw

   gradient_resize(tags: str, x: int, y: int, width: int, height: int)

      修改渐变图形的大小位置

   win32_high_dpi()

      windows平台高DPI启用


条目输入框
==========

class tkadw.windows.canvas.entry.AdwDrawBasicEntry(*args, width=120, height=40, animated=5, text: str = '', show: str = None, **kwargs)

class tkadw.windows.canvas.entry.AdwDrawBasicRoundEntry(*args, **kwargs)

class tkadw.windows.canvas.entry.AdwDrawBasicRoundEntry3(*args, **kwargs)

class tkadw.windows.canvas.entry.AdwDrawDarkEntry(*args, width=120, height=40, animated=5, text: str = '', show: str = None, **kwargs)

class tkadw.windows.canvas.entry.AdwDrawEntry(*args, width=120, height=40, animated=5, text: str = '', show: str = None, **kwargs)

class tkadw.windows.canvas.entry.AdwDrawRoundDarkEntry(*args, **kwargs)

class tkadw.windows.canvas.entry.AdwDrawRoundDarkEntry3(*args, **kwargs)

class tkadw.windows.canvas.entry.AdwDrawRoundEntry(*args, **kwargs)

class tkadw.windows.canvas.entry.AdwDrawRoundEntry3(*args, **kwargs)


容器
====

class tkadw.windows.canvas.frame.AdwDrawBasicFrame(*args, width=200, height=200, **kwargs)

class tkadw.windows.canvas.frame.AdwDrawBasicRoundFrame(*args, **kwargs)

class tkadw.windows.canvas.frame.AdwDrawBasicRoundFrame3(*args, **kwargs)

class tkadw.windows.canvas.frame.AdwDrawDarkFrame(*args, width=200, height=200, **kwargs)

class tkadw.windows.canvas.frame.AdwDrawDarkRoundFrame(*args, **kwargs)

class tkadw.windows.canvas.frame.AdwDrawDarkRoundFrame3(*args, **kwargs)

class tkadw.windows.canvas.frame.AdwDrawFrame(*args, width=200, height=200, **kwargs)

class tkadw.windows.canvas.frame.AdwDrawRoundFrame(*args, **kwargs)

class tkadw.windows.canvas.frame.AdwDrawRoundFrame3(*args, **kwargs)


标签
====

class tkadw.windows.widgets.label.AdwBasicLabel(*args, text: str = '', **kwargs)

class tkadw.windows.widgets.label.AdwDarkLabel(*args, text: str = '', **kwargs)

class tkadw.windows.widgets.label.AdwLabel(*args, text: str = '', **kwargs)


多文档窗口
==========

class tkadw.windows.widgets.mdi.AdwMDI(*args, **kwargs)

   多文档窗口

   create_child()

      创建一个子窗口

      返回:
         AdwTFrame


分割线
======

class tkadw.windows.canvas.separator.AdwDrawBasicSeparator(*args, width=50, height=3, **kwargs)

class tkadw.windows.canvas.separator.AdwDrawDarkSeparator(*args, width=50, height=3, **kwargs)

class tkadw.windows.canvas.separator.AdwDrawSeparator(*args, width=50, height=3, **kwargs)


文本输入框
==========

class tkadw.windows.canvas.textbox.AdwDrawBasicRoundText(*args, **kwargs)

class tkadw.windows.canvas.textbox.AdwDrawBasicRoundText3(*args, **kwargs)

class tkadw.windows.canvas.textbox.AdwDrawBasicText(*args, text: str = '', width=120, height=80, **kwargs)

class tkadw.windows.canvas.textbox.AdwDrawDarkText(*args, text: str = '', width=120, height=80, **kwargs)

class tkadw.windows.canvas.textbox.AdwDrawRoundDarkText(*args, **kwargs)

class tkadw.windows.canvas.textbox.AdwDrawRoundDarkText3(*args, **kwargs)

class tkadw.windows.canvas.textbox.AdwDrawRoundText(*args, **kwargs)

class tkadw.windows.canvas.textbox.AdwDrawRoundText3(*args, **kwargs)

class tkadw.windows.canvas.textbox.AdwDrawText(*args, text: str = '', width=120, height=80, **kwargs)


小组件
======

class tkadw.windows.canvas.widget.AdwWidget(*args, **kwargs)

   基础绘制组件类

   特性：自动将背景颜色设为父组件背景颜色


主题组件
========

class tkadw.windows.theme.AdwTButton(*args, **kwargs)

class tkadw.windows.theme.AdwTEntry(*args, **kwargs)

class tkadw.windows.theme.AdwTFrame(*args, **kwargs)

class tkadw.windows.theme.AdwTLabel(*args, text: str = '', **kwargs)

class tkadw.windows.theme.AdwTSeparator(*args, width=50, height=3, **kwargs)

class tkadw.windows.theme.AdwTText(*args, **kwargs)

class tkadw.windows.theme.Adwite(*args, title: str = 'adw', icon='light', windark: bool = True, wincaption=None, **kwargs)

"""

p01 = """
01 | 简介
*********

文档 > 简介

======================================================================


tkAdw是什么
===========

tkAdw是"tkinter"的扩展组件库，运用"tkinter.Canvas"组件绘制高级、现代化
的界面。将每个组件都设为"tkinter.Canvas"，在上面绘制组件，当大小位置发
生改变便重新绘制。


我为什么要做tkAdw
=================

之前我都在用"customtkinter"做界面，但是用着用着我就发现，有些样式无法
绘制出来，如"winui3"中的"TextBox(Entry)"界面效果下划线无法实现，所以这
才想到可以自己做一个界面框架。


其他类似扩展库
==============

* "customtkinter" ： 它和"tkadw"一样使用"tkinter.Canvas"绘制组件，也同
  样支持圆角绘制；不同的是他们采用的是"macos"平台组件设计的，而"tkadw"
  是采用"gtk"和"winui3"的样式进行设计的，还有就是按钮的点击事件不同，
  他们采用的是 "鼠标碰到并按下按钮" 触发事件，而"tkadw"这是更加高级复
  制的"鼠标碰到并按下按钮直到鼠标放开并碰到鼠标"触发事件。

* "tinui" ： *待添加*

======================================================================

编写：XiangQinxi

"""

p02 = """
02 | 主题组件
*************

文档 > 主题组件

======================================================================


主题原理
========

将主题加入环境变量"tkAdwite.DefaultTheme"，需要时对环境变量进行读取。


设置主题
========

root需设置为"tkadw.windows.theme.Adwite"，"set_default_theme"设置主题
及附加深浅模式设置，有三个内置主题"win11" "gtk" "bilibili" "metro", 我
为内置主题都设计了深浅两种主题，可以在附加参数填入"system" "dark"
"light"（"system"参数需安装"darkdetect"，如果未安装且设置为"system"将
自动设为"light"主题）。


使用主题组件
============

暂有这些组件"AdwTButton" "AdwTEntry" "AdwTFrame" "AdwTLabel"
"AdwTSeparator" "AdwTText"。需配合"Adwite"设置主题

   from tkadw import Adwite, AdwTButton

   root = Adwite()
   root.set_default_theme("win11", "dark")  # 设置主题，第一个参数为`主题设置`或`内置主题名`，第二个参数为`内置主题深浅模式`

   button = AdwTButton(text="Hello World")
   button.pack(fill="x", padx=15, pady=15)

   root.mainloop()


版本警告
========

"主题组件"自"0.3.0"版本才加入，请注意"tkadw"的版本号

======================================================================

编写：XiangQinxi

"""

root = Adwite()
root.set_default_theme("metro")
root.geometry("980x520")

page = 1
print(families())
read = AdwTText(root)
font = nametofont("TkDefaultFont")
font.configure(size=11)
read.font(font)
read.tdelete("1.0", "end")
read.tinsert("1.0", index)
read.pack(fill="both", expand="yes", padx=15, pady=15)


def up():
    global page
    if page == 1:
        page = 2
        read.tdelete("1.0", "end")
        read.tinsert("1.0", p00)
    elif page == 2:
        page = 3
        read.tdelete("1.0", "end")
        read.tinsert("1.0", p01)
    elif page == 3:
        page = 4
        read.tdelete("1.0", "end")
        read.tinsert("1.0", p02)
    elif page == 4:
        page = 1
        read.tdelete("1.0", "end")
        read.tinsert("1.0", index)


def down():
    global page
    if page == 1:
        page = 4
        read.tdelete("1.0", "end")
        read.tinsert("1.0", p02)
    elif page == 2:
        page = 1
        read.tdelete("1.0", "end")
        read.tinsert("1.0", index)
    elif page == 3:
        page = 2
        read.tdelete("1.0", "end")
        read.tinsert("1.0", p00)
    elif page == 4:
        page = 3
        read.tdelete("1.0", "end")
        read.tinsert("1.0", p01)


combar = AdwTFrame(root, height=40)
combar.frame_border_width = 0
combar.frame_radius = 0

comdowm = AdwTButton(combar.frame, text="上一页", command=down)
comdowm.pack(fill="both", expand="yes", side="left", padx=5, pady=5)

comup = AdwTButton(combar.frame, text="下一页", command=up)
comup.pack(fill="both", expand="yes", side="right", padx=5, pady=5)

combar.pack(fill="x", side="bottom", ipady=10)

root.mainloop()
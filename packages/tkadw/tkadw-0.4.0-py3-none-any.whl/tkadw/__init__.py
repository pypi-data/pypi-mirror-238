from tkadw.windows.widgets import *
from tkadw.utility.appconfig import appconfig as AdwReadAppConfig

from tkadw.windows import *

# 0.3.0加入
from tkadw.windows.theme import *

from tkadw.game import *

# 0.3.5加入
from tkadw.layout import *

# 0.3.9加入
from tkadw.designer import *


# from tkadw.tkite import * 已废弃移除
# from tkadw.win11 import * 已废弃移除
# from tkadw.advanced import * 已废弃移除，改为from tkadw.adw import Adw导入
# from tkadw.bilibili import BiliBiliButton, BiliBiliDarkButton, BiliBiliFrame, BiliBiliDarkFrame, \
#     BiliBiliEntry, BiliBiliDarkEntry, BiliBiliDarkTextBox, BiliBiliTextBox 已废弃移除

# 0.3.7补充
from tkadw.utility import *


def get_version():
    return "0.4.0"


def get_major_version():
    return "0"


def get_micro_version():
    return "4"

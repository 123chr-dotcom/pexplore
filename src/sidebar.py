import os
import platform
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt


class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.model = QStandardItemModel()
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setHeaderHidden(True)

        # 添加常用位置
        self.add_common_locations()

        layout.addWidget(self.tree_view)
        self.setLayout(layout)

    def add_common_locations(self):
        system = platform.system()
        if system == 'Windows':
            # 此电脑
            this_pc = QStandardItem("此电脑")
            self.model.appendRow(this_pc)

            # 桌面
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            desktop_item = QStandardItem("桌面")
            desktop_item.setData(desktop_path, Qt.UserRole)
            this_pc.appendRow(desktop_item)

            # 文档
            documents_path = os.path.join(os.path.expanduser("~"), "Documents")
            documents_item = QStandardItem("文档")
            documents_item.setData(documents_path, Qt.UserRole)
            this_pc.appendRow(documents_item)

            # 下载
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            downloads_item = QStandardItem("下载")
            downloads_item.setData(downloads_path, Qt.UserRole)
            this_pc.appendRow(downloads_item)

            # 图片
            pictures_path = os.path.join(os.path.expanduser("~"), "Pictures")
            pictures_item = QStandardItem("图片")
            pictures_item.setData(pictures_path, Qt.UserRole)
            this_pc.appendRow(pictures_item)

            # 视频
            videos_path = os.path.join(os.path.expanduser("~"), "Videos")
            videos_item = QStandardItem("视频")
            videos_item.setData(videos_path, Qt.UserRole)
            this_pc.appendRow(videos_item)

            # 音乐
            music_path = os.path.join(os.path.expanduser("~"), "Music")
            music_item = QStandardItem("音乐")
            music_item.setData(music_path, Qt.UserRole)
            this_pc.appendRow(music_item)

            # 驱动器
            import win32api
            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]
            for drive in drives:
                drive_item = QStandardItem(drive)
                drive_item.setData(drive, Qt.UserRole)
                this_pc.appendRow(drive_item)

    def get_item_path(self, index):
        item = self.model.itemFromIndex(index)
        if item:
            return item.data(Qt.UserRole)
        return None

    def update_current_path(self, path):
        # 这里可以实现高亮当前选中路径对应的侧边栏节点，暂未完善
        pass
    
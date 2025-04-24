import os
import subprocess
import shutil
import win32clipboard
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListView, QMenu, QInputDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileSystemModel


class FileView(QWidget):
    def __init__(self):
        super().__init__()
        self.history = []
        self.current_index = -1
        self.initUI()
        self.setStyleSheet("""
            QListView {
                background-color: #ffffff;
                border: none;
                font-family: "Segoe UI", sans-serif;
            }
            QListView::item {
                padding: 5px;
            }
            QListView::item:selected {
                background-color: #d0d0d0;
                color: #333333;
            }
            QListView::item:hover {
                background-color: #e0e0e0;
            }
        """)

    def initUI(self):
        layout = QVBoxLayout()

        self.model = QFileSystemModel()
        self.model.setRootPath(os.path.expanduser("~"))

        self.list_view = QListView()
        self.list_view.setModel(self.model)
        self.list_view.setRootIndex(self.model.index(os.path.expanduser("~")))
        self.list_view.clicked.connect(self.on_item_click)
        self.list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_view.customContextMenuRequested.connect(self.show_context_menu)

        layout.addWidget(self.list_view)
        self.setLayout(layout)

        self.history.append(self.model.rootPath())
        self.current_index = 0

    def set_path(self, path):
        if os.path.isdir(path):
            index = self.model.index(path)
            self.list_view.setRootIndex(index)
            if self.current_index < len(self.history) - 1:
                self.history = self.history[:self.current_index + 1]
            self.history.append(path)
            self.current_index += 1

    def on_item_click(self, index):
        path = self.model.filePath(index)
        if os.path.isdir(path):
            self.set_path(path)
        else:
            self.open_file(path)

    def open_file(self, path):
        try:
            if os.name == 'nt':
                os.startfile(path)
            else:
                subprocess.call(['open', path])
        except Exception as e:
            print(f"无法打开文件: {e}")

    def show_context_menu(self, pos):
        menu = QMenu(self)
        open_action = menu.addAction("打开")
        delete_action = menu.addAction("删除")
        copy_abs_path_action = menu.addAction("复制绝对路径")
        rename_action = menu.addAction("重命名")
        action = menu.exec_(self.list_view.mapToGlobal(pos))
        index = self.list_view.indexAt(pos)
        path = self.model.filePath(index)

        if action == open_action:
            if os.path.isfile(path):
                self.open_file(path)
        elif action == delete_action:
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)
                self.refresh_view()
        elif action == copy_abs_path_action:
            self.copy_to_clipboard(path)
        elif action == rename_action:
            if os.path.exists(path):
                dirname = os.path.dirname(path)
                old_name = os.path.basename(path)
                new_name, ok = QInputDialog.getText(self, "重命名", "请输入新的文件名:", text=old_name)
                if ok and new_name:
                    new_path = os.path.join(dirname, new_name)
                    try:
                        os.rename(path, new_path)
                        self.refresh_view()
                    except Exception as e:
                        print(f"重命名文件时出错: {e}")

    def refresh_view(self):
        current_path = self.model.rootPath()
        self.model.setRootPath('')
        self.model.setRootPath(current_path)

    def copy_to_clipboard(self, text):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text)
        win32clipboard.CloseClipboard()

    def go_back(self):
        if self.current_index > 0:
            self.current_index -= 1
            path = self.history[self.current_index]
            self.list_view.setRootIndex(self.model.index(path))

    def go_forward(self):
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            path = self.history[self.current_index]
            self.list_view.setRootIndex(self.model.index(path))

    
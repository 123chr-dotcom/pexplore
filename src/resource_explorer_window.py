import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QMenuBar, QAction, QToolBar, QTreeView, QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from sidebar import Sidebar
from file_view import FileView


class ResourceExplorerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStyleSheet(self.get_stylesheet())

    def initUI(self):
        self.setWindowTitle("资源管理器")
        main_layout = QVBoxLayout()

        # 工具栏
        toolbar = QToolBar()
        toolbar.setStyleSheet("QToolBar { background-color: #f0f0f0; border: none; }")
        back_action = QAction('←', self)
        back_action.triggered.connect(self.go_back)
        forward_action = QAction('→', self)
        forward_action.triggered.connect(self.go_forward)
        new_tab_action = QAction('+', self)
        new_tab_action.triggered.connect(self.add_new_tab)
        toolbar.addAction(back_action)
        toolbar.addAction(forward_action)
        toolbar.addAction(new_tab_action)
        main_layout.addWidget(toolbar)

        # 水平布局，包含侧边栏和标签页
        h_layout = QHBoxLayout()

        # 侧边栏
        self.sidebar = Sidebar()
        self.sidebar.tree_view.clicked.connect(self.on_sidebar_select)
        h_layout.addWidget(self.sidebar)

        # 主文件视图（使用标签页管理）
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tab_widget.customContextMenuRequested.connect(self.show_tab_context_menu)
        self.tab_widget.setStyleSheet("QTabWidget::pane { border: none; }"
                                      "QTabBar::tab { background-color: #f0f0f0; padding: 5px; border: none; }"
                                      "QTabBar::tab:selected { background-color: #d0d0d0; }")
        h_layout.addWidget(self.tab_widget)

        main_layout.addLayout(h_layout)

        # 初始标签页
        self.add_new_tab()

        # 菜单栏
        menubar = QMenuBar()
        file_menu = menubar.addMenu('文件')
        new_tab_action_menu = QAction('新建标签页', self)
        new_tab_action_menu.triggered.connect(self.add_new_tab)
        file_menu.addAction(new_tab_action_menu)
        close_tab_action_menu = QAction('关闭当前标签页', self)
        close_tab_action_menu.triggered.connect(self.close_current_tab)
        file_menu.addAction(close_tab_action_menu)

        main_layout.setMenuBar(menubar)
        self.setLayout(main_layout)

    def add_new_tab(self):
        file_view = FileView()
        index = self.tab_widget.addTab(file_view, "新标签页")
        self.tab_widget.setCurrentIndex(index)
        self.sidebar.update_current_path(file_view.model.rootPath())

    def close_current_tab(self):
        current_index = self.tab_widget.currentIndex()
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(current_index)

    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)

    def on_sidebar_select(self, index):
        path = self.sidebar.get_item_path(index)
        if path and os.path.isdir(path):
            current_file_view = self.tab_widget.currentWidget()
            current_file_view.set_path(path)
            self.sidebar.update_current_path(path)

    def go_back(self):
        current_file_view = self.tab_widget.currentWidget()
        current_file_view.go_back()

    def go_forward(self):
        current_file_view = self.tab_widget.currentWidget()
        current_file_view.go_forward()

    def show_tab_context_menu(self, pos):
        menu = QMenu(self)
        close_current_tab_action = menu.addAction("关闭当前标签页")
        close_other_tabs_action = menu.addAction("关闭其他标签页")
        close_all_tabs_action = menu.addAction("关闭所有标签页")
        action = menu.exec_(self.tab_widget.mapToGlobal(pos))
        current_index = self.tab_widget.currentIndex()
        if action == close_current_tab_action:
            self.close_current_tab()
        elif action == close_other_tabs_action:
            for i in range(self.tab_widget.count() - 1, -1, -1):
                if i != current_index:
                    self.tab_widget.removeTab(i)
        elif action == close_all_tabs_action:
            while self.tab_widget.count() > 0:
                self.tab_widget.removeTab(0)
            self.add_new_tab()

    def get_stylesheet(self):
        return """
            QWidget {
                background-color: #ffffff;
                color: #333333;
                font-family: "Segoe UI", sans-serif;
            }
            QTreeView {
                background-color: #f0f0f0;
                border: none;
            }
            QListView {
                background-color: #ffffff;
                border: none;
            }
            QMenu {
                background-color: #ffffff;
                border: 1px solid #d0d0d0;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: #d0d0d0;
            }
        """
    
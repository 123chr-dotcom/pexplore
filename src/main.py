import sys
from PyQt5.QtWidgets import QApplication
from resource_explorer_window import ResourceExplorerWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    explorer = ResourceExplorerWindow()
    explorer.show()
    sys.exit(app.exec_())
    
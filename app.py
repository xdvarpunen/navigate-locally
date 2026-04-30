import sys
from io import BytesIO

import qrcode
from PyQt5.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu,
    QAction, QWidget, QLabel, QVBoxLayout, QInputDialog
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt


class QRWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Code")
        self.setFixedSize(300, 320)

        layout = QVBoxLayout()

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)

        self.text = QLabel()
        self.text.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.label)
        layout.addWidget(self.text)

        self.setLayout(layout)

    def update_qr(self, text: str):
        img = qrcode.make(text)

        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        pixmap = QPixmap()
        pixmap.loadFromData(buf.read())

        self.label.setPixmap(
            pixmap.scaled(250, 250, Qt.KeepAspectRatio)
        )
        self.text.setText(text)


class TrayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.text = "Hello QR"
        self.window = QRWindow()
        self.window.update_qr(self.text)

        self.tray = QSystemTrayIcon(QIcon())
        self.menu = QMenu()

        self.show_action = QAction("Show QR")
        self.show_action.triggered.connect(self.window.show)

        self.edit_action = QAction("Edit Text")
        self.edit_action.triggered.connect(self.edit_text)

        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(self.quit)

        self.menu.addAction(self.show_action)
        self.menu.addAction(self.edit_action)
        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)

        self.tray.setContextMenu(self.menu)
        self.tray.setToolTip("QR Tray MVP")
        self.tray.show()

    def edit_text(self):
        text, ok = QInputDialog.getText(
            None,
            "Update QR",
            "Enter text:"
        )

        if ok and text:
            self.text = text
            self.window.update_qr(text)
            self.window.show()

    def quit(self):
        self.tray.hide()
        self.app.quit()

    def run(self):
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    TrayApp().run()

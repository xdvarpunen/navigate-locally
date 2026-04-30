import sys
from io import BytesIO

import qrcode
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLineEdit, QLabel
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class QRApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Live QR Generator (2026)")
        self.setMinimumSize(380, 450)

        layout = QVBoxLayout(self)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Type text or URL...")
        self.input.textChanged.connect(self.update_qr)

        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)

        self.text_label = QLabel()
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setWordWrap(True)

        layout.addWidget(self.input)
        layout.addWidget(self.qr_label)
        layout.addWidget(self.text_label)

        self.update_qr("Hello QR")

    def update_qr(self, text: str):
        if not text:
            text = " "

        img = qrcode.make(text)

        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        pixmap = QPixmap()
        pixmap.loadFromData(buf.read())

        self.qr_label.setPixmap(
            pixmap.scaled(320, 320, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        self.text_label.setText(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRApp()
    window.show()
    sys.exit(app.exec())

import sys
import socket
from io import BytesIO

import qrcode
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLineEdit, QLabel, QPushButton, QHBoxLayout
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()


class QRApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LAN QR Generator")
        self.setMinimumSize(400, 520)

        self.last_ip = None
        self.current_ip = None

        # ---------- Layout ----------
        layout = QVBoxLayout(self)

        # ---------- IP Section ----------
        self.ip_label = QLabel()
        self.ip_label.setAlignment(Qt.AlignCenter)

        self.last_ip_label = QLabel()
        self.last_ip_label.setAlignment(Qt.AlignCenter)
        self.last_ip_label.setStyleSheet("color: gray; font-size: 11px;")

        self.refresh_btn = QPushButton("Refresh Wi-Fi IP")
        self.refresh_btn.clicked.connect(self.refresh_ip)

        ip_layout = QVBoxLayout()
        ip_layout.addWidget(self.ip_label)
        ip_layout.addWidget(self.last_ip_label)
        ip_layout.addWidget(self.refresh_btn)

        # ---------- Input ----------
        self.input = QLineEdit()
        self.input.setPlaceholderText("Type text or URL...")
        self.input.textChanged.connect(self.update_qr)

        # ---------- QR ----------
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)

        self.text_label = QLabel()
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setWordWrap(True)

        # ---------- Assemble ----------
        layout.addLayout(ip_layout)
        layout.addWidget(self.input)
        layout.addWidget(self.qr_label)
        layout.addWidget(self.text_label)

        # init state
        self.refresh_ip()
        self.update_qr("Hello QR")

    # -------------------------
    # IP logic
    # -------------------------
    def refresh_ip(self):
        self.last_ip = self.current_ip
        self.current_ip = get_local_ip()

        self.ip_label.setText(f"🌐 Wi-Fi IP: {self.current_ip}")

        if self.last_ip:
            self.last_ip_label.setText(f"Last IP: {self.last_ip}")
        else:
            self.last_ip_label.setText("Last IP: —")

    # -------------------------
    # QR logic
    # -------------------------
    def update_qr(self, text):
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

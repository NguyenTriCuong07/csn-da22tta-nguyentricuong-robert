from PyQt6 import QtCore, QtGui, QtWidgets
from PIL import Image
import numpy as np

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 900)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 100, 600, 600))
        self.label.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(700, 100, 600, 600))
        self.label_2.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.textBrowser = QtWidgets.QTextBrowser(parent=self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(300, 20, 700, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(200, 750, 150, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(400, 750, 150, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(600, 750, 150, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(800, 750, 150, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1300, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Kết nối sự kiện nút
        self.pushButton.clicked.connect(self.upload_image)
        self.pushButton_2.clicked.connect(self.save_image)
        self.pushButton_3.clicked.connect(self.delete_image)
        self.pushButton_4.clicked.connect(self.exit_application)

        # Khởi tạo biến lưu ảnh cạnh
        self.image_path = None
        self.edges_image = None

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textBrowser.setHtml(_translate("MainWindow", "<p align='center'><span style='font-size:18pt; font-weight:600;'>Phát hiện cạnh của đối tượng dựa trên kỹ thuật Robert</span></p>"))
        self.pushButton.setText(_translate("MainWindow", "Tải ảnh lên"))
        self.pushButton_2.setText(_translate("MainWindow", "Lưu"))
        self.pushButton_3.setText(_translate("MainWindow", "Xóa"))
        self.pushButton_4.setText(_translate("MainWindow", "Thoát"))

    def upload_image(self):
        try:
            options = QtWidgets.QFileDialog.Option.DontUseNativeDialog
            file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
                parent=None,
                caption="Chọn ảnh để upload",
                filter="Image Files (*.png *.jpg *.bmp *.webp)",
                options=options
            )

            if not file_path:
                QtWidgets.QMessageBox.warning(None, "Cảnh báo", "Bạn chưa chọn file!")
                return

            try:
                image = Image.open(file_path).convert('L')
                self.image_path = file_path

                # Áp dụng bộ lọc Robert
                self.edges_image = self.roberts_cross_edge_detection_manual(image)

                # Hiển thị ảnh gốc giữ nguyên tỉ lệ
                pixmap = QtGui.QPixmap(file_path)
                scaled_pixmap = pixmap.scaled(
                    self.label.width(), self.label.height(),
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio
                )
                self.label.setPixmap(scaled_pixmap)

                # Hiển thị ảnh đã xử lý cạnh giữ nguyên tỉ lệ
                edges_image = Image.fromarray(self.edges_image)
                edges_qimage = QtGui.QImage(
                    edges_image.tobytes("raw", "L"),
                    edges_image.width,
                    edges_image.height,
                    edges_image.width,
                    QtGui.QImage.Format.Format_Grayscale8
                )
                edges_pixmap = QtGui.QPixmap.fromImage(edges_qimage).scaled(
                    self.label_2.width(), self.label_2.height(),
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio
                )
                self.label_2.setPixmap(edges_pixmap)

                QtWidgets.QMessageBox.information(None, "Thành công", "Ảnh đã được tải và xử lý thành công!")

            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Lỗi", f"Tệp không phải ảnh hợp lệ hoặc không thể xử lý: {e}")
                return

        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Lỗi", f"Đã xảy ra lỗi không mong muốn: {e}")

    def save_image(self):
        """
        Hàm lưu ảnh đã xử lý cạnh.
        """
        if self.edges_image is not None:
            options = QtWidgets.QFileDialog.Option.DontUseNativeDialog
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                parent=None,
                caption="Lưu ảnh",
                filter="Image Files (*.png *.jpg *.bmp)",
                options=options
            )
            if file_path:
                try:
                    Image.fromarray(self.edges_image).save(file_path)
                    QtWidgets.QMessageBox.information(None, "Thành công", "Ảnh đã được lưu thành công!")
                except Exception as e:
                    QtWidgets.QMessageBox.critical(None, "Lỗi", f"Không thể lưu ảnh: {e}")
        else:
            QtWidgets.QMessageBox.warning(None, "Cảnh báo", "Bạn cần tải và xử lý ảnh trước khi lưu!")

    def delete_image(self):
        """
        Hàm xóa ảnh.
        """
        self.image_path = None
        self.edges_image = None
        self.label.clear()
        self.label_2.clear()
        QtWidgets.QMessageBox.information(None, "Thông báo", "Ảnh đã được xóa thành công!")

    def exit_application(self):
        """
        Hàm thoát ứng dụng.
        """
        QtWidgets.QApplication.instance().quit()

    def roberts_cross_edge_detection_manual(self, image):
        """
        Hàm phát hiện cạnh bằng bộ lọc Roberts.
        """
        image = np.array(image, dtype=float)
        roberts_cross_v = np.array([[1, 0], [0, -1]])
        roberts_cross_h = np.array([[0, 1], [-1, 0]])
        rows, cols = image.shape
        vertical_edges = np.zeros((rows - 1, cols - 1))
        horizontal_edges = np.zeros((rows - 1, cols - 1))

        for i in range(rows - 1):
            for j in range(cols - 1):
                vertical_edges[i, j] = (
                    roberts_cross_v[0, 0] * image[i, j] +
                    roberts_cross_v[0, 1] * image[i, j + 1] +
                    roberts_cross_v[1, 0] * image[i + 1, j] +
                    roberts_cross_v[1, 1] * image[i + 1, j + 1]
                )
                horizontal_edges[i, j] = (
                    roberts_cross_h[0, 0] * image[i, j] +
                    roberts_cross_h[0, 1] * image[i, j + 1] +
                    roberts_cross_h[1, 0] * image[i + 1, j] +
                    roberts_cross_h[1, 1] * image[i + 1, j + 1]
                )

        edges = np.sqrt(np.square(vertical_edges) + np.square(horizontal_edges))
        edges = (edges / edges.max()) * 255
        return edges.astype(np.uint8)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QFrame, QHBoxLayout, QScrollArea, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap, QColor
import _pip

BLOCK_STYLESHEET = "background-color: #ECECEC; border-radius: 10px;"
TEXTLABEL_STYLESHEET = "color: #000000; text-align: center;"

def createVerticalBlock(layout, package_name, mousePressHandler):
    # Create block 1
    block1 = QFrame()
    block1.setFrameShape(QFrame.StyledPanel)
    block1.setFixedHeight(100)
    block1.setStyleSheet(BLOCK_STYLESHEET)
    layout.addWidget(block1)

    # Add image and text label to block 1
    block1_layout = QHBoxLayout(block1)
    block1_layout.setContentsMargins(10, 10, 10, 10)

    # Add text label to block 1
    text_label1 = QLabel(package_name)
    text_label1.setStyleSheet(TEXTLABEL_STYLESHEET)
    text_label1.setWordWrap(True)
    block1_layout.addWidget(text_label1)

    block1.mousePressEvent = mousePressHandler

def createMessageBox(text, title, icon=QMessageBox.Information):
    msgBox = QMessageBox()
    msgBox.setIcon(icon)
    msgBox.setText(text)
    msgBox.setWindowTitle(title)

    return msgBox

def uninstallConfirm(name):
    def handler(event):
        msgBox = createMessageBox(f"Uninstall \"{name}\"?", "Confirm")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        returnValue = msgBox.exec()

        if returnValue == QMessageBox.Yes:
            try:
                _pip.uninstall_package(name)
            except Exception as e:
                msgBox = createMessageBox(f"Error occured while uninstalling package \"{name}\".\n{e}", "Error")
                msgBox.exec()
            resetScrollWidget()

            for package in _pip.getInstalledPackages():
                createVerticalBlock(scroll_widget_layout, package.title(), uninstallConfirm(package.title()))
                createSeparator(scroll_widget_layout)
                resetScrollWidget()

                for package in _pip.getInstalledPackages():
                    createVerticalBlock(scroll_widget_layout, package.title(), uninstallConfirm(package.title()))
                    createSeparator(scroll_widget_layout)

                window.setWindowTitle("GPIP - %s results" % len(_pip.getInstalledPackages()))


    return handler

def installConfirm(name):
    def handler(event):
        msgBox = createMessageBox(f"Install \"{name}\"?", "Confirm")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        returnValue = msgBox.exec()

        if returnValue == QMessageBox.Yes:
            try:
                _pip.install_package(name)
            except Exception as e:
                msgBox = createMessageBox(f"Error occured while installing package \"{name}\".\n{e}", "Error")
                msgBox.exec()
            resetScrollWidget()

            for package in _pip.getInstalledPackages():
                createVerticalBlock(scroll_widget_layout, package.title(), uninstallConfirm(package.title()))
                createSeparator(scroll_widget_layout)

            resetScrollWidget()

            for package in _pip.getInstalledPackages():
                createVerticalBlock(scroll_widget_layout, package.title(), uninstallConfirm(package.title()))
                createSeparator(scroll_widget_layout)

            window.setWindowTitle("GPIP - %s results" % len(_pip.getInstalledPackages()))

    return handler

def createSeparator(layout):
    separator = QFrame()
    separator.setFrameShape(QFrame.HLine)
    separator.setFrameShadow(QFrame.Sunken)
    layout.addWidget(separator)

def createSearchField():
    search_widget = QWidget()
    search_layout = QHBoxLayout(search_widget)
    search_layout.setContentsMargins(10, 10, 10, 10)
    search_layout.setSpacing(10)

    search_field = QLineEdit()
    search_layout.addWidget(search_field)

    search_button = QPushButton("Search")
    search_button.clicked.connect(lambda: search_packets(search_field.text()))
    search_layout.addWidget(search_button)

    return search_widget

def resetScrollWidget():
    while scroll_widget_layout.count():
        child = scroll_widget_layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()

def search_packets(query):
    resetScrollWidget()
    _len = 0

    for package in _pip.searchPackage(query):
        createVerticalBlock(scroll_widget_layout, package.title(), installConfirm(package.title()))
        createSeparator(scroll_widget_layout)

        _len += 1 
    
    window.setWindowTitle("GPIP - %s results" % _len)

app = QApplication(sys.argv)

scroll_area = QScrollArea()
scroll_area.setWidgetResizable(True)

scroll_widget = QWidget()
scroll_widget_layout = QVBoxLayout(scroll_widget)

for package in _pip.getInstalledPackages():
    createVerticalBlock(scroll_widget_layout, package.title(), uninstallConfirm(package.title()))
    createSeparator(scroll_widget_layout)

scroll_area.setWidget(scroll_widget)

search_widget = createSearchField()

main_layout = QVBoxLayout()
main_layout.addWidget(search_widget)
main_layout.addWidget(scroll_area)
main_layout.addStretch(1)

window = QWidget()
window.setLayout(main_layout)
window.setWindowTitle("GPIP - %s results" % len(_pip.getInstalledPackages()))
window.resize(800, 600)
window.show()

sys.exit(app.exec_())

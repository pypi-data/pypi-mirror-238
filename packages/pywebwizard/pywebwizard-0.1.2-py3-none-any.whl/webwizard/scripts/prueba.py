import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QGroupBox

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Top section
        h_layout1 = QHBoxLayout()
        h_layout1.addWidget(QLabel("Archivo"))
        h_layout1.addWidget(QLineEdit())
        h_layout1.addWidget(QLineEdit())
        h_layout1.addWidget(QLineEdit())
        h_layout1.addWidget(QPushButton("+"))
        h_layout1.addWidget(QPushButton("Ir"))
        layout.addLayout(h_layout1)

        # Middle section
        group_box = QGroupBox("Config")
        group_box_layout = QVBoxLayout()

        h_layout2 = QHBoxLayout()
        h_layout2.addWidget(QLabel("Interface"))
        h_layout2.addWidget(QComboBox())
        h_layout2.addWidget(QLabel("Browser:"))
        h_layout2.addWidget(QComboBox())
        h_layout2.addWidget(QLabel("Hidden:"))
        h_layout2.addWidget(QComboBox())
        group_box_layout.addLayout(h_layout2)

        h_layout3 = QHBoxLayout()
        h_layout3.addWidget(QLabel("Id:"))
        h_layout3.addWidget(QLineEdit())
        h_layout3.addWidget(QLabel("Browser:"))
        h_layout3.addWidget(QComboBox())
        h_layout3.addWidget(QLabel("x:"))
        h_layout3.addWidget(QLineEdit())
        h_layout3.addWidget(QLabel("y:"))
        h_layout3.addWidget(QLineEdit())
        group_box_layout.addLayout(h_layout3)

        group_box.setLayout(group_box_layout)
        layout.addWidget(group_box)

        # Bottom section
        h_layout4 = QHBoxLayout()
        h_layout4.addWidget(QPushButton("Add"))
        h_layout4.addWidget(QPushButton("Edit"))
        h_layout4.addWidget(QPushButton("Delete"))
        h_layout4.addWidget(QPushButton("Debug"))
        h_layout4.addWidget(QPushButton("Run"))
        h_layout4.addWidget(QPushButton("Do"))
        h_layout4.addWidget(QPushButton("Show"))
        layout.addLayout(h_layout4)

        # Set main layout
        self.setLayout(layout)
        self.setWindowTitle('Interfaz')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

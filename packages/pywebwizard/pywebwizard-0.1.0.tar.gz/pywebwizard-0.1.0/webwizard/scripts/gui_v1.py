import sys
from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMessageBox
from qt_material import apply_stylesheet


class QtWidgetGenerator:
    def __init__(self, parent):
        self.parent = parent

    def create_label(self, text, alignment=QtCore.Qt.AlignmentFlag.AlignLeft):
        label = QtWidgets.QLabel(text)
        label.setAlignment(alignment)
        return label

    def create_line_edit(self, placeholder_text="", read_only=False):
        line_edit = QtWidgets.QLineEdit()
        line_edit.setPlaceholderText(placeholder_text)
        line_edit.setReadOnly(read_only)
        return line_edit

    def create_button(self, text, click_handler=None):
        button = QtWidgets.QPushButton(text)
        if click_handler:
            button.clicked.connect(click_handler)
        return button

    def create_spin_box(self, min_value=0, max_value=100, initial_value=0):
        spin_box = QtWidgets.QSpinBox()
        spin_box.setRange(min_value, max_value)
        spin_box.setValue(initial_value)
        return spin_box

    def create_web_engine_view(self):
        web_view = QtWebEngineWidgets.QWebEngineView()
        return web_view

    def create_tree_view(self):
        tree_view = QtWidgets.QTreeView()
        return tree_view


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 800)
        self.setMinimumSize(400, 400)
        self.init_ui()

    def init_ui(self):
        # Crear un QTabWidget para las pestañas
        self.tab_widget = QtWidgets.QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')

        # Crear un menú desplegable en "File"
        options_menu = QtWidgets.QMenu('Open file...', self)
        file_menu.addMenu(options_menu)

        # Agregar opciones al menú desplegable
        option1_action = QtWidgets.QAction('From PC', self)
        option2_action = QtWidgets.QAction('From URL', self)
        options_menu.addAction(option1_action)
        options_menu.addAction(option2_action)

        # Agregar un separador
        file_menu.addSeparator()

        # Agregar "Exit" para salir de la aplicación
        exit_action = QtWidgets.QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Crear la primera pestaña
        self.create_tab()

        # Añadir el boton de crear nueva pestaña
        add_tab_button = QtWidgets.QPushButton("+", self)
        add_tab_button.clicked.connect(self.create_tab)
        self.tab_widget.setCornerWidget(add_tab_button, QtCore.Qt.TopRightCorner)

        # Agregar un botón de "+" para crear nuevas pestañas
        self.menu_bar = self.menuBar()

    def create_tab(self):
        # Crear una instancia de CustomTabWidget para cada pestaña
        custom_tab = CustomTabWidget(self.tab_widget)
        tab_index = self.tab_widget.addTab(custom_tab, "Pestaña {}".format(self.tab_widget.count()))

        # Establecer el último índice activo
        self.tab_widget.setCurrentIndex(tab_index)


class CustomTabWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        # Configura CustomTabWidget para que sea expansible en ambas dimensiones
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.parent = parent
        self.tab_number = 0
        self.init_ui()

        # Registrar el atajo de teclado Ctrl + S
        self.save_shortcut = QtWidgets.QShortcut(QKeySequence("Ctrl+S"), self)
        self.save_shortcut.activated.connect(self.save_changes)

    def init_ui(self):
        self.changed = False  # Variable para rastrear los cambios sin guardar

        widget_generator = QtWidgetGenerator(self)

        top_panel = QtWidgets.QWidget(self)
        top_panel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        top_panel.setGeometry(0, 0, 800, 200)
        grid = QtWidgets.QGridLayout(top_panel)

        self.tab_label = widget_generator.create_label("Pestaña {}".format(self.tab_number))
        self.tab_label.mouseDoubleClickEvent = self.rename_tab_label

        panel1 = QtWidgets.QWidget()
        panel1.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        panel1_layout = QtWidgets.QVBoxLayout(panel1)

        file_label = widget_generator.create_label("Cargar fichero YAML:")
        file_input = widget_generator.create_line_edit()
        panel1_layout.addWidget(file_label)
        panel1_layout.addWidget(file_input)

        url_label = widget_generator.create_label("URL (ejemplo: example.com):")
        url_input = widget_generator.create_line_edit("example.com")
        panel1_layout.addWidget(url_label)
        panel1_layout.addWidget(url_input)

        search_button = widget_generator.create_button("Buscar")
        panel1_layout.addWidget(search_button)

        timeout_label = widget_generator.create_label("Timeout (0-30):")
        timeout_input = widget_generator.create_spin_box(0, 30, 0)
        panel1_layout.addWidget(timeout_label)
        panel1_layout.addWidget(timeout_input)

        panel2 = QtWidgets.QWidget()
        panel2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        panel3 = QtWidgets.QWidget()
        panel3.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        panels_layout = QtWidgets.QHBoxLayout()
        panels_layout.addWidget(panel1)
        panels_layout.addWidget(panel2)
        panels_layout.addWidget(panel3)
        panels_layout.setStretch(0, 1)
        panels_layout.setStretch(1, 1)
        panels_layout.setStretch(2, 1)

        grid.addLayout(panels_layout, 0, 0)

        bottom_panel = QtWidgets.QWidget(self)
        bottom_panel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        bottom_panel.setGeometry(0, 200, 800, 600)
        bottom_layout = QtWidgets.QHBoxLayout(bottom_panel)

        web_view_panel = QtWidgets.QWidget()
        web_view_panel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        web_view_layout = QtWidgets.QVBoxLayout(web_view_panel)
        
        web_view = widget_generator.create_web_engine_view()
        web_view_layout.addWidget(web_view)

        tree_view_panel = QtWidgets.QWidget()
        tree_view_panel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        tree_view_layout = QtWidgets.QVBoxLayout(tree_view_panel)
        
        tree_view = widget_generator.create_tree_view()
        tree_view_layout.addWidget(tree_view)
        
        bottom_layout.addWidget(web_view_panel, 3)
        bottom_layout.addWidget(tree_view_panel, 1)

    def save_changes(self):
        self.changed = True  # TODO Hardcoded - remove this
        # Verificar si se han realizado cambios en la pestaña
        if self.changed:
            # Obtener el índice de la pestaña actual
            tab_index = self.parent.indexOf(self)

            # Mostrar un cuadro de diálogo para confirmar el guardado
            reply = QMessageBox.question(self, f'Guardar Cambios en Pestaña {tab_index}', '¿Desea guardar los cambios?',
                                         QMessageBox.Yes | QMessageBox.Cancel)

            if reply == QMessageBox.Yes:
                # Aquí puedes agregar la lógica para guardar los cambios
                # Puedes usar self.parent para acceder a la instancia de MainApp o hacerlo como mejor se adapte a tu estructura
                # Por ejemplo, podrías mostrar un cuadro de diálogo de guardado de archivo
                # y guardar los cambios en el archivo correspondiente.
                # Después de guardar los cambios, puedes restablecer self.changed a False.
                # Ejemplo:
                # guardar_cambios(self)
                print(f"Guardando cambios en Pestaña {tab_index}")
                self.changed = False

    # Función para permitir la edición del nombre de la pestaña al hacer doble clic en la etiqueta
    def rename_tab_label(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            old_text = self.tab_label.text()
            new_text, ok = QtWidgets.QInputDialog.getText(self, "Renombrar Pestaña", "Nuevo nombre:", QtWidgets.QLineEdit.Normal, old_text)
            if ok and new_text:
                self.tab_label.setText(new_text)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_amber.xml')
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())

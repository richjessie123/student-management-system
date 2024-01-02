from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, \
    QVBoxLayout, QComboBox, QToolBar, QStatusBar
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        # Call Parent Class and Set Window Title
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        # Set Menu Bars on top left for the main program window
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Make the File Menu Item Actionable by Connecting the Add Student Option to the Insert Method Below
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        # Make the Help Menu Item Actionable
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        # Make the Edit Menu Item Actionable by Connecting the Search Option to the Search Method Below
        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        # Create Table For the Main Window and set as Central Widget
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Id", "Name", "Course", "Mobile"])
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create Toolbar Object Instance and make it movable, add toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        # Add Action to Toolbar items
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Create Status bar and add status bar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        """This method loads the status bar widgets when a cell in the table is clocked"""
        edit_button = QPushButton("Edit Record")
        delete_button = QPushButton("Delete Record")

        # Connects the Edit and delete button when clicked to their methods below
        edit_button.clicked.connect(self.edit)
        delete_button.clicked.connect(self.delete)

        # Remove Edit and Delete Button
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)


    def load_data(self):
        """This method loads the SQL database that contains the student data and connects
        it to the table in the Main Window"""
        connection = sqlite3.connect("database.db")
        data = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(data):
            self.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))
        connection.close()

    def insert(self):
        """This method initiates the Insert Dialog class when the Add Student Menu Option under File is
        selected"""
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        """This method initiates the Search Dialog class when the Search Menu Option under Edit is
        selected"""
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        """This method initiates the Edit Dialog class when the Edit Record Button is
        selected"""
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        """This method initiates the Delete Dialog class when the Delete Record Button is
        selected"""
        dialog = DeleteDialog()
        dialog.exec()


class EditDialog(QDialog):
    """This class opens up a Dialog Box when the Edit Record Button is clicked"""
    pass


class DeleteDialog(QDialog):
    """This class opens up a Dialog Box when the Delete Record Button is clicked"""
    pass


class InsertDialog(QDialog):
    """This class opens a Dialog Box when the Add Student Menu Option is clicked"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Creation a Box Layout
        layout = QVBoxLayout()

        # Add Student Name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add student course options
        self.courses = QComboBox()
        course_options = ["Math", "Biology", "Astronomy", "Physics"]
        self.courses.addItems(course_options)
        layout.addWidget(self.courses)

        # Add Mobile
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add submit button and connect it to the register method below
        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def register(self):
        """This method inserts the student data from the dialog box into the SQL database
        and updates the data in the main window"""
        name = self.student_name.text()
        course = self.courses.currentText()
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?,?,?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class SearchDialog(QDialog):
    """This class opens a Dialog Box when the Search Menu Item is clicked"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add Student Name Search Bar
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add Student Search Button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.student_search)
        layout.addWidget(search_button)

        self.setLayout(layout)

    def student_search(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        results = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(), item.column()).setSelected(True)

        cursor.close()
        connection.close()


# Run program
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())

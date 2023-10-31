import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout,QLineEdit,QPushButton, QLabel

class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.num1_input = QLineEdit(self)
        self.num2_input = QLineEdit(self)
        self.add_button = QPushButton('ADD', self)
        self.sub_button = QPushButton('SUB', self)
        self.mul_button = QPushButton('MUL', self)
        self.div_button = QPushButton('DIV', self)
        self.result_label = QLabel(self)

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.num1_input)
        input_layout.addWidget(self.num2_input)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.sub_button)
        button_layout.addWidget(self.mul_button)
        button_layout.addWidget(self.div_button)

        main_layout = QHBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.result_label)

        self.setLayout(main_layout)

        self.add_button.clicked.connect(self.add)
        self.sub_button.clicked.connect(self.sub)
        self.mul_button.clicked.connect(self.mul)
        self.div_button.clicked.connect(self.div)

    def add(self):
        num1 = float(self.num1_input.text())
        num2 = float(self.num2_input.text())
        result = num1 + num2
        self.result_label.setText(f'Result: {result}')

    def sub(self):
        num1 = float(self.num1_input.text())
        num2 = float(self.num2_input.text())
        result = num1 - num2
        self.result_label.setText(f'Result: {result}')

    def mul(self):
        num1 = float(self.num1_input.text())
        num2 = float(self.num2_input.text())
        result = num1 * num2
        self.result_label.setText(f'Result: {result}')

    def div(self):
        num1 = float(self.num1_input.text())
        num2 = float(self.num2_input.text())
        result = num1 / num2
        self.result_label.setText(f'Result: {result}')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mycalc = CalculatorApp()
    mycalc.setWindowTitle("My Calculator")
    mycalc.show()
    sys.exit(app.exec_())
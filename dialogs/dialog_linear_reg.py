import json
import os

from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton

class InputDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        value_a = None
        value_b = None
        units = None
        try:
            with open('data/params_linear_reg.json', 'r') as file:
                data_json = json.loads(file.read())
            value_a = data_json.get('a', 0)
            value_b = data_json.get('b', 0)
            units = data_json.get('units', "''")
        except:
            pass

        # Параметр a
        self.label_a = QLabel('Введите параметр "a":')

        self.input_a = QLineEdit(self)
        validator_a = QDoubleValidator()
        self.input_a.setValidator(validator_a)
        self.input_a.setPlaceholderText('Только число')
        layout.addWidget(self.label_a)
        layout.addWidget(self.input_a)

        # Параметр b
        self.label_b = QLabel('Введите параметр "b":')
        self.input_b = QLineEdit(self)
        validator_b = QDoubleValidator()
        self.input_b.setValidator(validator_b)
        self.input_b.setPlaceholderText('Только число')
        layout.addWidget(self.label_b)
        layout.addWidget(self.input_b)

        # Единицы измерения
        self.label_units = QLabel('Выберите единицы измерения:')
        self.combo_units = QComboBox(self)
        self.combo_units.addItems(["''", "'", 'mrad'])
        layout.addWidget(self.label_units)
        layout.addWidget(self.combo_units)

        if value_a is not None:
            self.input_a.setText(str(value_a))
        if value_b is not None:
            self.input_b.setText(str(value_b))
        if units is not None:
            self.combo_units.setCurrentText(str(units))

        # Кнопка отправки
        self.btn_submit = QPushButton('Сохранить', self)
        self.btn_submit.clicked.connect(self.submit)
        layout.addWidget(self.btn_submit)

        self.setLayout(layout)

    @staticmethod
    def create_directory(folder_path):
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            return
        else:
            os.makedirs(folder_path)
    def submit(self):
        # Получение значений
        value_a = self.input_a.text()
        value_b = self.input_b.text()
        units = self.combo_units.currentText()

        # Проверка на ввод только чисел
        try:
            value_a = float(value_a)
            value_b = float(value_b)
            print(f'Параметр "a": {value_a}, Параметр "b": {value_b}, Единицы измерения: {units}')
            data_json = {'a': value_a, 'b': value_b, 'units': units}
            current_directory = os.getcwd()
            self.create_directory(current_directory.replace('\\', '/') + '/data')
            with open('data/params_linear_reg.json', 'w+') as file:
                file.write(json.dumps(data_json))
            self.accept()
        except ValueError:
            print('Пожалуйста, введите только числовые значения для параметров "a" и "b".')

if __name__ == '__main__':
    app = QApplication([])
    dialog = InputDialog()
    if dialog.exec_():
        print('Данные отправлены')
    else:
        print('Отправка отменена')

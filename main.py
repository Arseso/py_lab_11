import sys
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainter, QTextLayout, QFont, QColor
from PySide6.QtWidgets import QApplication, QWidget, QScrollArea, QVBoxLayout

from parse_json import parse_json

class ResumeWidget(QWidget):
    def __init__(self, text: str):
        super().__init__()
        self.text = text
        self.setFixedWidth(760)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        # Draw shapes on the sides
        painter.setBrush(QColor(0, 200, 200))
        painter.drawEllipse(-50, rect.height() // 4, 100, 100)
        painter.drawEllipse(rect.width() - 50, rect.height() // 4, 100, 100)

        font = QFont("Arial", 12)
        layout = QTextLayout()
        layout.setFont(font)

        y = 5
        lines = self.text.split('\n')
        total_height = 0
        for line in lines:
            layout.setText(line)
            layout.beginLayout()
            while True:
                text_line = layout.createLine()
                if not text_line.isValid():
                    break
                text_line.setLineWidth(rect.width() - 40)
                text_line.setPosition(QPointF(30, y))
                y += text_line.height()
            layout.endLayout()
            layout.draw(painter, QPointF(30, y))
            y += 1  # Добавляем немного пространства между строками
            total_height = y  # Накопление высоты всех строк

        self.setFixedHeight(total_height+600)  # Устанавливаем высоту виджета на основе накопленной высоты

class MainWindow(QWidget):
    def __init__(self, text: str):
        super().__init__()
        self.setWindowTitle("Резюме")
        self.setGeometry(100, 100, 800, 600)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        resume_widget = ResumeWidget(text)
        scroll_area.setWidget(resume_widget)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_resume.json>")
        return

    FILE_NAME = sys.argv[1]
    text = parse_json(FILE_NAME)
    print(text)

    app = QApplication(sys.argv)
    window = MainWindow(text)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()

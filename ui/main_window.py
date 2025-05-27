# PyQt5 MainWindow for Ollama Chat GUI v0
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton, QTextBrowser
from core.api import generate

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ollama Chat GUI")
        self.resize(600, 500)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.outputBox = QTextBrowser(objectName="outputBox")
        layout.addWidget(self.outputBox)

        self.inputBox = QTextEdit(objectName="inputBox")
        self.inputBox.setFixedHeight(80)
        layout.addWidget(self.inputBox)

        self.sendButton = QPushButton("Send", objectName="sendButton")
        self.sendButton.clicked.connect(self.send_prompt)
        layout.addWidget(self.sendButton)

    def send_prompt(self):
        prompt = self.inputBox.toPlainText().strip()
        if not prompt:
            return
        self.outputBox.append(f"<b>You:</b> {prompt}")
        self.inputBox.clear()
        try:
            response = generate(prompt, model="llama3.2-vision:latest")
            self.outputBox.append(f"<b>Ollama:</b> {response}")
        except Exception as e:
            self.outputBox.append(f"<span style='color:red'>Error: {e}</span>")

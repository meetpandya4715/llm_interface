# PyQt5 MainWindow for Ollama Chat GUI v1
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton, QTextBrowser, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QTextCursor # Import QTextCursor
from core.api import generate, get_models
import datetime
import html # Import the html module

class GenerateThread(QThread):
    result = pyqtSignal(str, str)
    error = pyqtSignal(str)
    def __init__(self, prompt, model, history): # Added history
        super().__init__()
        self.prompt = prompt
        self.model = model
        self.history = history # Store history

    def run(self):
        try:
            # Pass history to generate function
            response = generate(self.prompt, self.model, self.history)
            self.result.emit(self.prompt, response)
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ollama Chat GUI")
        self.resize(600, 500)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.chat_history = [] # Initialize chat history

        self.outputBox = QTextBrowser(objectName="outputBox")
        layout.addWidget(self.outputBox)

        # Model selector and clear button
        top_bar = QHBoxLayout()
        self.modelSelector = QComboBox(objectName="modelSelector")
        self.modelSelector.addItem("Loading models...")
        top_bar.addWidget(self.modelSelector)
        self.clearButton = QPushButton("Clear", objectName="clearButton")
        self.clearButton.clicked.connect(self.clear_chat)
        top_bar.addWidget(self.clearButton)
        layout.addLayout(top_bar)

        self.inputBox = QTextEdit(objectName="inputBox")
        self.inputBox.setFixedHeight(80)
        self.inputBox.setPlaceholderText("Type your message and press Ctrl+Enter or Send...")
        layout.addWidget(self.inputBox)
        self.inputBox.keyPressEvent = self.input_keypress

        self.sendButton = QPushButton("Send", objectName="sendButton")
        self.sendButton.clicked.connect(self.send_prompt)
        layout.addWidget(self.sendButton)

        self.load_models()

    def load_models(self):
        try:
            models = get_models()
            self.modelSelector.clear()
            if models:
                self.modelSelector.addItems(models)
                self.sendButton.setEnabled(True)
                self.inputBox.setEnabled(True)
            else:
                self.modelSelector.addItem("No models found")
                self.sendButton.setEnabled(False)
                self.inputBox.setEnabled(False)
        except Exception as e:
            self.modelSelector.clear()
            self.modelSelector.addItem("Connection failed")
            self.display_error(str(e))
            self.sendButton.setEnabled(False)
            self.inputBox.setEnabled(False)

    def input_keypress(self, event):
        if event.key() == Qt.Key_Return and (event.modifiers() & Qt.ControlModifier):
            self.send_prompt()
        else:
            QTextEdit.keyPressEvent(self.inputBox, event)

    def send_prompt(self):
        prompt = self.inputBox.toPlainText().strip()
        if not prompt:
            return
        model = self.modelSelector.currentText()
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        # Escape HTML in prompt before displaying
        escaped_prompt = html.escape(prompt)
        self.outputBox.append(f"<hr><b>{timestamp} You:</b> {escaped_prompt}")

        self.inputBox.clear()
        self.sendButton.setEnabled(False)
        # The new api.generate handles adding the prompt to the history
        self.thread = GenerateThread(prompt, model, list(self.chat_history))  # Pass a copy
        self.thread.result.connect(self.display_response)
        self.thread.error.connect(self.display_error)
        self.thread.finished.connect(lambda: self.sendButton.setEnabled(True))
        self.thread.start()

    def display_response(self, prompt, response):
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        # Escape HTML in response before displaying
        escaped_response = html.escape(response)
        self.outputBox.append(f"<b>{timestamp} Ollama:</b> {escaped_response}")
        # Add user and assistant messages to history
        self.chat_history.append({"role": "user", "content": prompt})
        self.chat_history.append({"role": "assistant", "content": response})

    def display_error(self, error):
        self.outputBox.append(f"<span style='color:red'>Error: {error}</span>")
        # No action needed on history, as it's only updated on success


    def clear_chat(self):
        self.outputBox.clear()
        self.chat_history = [] # Clear history

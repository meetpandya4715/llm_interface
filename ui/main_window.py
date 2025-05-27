# PyQt5 MainWindow for Ollama Chat GUI v1
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton, QTextBrowser, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from core.api import generate, get_models
import datetime

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
            self.modelSelector.addItems(models)
        except Exception as e:
            self.modelSelector.clear()
            self.modelSelector.addItem(f"Error: {e}")

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
        self.outputBox.append(f"<hr><b>{timestamp} You:</b> {prompt}")
        
        # Add user message to history BEFORE making the API call
        self.chat_history.append({"role": "user", "content": prompt})
        
        self.inputBox.clear()
        self.sendButton.setEnabled(False)
        # Pass current chat_history to the thread
        self.thread = GenerateThread(prompt, model, list(self.chat_history)) # Pass a copy
        self.thread.result.connect(self.display_response)
        self.thread.error.connect(self.display_error)
        self.thread.finished.connect(lambda: self.sendButton.setEnabled(True))
        self.thread.start()

    def display_response(self, prompt, response):
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        self.outputBox.append(f"<b>{timestamp} Ollama:</b> {response}")
        # Add assistant message to history
        self.chat_history.append({"role": "assistant", "content": response})

    def display_error(self, error):
        self.outputBox.append(f"<span style='color:red'>Error: {error}</span>")
        # Optionally, remove the last user message from history if API call failed
        # if self.chat_history and self.chat_history[-1][\"role\"] == \"user\":
        #     self.chat_history.pop()


    def clear_chat(self):
        self.outputBox.clear()
        self.chat_history = [] # Clear history

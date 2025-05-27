# 🧠 Ollama Chat GUI

A PyQt5-based desktop interface to interact with locally hosted Ollama LLMs.

## Overview

Ollama Chat GUI is a lightweight and user-friendly desktop application designed to facilitate interaction with locally hosted large language models (LLMs). It provides features such as chat history, model selection, and asynchronous responsiveness.

## Features

- **Chat Interface**: Send prompts and receive responses from the LLM.
- **Chat History**: View previous interactions with timestamps.
- **Model Selector**: Choose from available models hosted locally.
- **Keyboard Shortcuts**: Use Ctrl+Enter to send prompts quickly.
- **Error Handling**: Display errors gracefully in the chat window.

## Requirements

- Python 3.8+
- Locally hosted Ollama server running on `localhost:11434`

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd llm_interface
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the Ollama server is running locally:
   ```bash
   # Example command to start the server
   ollama start
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Interact with the GUI:
   - Type your message in the input box.
   - Press Ctrl+Enter or click "Send" to submit your prompt.
   - View the response in the output box.

3. Select a model from the dropdown menu to switch between available models.

4. Use the "Clear" button to reset the chat history.

## Folder Structure

```
ollama_chat_gui/
├── main.py # Entry point
├── ui/ # PyQt5 UI components
│ └── main_window.py
├── core/ # API and logic
│ ├── api.py # Ollama API calls
│ └── utils.py # Helpers (tokenizer, markdown, etc.)
├── assets/ # Icons, themes, etc.
├── styles/ # QSS themes
├── settings.json # Persistent config
└── README.md
```

## Future Plans

Refer to the [TODO.md](TODO.md) file for planned features and development roadmap.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

## Contact

For questions or support, please contact [meetpandya4715@gmail.com].

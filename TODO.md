# 🧠 Ollama Chat GUI — Development TODO

A PyQt5-based desktop interface to interact with locally hosted Ollama LLMs.

---

## ✅ v0 — MVP: Minimal Chat Interface
> Goal: Send a prompt, display non-streamed response.

### UI Setup
- [x] `ui/main_window.py`: Create `QMainWindow` with vertical layout
- [x] Add `QTextEdit` for input box (objectName: `inputBox`)
- [x] Add `QPushButton` labeled "Send" (objectName: `sendButton`)
- [x] Add `QTextBrowser` for output display (objectName: `outputBox`)

### Backend
- [x] `core/api.py`: Implement `generate(prompt: str, model: str) -> str`
- [x] Use `requests.post` with `stream: false` to `localhost:11434/api/generate`
- [x] Basic error handling (connection refused, 500, etc.)

### Integration
- [x] Connect button click to `send_prompt()` logic
- [x] Display model output in `outputBox`

---

## 🚀 v1 — Functional Chat Client
> Goal: Add basic history, model selector, and async responsiveness.

### Chat History
- [x] Append each prompt and response to `outputBox` with clear separators
- [x] Add timestamp per message (format: `[HH:MM:SS]`)

### Model Selector
- [x] `core/api.py`: Implement `get_models() -> List[str]` from `/api/tags`
- [x] Add `QComboBox` for model selection (objectName: `modelSelector`)

### Usability
- [x] Add keyboard shortcut: Ctrl+Enter triggers send
- [x] Add `QPushButton` to clear chat (objectName: `clearButton`)
- [x] Use `QThread` or `asyncio` to offload `generate()` to avoid UI freezing

---

## ⚙️ v2 — Streaming & Controls
> Goal: Enable streaming output with live feedback and cancellation.

### Streaming
- [ ] Replace `requests` with `httpx.AsyncClient` for streaming mode
- [ ] Parse `event-stream` chunks and append tokens in real time
- [ ] Update UI incrementally as data arrives

### Control
- [ ] Add "Cancel" button to interrupt streaming call
- [ ] Show "Generating..." status while request is active

### Settings
- [ ] Add sliders/spinboxes for `temperature`, `top_p` (optional section)
- [ ] Pass config parameters to API request payload

---

## 🧠 v3 — Developer & Power Features
> Goal: Markdown rendering, code highlighting, and dev tools.

### Rich Output
- [ ] Convert markdown to HTML and inject into `QTextBrowser`
- [ ] Add basic support for `**bold**`, `*italic*`, `\`\`\`code\`\`\``

### Syntax Highlighting
- [ ] Use `QSyntaxHighlighter` for `QPlainTextEdit` fallback mode
- [ ] Language detection from code block (e.g., ```python)

### Debugging
- [ ] Display token estimate (use `tiktoken` or similar)
- [ ] Measure and show latency per response

---

## ✨ v4 — UX Polish & Multi-Session
> Goal: Make it smooth, persistent, and production-like.

### Persistence
- [ ] Save/load chat history to `.jsonl`
- [ ] Store selected model, temperature, and theme in `~/.ollama-chat/config.json`

### Session Management
- [ ] Add tabbed interface for multi-model or multi-session chats
- [ ] Allow renaming tabs

### Theming
- [ ] Light/dark theme toggle (QSS or dynamic stylesheet)
- [ ] Save last used theme across sessions

### System Integration
- [ ] Add minimize-to-tray support
- [ ] Play notification sound on completion (optional)

---

## 📁 Folder Structure Plan (For Agent Navigation)

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

---

## 🔖 Tags for Coding Agent
- `#priority:high` — v0 & v1 tasks
- `#streaming` — v2
- `#markdown` — v3
- `#config` — v4
- `#agent_focus` — Agent-friendly structure and filenames

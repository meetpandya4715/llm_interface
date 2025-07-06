# Ollama API call logic for v1 (using /api/chat)
import requests
from typing import Optional, List, Dict

def generate(prompt: str, model: str, history: Optional[List[Dict[str, str]]] = None) -> str:
    """
    Generate a response from the LLM using the /api/chat endpoint.
    history: list of dicts, e.g. [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "hello!"}]
    """
    url = "http://localhost:11434/api/chat"

    # Combine history with the new prompt
    messages = history or []
    messages.append({"role": "user", "content": prompt})

    payload = {"model": model, "messages": messages, "stream": False}
    try:
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        # The response from /api/chat is structured differently
        if "message" in data and "content" in data["message"]:
            return data["message"]["content"]
        return "[No response content]"
    except requests.ConnectionError:
        raise RuntimeError("Could not connect to Ollama server at localhost:11434.")
    except requests.HTTPError as e:
        # Try to get a more descriptive error from the response body
        try:
            error_detail = e.response.json().get("error", "Unknown error")
        except Exception:
            error_detail = e.response.text
        raise RuntimeError(f"HTTP error: {e.response.status_code} - {error_detail}")
    except Exception as e:
        raise RuntimeError(str(e))

def get_models() -> list:
    url = "http://localhost:11434/api/tags"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # Expecting {"models": [{"name": ...}, ...]}
        return [m["name"] for m in data.get("models", [])]
    except requests.ConnectionError:
        raise RuntimeError("Could not connect to Ollama server at localhost:11434.")
    except requests.HTTPError as e:
        raise RuntimeError(f"HTTP error: {e.response.status_code}")
    except Exception as e:
        raise RuntimeError(str(e))

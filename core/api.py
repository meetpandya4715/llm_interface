# Ollama API call logic for v0
import requests

def generate(prompt: str, model: str) -> str:
    url = "http://localhost:11434/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False}
    try:
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "[No response]")
    except requests.ConnectionError:
        raise RuntimeError("Could not connect to Ollama server at localhost:11434.")
    except requests.HTTPError as e:
        raise RuntimeError(f"HTTP error: {e.response.status_code}")
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

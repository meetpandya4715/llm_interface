# Ollama API call logic for v0
import requests

def generate(prompt: str, model: str, history: list | None = None) -> str:
    """
    Generate a response from the LLM, including previous chat history as context.
    history: list of dicts, e.g. [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "hello!"}]
    """
    url = "http://localhost:11434/api/generate"

    # Format history and current prompt for Ollama
    # Ollama's /api/generate endpoint expects a single "prompt" string.
    # We'll concatenate the history and the new prompt.
    # For /api/chat (which supports a messages list directly), this would be different.
    full_prompt = ""
    if history:
        for message in history:
            # Ensuring message is a dict with 'role' and 'content'
            if isinstance(message, dict) and "role" in message and "content" in message:
                full_prompt += f"{message['role'].capitalize()}: {message['content']}\n"
            else:
                # Fallback for unexpected history format, or skip
                print(f"Warning: Skipping malformed history entry: {message}")


    full_prompt += f"User: {prompt}\nAssistant:" # Ensure the model knows it's its turn

    payload = {"model": model, "prompt": full_prompt, "stream": False}
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

# parse.py

# ✅ This function takes a fully constructed prompt string
# and sends it to the locally running LLaMA 3 model using Ollama.

def parse_with_ollama(prompt: str):
    try:
        from ollama import chat  # Native Ollama Python API
    except ImportError:
        raise ImportError("Make sure you have installed the Ollama Python package: pip install ollama")

    try:
        response = chat(
            model="llama3",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"❌ Error during LLaMA call: {str(e)}"

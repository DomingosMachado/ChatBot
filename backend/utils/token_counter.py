import tiktoken

def count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fallback to cl100k_base encoding
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))
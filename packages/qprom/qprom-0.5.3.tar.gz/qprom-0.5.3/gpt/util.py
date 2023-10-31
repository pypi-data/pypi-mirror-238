import tiktoken


def get_token_amount_from_string(text: str):
    # cl100k_base is for gpt-4 and gpt-3.5-turbo
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))
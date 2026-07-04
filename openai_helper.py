import os

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - depends on environment
    OpenAI = None


DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def ask_openai(system_prompt, user_prompt, model=None):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    if OpenAI is None:
        return None

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=model or DEFAULT_MODEL,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return getattr(response, "output_text", None) or ""
    except Exception:
        return None

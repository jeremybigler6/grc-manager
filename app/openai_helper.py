import os

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def ask_openai(system_prompt, user_prompt, model=None):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("DEBUG: OPENAI_API_KEY was not found.")
        return None

    if OpenAI is None:
        print("DEBUG: OpenAI package is not installed.")
        return None

    try:
        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model=model or DEFAULT_MODEL,
            instructions=system_prompt,
            input=user_prompt,
        )

        return response.output_text

    except Exception as e:
        print("DEBUG: OpenAI API error:")
        print(e)
        return None
        
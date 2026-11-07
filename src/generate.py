import json
import re
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ---- settings ----
PROVIDER = "anthropic"        # "anthropic", "openai" or "gemini"
MODEL = "claude-sonnet-5-5"   # exact model name from the provider's docs
N_RUNS = 1                    # repetitions per prompt and condition
TEMPERATURE = 1.0             # set to None if the API rejects it
MAX_TOKENS = 2000
SYSTEM_PROMPT = (
    "You are a Python coding assistant. "
    "Reply with the code only, in one ```python block, without explanations."
)

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_FILE = ROOT / "prompts" / "prompts.json"
SAFE_MODEL = MODEL.replace("_", "-")
OUT_DIR = ROOT / "data" / "generated" / SAFE_MODEL


def ask_anthropic(prompt):
    import anthropic
    client = anthropic.Anthropic()
    kwargs = dict(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    if TEMPERATURE is not None:
        kwargs["temperature"] = TEMPERATURE
    response = client.messages.create(**kwargs)
    return "".join(b.text for b in response.content if b.type == "text")


def ask_openai(prompt):
    from openai import OpenAI
    client = OpenAI()
    kwargs = dict(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    if TEMPERATURE is not None:
        kwargs["temperature"] = TEMPERATURE
    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content


def ask_gemini(prompt):
    from google import genai
    from google.genai import types
    client = genai.Client()
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=TEMPERATURE,
    )
    response = client.models.generate_content(
        model=MODEL, contents=prompt, config=config
    )
    return response.text


ASK = {"anthropic": ask_anthropic, "openai": ask_openai, "gemini": ask_gemini}


def extract_code(text):
    """Return the code from the first ```python block, or the whole text."""
    match = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.DOTALL)
    code = match.group(1) if match else text
    return code.strip() + "\n"


def main():
    prompts = json.loads(PROMPTS_FILE.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ask = ASK[PROVIDER]

    for item in prompts:
        for condition in ("A", "B"):
            for run in range(1, N_RUNS + 1):
                path = OUT_DIR / f"{SAFE_MODEL}_{condition}_{item['id']:02d}_{run:02d}.py"
                if path.exists():          # lets you resume after an interruption
                    continue

                text = None
                for attempt in range(3):
                    try:
                        text = ask(item[f"prompt_{condition}"])
                        break
                    except Exception as e:
                        print(f"Error on {path.name} (attempt {attempt + 1}): {e}")
                        time.sleep(5)
                if text is None:
                    continue

                path.write_text(extract_code(text), encoding="utf-8")
                print("saved", path.name)


if __name__ == "__main__":
    main()
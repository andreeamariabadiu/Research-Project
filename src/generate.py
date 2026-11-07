import json
import os
import re
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# ---- settings ----
MODEL = "gemini-3.6-flash"
RUN_START = 1
N_RUNS = 1
TEMPERATURE = 1.0
PAUSE_SECONDS = 13
RETRY_WAIT_SECONDS = 60
TIMEOUT_SECONDS = 120
SYSTEM_PROMPT = (
    "You are a Python coding assistant. "
    "Reply with the code only, in one ```python block, without explanations."
)

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_FILE = ROOT / "prompts" / "prompts.json"
SAFE_MODEL = MODEL.replace("_", "-")
OUT_DIR = ROOT / "data" / "generated" / SAFE_MODEL

client = genai.Client(
    http_options=types.HttpOptions(timeout=TIMEOUT_SECONDS * 1000)
)


def ask_gemini(prompt):
    # max_output_tokens is intentionally not set: Gemini counts its internal
    # "thinking" tokens in that limit and could return empty text.
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=TEMPERATURE,
    )
    response = client.models.generate_content(
        model=MODEL, contents=prompt, config=config
    )
    return response.text


def extract_code(text):
    """Return the code from the first ```python block, or the whole text."""
    match = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.DOTALL)
    code = match.group(1) if match else text
    return code.strip() + "\n"


def main():
    print("Starting generate.py", flush=True)
    print("Model:", MODEL, flush=True)
    print("API key found:", bool(os.getenv("GEMINI_API_KEY")), flush=True)
    print("Prompts file:", PROMPTS_FILE, "| exists:", PROMPTS_FILE.exists(), flush=True)
    print("Output folder:", OUT_DIR, flush=True)

    prompts = json.loads(PROMPTS_FILE.read_text(encoding="utf-8"))
    print("Prompts loaded:", len(prompts), flush=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    generated = 0
    skipped_existing = 0
    failed = []
    for item in prompts:
        for condition in ("A", "B"):
            for run in range(RUN_START, RUN_START + N_RUNS):
                path = OUT_DIR / f"{SAFE_MODEL}_{condition}_{item['id']:02d}_{run:02d}.py"
                if path.exists():
                    skipped_existing += 1
                    print("already exists, skipping", path.name, flush=True)
                    continue

                print("requesting", path.name, "...", flush=True)
                text = None
                for attempt in range(3):
                    try:
                        text = ask_gemini(item[f"prompt_{condition}"])
                        if text and text.strip():
                            break
                        print(f"Empty answer for {path.name} (attempt {attempt + 1})", flush=True)
                        text = None
                    except Exception as e:
                        print(f"Error on {path.name} (attempt {attempt + 1}): {str(e)[:300]}", flush=True)
                    time.sleep(RETRY_WAIT_SECONDS)
                if text is None:
                    print(f"SKIPPED {path.name}", flush=True)
                    failed.append(path.name)
                    continue

                path.write_text(extract_code(text), encoding="utf-8")
                generated += 1
                print("saved", path.name, flush=True)
                time.sleep(PAUSE_SECONDS)

    print(f"\nDone. Generated: {generated}, already existed: {skipped_existing}, failed: {len(failed)}", flush=True)
    for name in failed:
        print("  failed:", name, flush=True)
    if failed:
        print("Run the script again later (e.g. after the daily quota resets) to fill the missing files.", flush=True)


if __name__ == "__main__":
    main()
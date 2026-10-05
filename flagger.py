"""
This file's purpose is to read relevent information from the provided text files and call the AI agent.

Use by: putting API key in file, then run python flagger.py
"""

import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from criteria import CRITERIA, criteria_as_text

load_dotenv()  # will read the groq API key & model if applicable from the .env file

# If current model doesn't work, go to console.groq.com
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

HERE = Path(__file__).parent
NOTES_DIR = HERE / "notes"
OUTPUT_FILE = HERE / "results.json"
SECONDS_BETWEEN_REQUESTS = 2  # ensuring free API is not overwhelmed by requests

SYSTEM_PROMPT = f"""You will review ophthalmology clinical notes and flag patients who
meet criteria for tests or procedures that are not yet ordered.

Criteria:
{criteria_as_text()}

Rules:
- Only flag a criterion if the note contains evidence for EVERY part of it.
- Quote the specific evidence from the note in your reasoning.
- Always respond by calling record_flags. If nothing applies, call it with an empty flags list.
- You are assisting a clinician, not making an actual diagnosis."""

# Ensures the model will all the funciton & return data according to schema, ensuring readability & realiability
FLAG_TOOL = {
    "type": "function",
    "function": {
        "name": "record_flags",
        "description": "Record which criteria the patient meets, with evidence and reasoning.",
        "parameters": {
            "type": "object",
            "properties": {
                "flags": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "criterion": {"type": "string", "enum": list(CRITERIA)},
                            "evidence": {
                                "type": "string",
                                "description": "Short quote(s) from the note supporting the flag.",
                            },
                            "reasoning": {"type": "string"},
                            "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
                        },
                        "required": ["criterion", "evidence", "reasoning", "confidence"],
                    },
                }
            },
            "required": ["flags"],
        },
    },
}


def flag_note(client: Groq, note_text: str) -> list[dict]:
    """Send one note to the model and return its list of flags."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Clinical note:\n\n{note_text}"},
        ],
        tools=[FLAG_TOOL],
        tool_choice={"type": "function", "function": {"name": "record_flags"}},
        temperature=0,  # make results as repeatable as possible for evaluation
    )
    tool_calls = response.choices[0].message.tool_calls
    if not tool_calls:
        return []
    return json.loads(tool_calls[0].function.arguments).get("flags", [])


def main() -> None:
    if not os.getenv("GROQ_API_KEY"):
        raise SystemExit("GROQ_API_KEY not found. Create a .env file (see .env.example).")

    client = Groq()  # picks up GROQ_API_KEY automatically
    results = {}
    note_paths = sorted(NOTES_DIR.glob("*.txt"))
    print(f"Using model: {MODEL}\n")

    for i, note_path in enumerate(note_paths):
        print(f"Processing {note_path.name}...")
        try:
            flags = flag_note(client, note_path.read_text(encoding="utf-8"))
            results[note_path.name] = flags
            for flag in flags:
                print(f"  FLAG: {flag['criterion']} ({flag['confidence']}) - {flag['evidence']}")
            if not flags:
                print("  No flags.")
        except Exception as err:  # one bad call shouldn't crash the whole batch
            print(f"  Error on {note_path.name}: {err}")
            results[note_path.name] = {"error": str(err)}

        if i < len(note_paths) - 1:
            time.sleep(SECONDS_BETWEEN_REQUESTS)

    OUTPUT_FILE.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nSaved results to {OUTPUT_FILE.name}. Run: python evaluate.py")


if __name__ == "__main__":
    main()
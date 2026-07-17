import os
import json
import hashlib

from groq import Groq
from dotenv import load_dotenv

from app.database.database import get_connection

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

OUTPUT_DIR = "generated_outputs"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


def get_selection_text(selection_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT n.title,
           n.content
    FROM nodes n
    JOIN selection_nodes sn
    ON n.id = sn.node_id
    WHERE sn.selection_id = ?
    """, (selection_id,))

    rows = cursor.fetchall()

    conn.close()

    text = ""

    for row in rows:

        text += f"\n\nSECTION: {row['title']}\n"
        text += row["content"]

    return text


def generate_test_cases(selection_id):

    text = get_selection_text(
        selection_id
    )

    if not text.strip():

        return {
            "error": "No content found for selection"
        }

    prompt = f"""
You are a QA Engineer.

Using ONLY the provided manual content.

Generate 3-5 QA test cases.

For each test case provide:

1. Test Case Name
2. Objective
3. Expected Result

Manual Content:

{text}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        generated_text = (
            response
            .choices[0]
            .message.content
        )

    except Exception as e:

        return {
            "error": f"Groq API Error: {str(e)}"
        }

    # Structured output validation

    if not generated_text:

        return {
            "error": "LLM returned empty output"
        }

    if len(generated_text.strip()) < 20:

        return {
            "error": "LLM output too short or malformed"
        }

    source_hash = hashlib.sha256(
        text.encode()
    ).hexdigest()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO generations
        (
            selection_id,
            generated_text,
            model_name,
            source_hash
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            selection_id,
            generated_text,
            "llama-3.3-70b-versatile",
            source_hash
        )
    )

    generation_id = cursor.lastrowid

    conn.commit()
    conn.close()

    # NoSQL-style JSON storage

    output_data = {
        "generation_id": generation_id,
        "selection_id": selection_id,
        "generated_text": generated_text,
        "source_hash": source_hash,
        "model": "llama-3.3-70b-versatile"
    }

    with open(
        f"{OUTPUT_DIR}/generation_{generation_id}.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            output_data,
            f,
            indent=4,
            ensure_ascii=False
        )

    return {
        "generation_id": generation_id,
        "generated_text": generated_text
    }
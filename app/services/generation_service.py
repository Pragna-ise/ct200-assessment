import os
import hashlib

from groq import Groq
from dotenv import load_dotenv

from app.database.database import get_connection

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
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

    prompt = f"""
You are a QA engineer.

Based ONLY on the following manual content.

Generate 3-5 QA test case ideas.

Return:
1. Test Case Name
2. Objective
3. Expected Result

Manual Content:
{text}
"""
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
    return {
        "generation_id": generation_id,
        "generated_text": generated_text
    }